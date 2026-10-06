"""Purchase service."""

from __future__ import annotations

from datetime import datetime, timezone
from decimal import Decimal

from src.models.customer import Customer
from src.models.purchase import Purchase
from src.models.purchase_item import PurchaseItem
from src.repositories.purchase_repository import PurchaseRepository
from src.services.customer_service import CustomerService
from src.services.drink_service import DrinkService
from src.services.baked_good_service import BakedGoodService
from src.services.ingredient_service import IngredientService
from src.validators import validate_purchase_timestamp_utc
from src.exceptions import CustomerLifetimeSpentIsIncorrectError
from src.exceptions import InsufficientStockError
from src.models.purchase import Purchase, PurchaseItem


class PurchaseService:
    """Enforce purchase business rules and related customer/item validation."""

    def __init__(
        self,
        repository: PurchaseRepository,
        customer_service: CustomerService | None = None,
        drink_service: DrinkService | None = None,
        baked_good_service: BakedGoodService | None = None,
        ingredient_service: IngredientService | None = None,
    ):
        self._repository = repository
        self._customer_service = customer_service
        self._drink_service = drink_service
        self._baked_good_service = baked_good_service
        self._ingredient_service = ingredient_service

    def get_all(self) -> list[Purchase]:
        return self._repository.get_all()

    def get_by_id(self, purchase_id: int) -> Purchase | None:
        return self._repository.get_by_id(purchase_id)

    def create_purchase(self, purchase: Purchase) -> Purchase:
        self._validate_purchase(purchase)
        purchase.total_cost = self._calculate_total_cost(purchase)
        purchase.timestamp = self._normalize_timestamp(purchase.timestamp)

        created_purchase = self._repository.add(purchase)

        if purchase.customer_id is not None and self._customer_service is not None:
            record_purchase = getattr(self._customer_service, "record_purchase", None)
            if callable(record_purchase):
                record_purchase(purchase.customer_id, created_purchase.total_cost)

        return created_purchase

    def purchase_a_drink(self, name: str, email: str, drink_id: int) -> Purchase:
        """Sell one drink to a new customer, record the sale, and deduct stock."""
        drink = self._drink_service.get_by_id(drink_id)
        if drink is None:
            raise ValueError("Drink does not exist.")

        for recipe_item in drink.recipe:
            if not self._ingredient_service.is_ingredient_amount_sufficient(
                recipe_item.ingredient_id, recipe_item.quantity
            ):
                raise InsufficientStockError(
                    f"Not enough stock for ingredient id {recipe_item.ingredient_id}."
                )

        customer = self._customer_service.get_by_email(email)
        if customer is None:
            customer = self._customer_service.create_customer(
                Customer(name=name, email=email)
            )

        purchase = Purchase(
            customer_id=customer.id,
            timestamp=datetime.now(timezone.utc),
            items=[
                PurchaseItem(
                    item_type="drink",
                    item_id=drink_id,
                    quantity=1,
                    unit_price=drink.sale_price,
                )
            ],
        )
        created_purchase = self.create_purchase(purchase)

        for recipe_item in drink.recipe:
            self._ingredient_service.deduct_ingredient_amount(
                recipe_item.ingredient_id, recipe_item.quantity
            )

        return created_purchase

    def update_purchase(self, purchase_id: int, purchase: Purchase) -> Purchase | None:
        if self._repository.get_by_id(purchase_id) is None:
            raise ValueError("Purchase does not exist.")

        purchase.id = purchase_id
        self._validate_purchase(purchase)
        purchase.total_cost = self._calculate_total_cost(purchase)
        purchase.timestamp = self._normalize_timestamp(purchase.timestamp)

        updated_purchase = self._repository.update(purchase_id, purchase)
        if updated_purchase is not None and self._customer_service is not None:
            record_purchase = getattr(self._customer_service, "record_purchase", None)
            if callable(record_purchase):
                record_purchase(purchase.customer_id, updated_purchase.total_cost)

        return updated_purchase

    def delete_purchase(self, purchase_id: int) -> bool:
        return self._repository.delete(purchase_id)

    def _validate_purchase(self, purchase: Purchase) -> None:
        if purchase.customer_id is None:
            raise ValueError("Customer ID is required.")
        if not purchase.items:
            raise ValueError("Purchase must include at least one item.")
<<<<<<< HEAD
        if not purchase.timestamp:
=======
        if purchase.timestamp is None:
>>>>>>> db0df7b52156e5c8a98888086b7e9c8250f3d3e0
            purchase.timestamp = datetime.now(timezone.utc)
        else:
            validate_purchase_timestamp_utc(purchase.timestamp)

        self._validate_customer_exists(purchase.customer_id)

        for item in purchase.items:
            if item.item_id is None:
                raise ValueError("Each purchase item must reference a valid item ID.")
            if item.quantity <= 0:
                raise ValueError("Item quantity must be greater than zero.")
            if item.item_type not in {"drink", "baked_good"}:
                raise ValueError("Item type must be 'drink' or 'baked_good'.")

            item.unit_price = self._get_current_item_price(item)

    def _calculate_total_cost(self, purchase: Purchase) -> Decimal:
        total_cost = Decimal("0.00")
        for item in purchase.items:
            total_cost += Decimal(item.quantity) * item.unit_price
        return total_cost.quantize(Decimal("0.01"))

    def _normalize_timestamp(self, timestamp: datetime) -> datetime:
        if timestamp.tzinfo is None:
            raise ValueError("Timestamp must be in UTC format.")
        validate_purchase_timestamp_utc(timestamp)
        return timestamp.astimezone(timezone.utc)

    def _validate_customer_exists(self, customer_id: int) -> None:
        if self._customer_service is None:
            raise ValueError("Customer service is required.")

        get_customer_method = getattr(
            self._customer_service, "get_customer_by_id", None
        )
        if get_customer_method is None:
            get_customer_method = getattr(self._customer_service, "get_by_id", None)

        if get_customer_method is None:
            raise ValueError("Customer service does not support customer lookup.")

        if get_customer_method(customer_id) is None:
            raise ValueError("Customer does not exist.")

    def _validate_customer_lifetime_spent(self, customer_id: int):
        purchases = self.get_all()
        purchase_totals: list[Decimal] = [
            purchase.total_cost
            for purchase in purchases
            if purchase.customer_id == customer_id
        ]
        calculated_lifetime_spent = sum(purchase_totals)

        assert self._customer_service is not None
        customer = self._customer_service.get_customer(customer_id)
        if customer.lifetime_spent != calculated_lifetime_spent:
            raise CustomerLifetimeSpentIsIncorrectError(
                f"Customer by id '{customer_id}' lifetime spent is incorrect."
            )

    def _get_current_item_price(self, item: PurchaseItem):
        if item.item_type == "drink":
            if self._drink_service is None:
                raise ValueError("Drink service is required to price a drink purchase.")

            get_drink_method = getattr(self._drink_service, "get_drink_by_id", None)
            if get_drink_method is None:
                get_drink_method = getattr(self._drink_service, "get_by_id", None)

            if get_drink_method is None:
                raise ValueError("Drink service does not support drink lookup.")

            drink = get_drink_method(item.item_id)
            if drink is None:
                raise ValueError("Drink does not exist.")
            return drink.sale_price

        if item.item_type == "baked_good":
            if self._baked_good_service is None:
                raise ValueError(
                    "Baked good service is required to price a baked good purchase."
                )

            get_baked_good_method = getattr(
                self._baked_good_service, "get_baked_good_by_id", None
            )
            if get_baked_good_method is None:
                get_baked_good_method = getattr(
                    self._baked_good_service, "get_by_id", None
                )

            if get_baked_good_method is None:
                raise ValueError(
                    "Baked good service does not support baked good lookup."
                )

            baked_good = get_baked_good_method(item.item_id)
            if baked_good is None:
                raise ValueError("Baked good does not exist.")
            return baked_good.sale_price

        raise ValueError("Item type must be 'drink' or 'baked_good'.")
