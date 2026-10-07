from decimal import Decimal
from datetime import datetime, timezone
import pytest

from src.exceptions import InsufficientStockError
from src.models.drink import Drink
from src.models.ingredient import Ingredient
from src.models.recipe_item import RecipeItem
from src.repositories.customer_repository import CustomerRepository
from src.repositories.drink_repository import DrinkRepository
from src.repositories.ingredient_repository import IngredientRepository
from src.repositories.purchase_repository import PurchaseRepository
from src.services.customer_service import CustomerService
from src.services.drink_service import DrinkService
from src.services.ingredient_service import IngredientService
from src.services.purchase_service import PurchaseService
from src.models.customer import Customer
from src.models.purchase import Purchase
from src.models.purchase_item import PurchaseItem


class FakeCustomerService:
    def __init__(self):
        self.customer = Customer(name="Alice", email="alice@example.com")
        self.recorded = []

    def get_customer_by_id(self, customer_id):
        return self.customer if customer_id == 1 else None

    def record_purchase(self, customer_id, amount):
        self.recorded.append((customer_id, amount))


class FakeDrinkService:
    def __init__(self):
        self.drink = Drink(
            name="Latte", markup_percentage=Decimal("0.20"), sale_price=Decimal("5.00")
        )

    def get_drink_by_id(self, drink_id):
        return self.drink if drink_id == 7 else None


class FakeBakedGoodService:
    def __init__(self):
        self.item = None

    def get_baked_good_by_id(self, baked_good_id):
        return self.item if baked_good_id == 8 else None


def test_create_purchase_sets_total_and_records_customer_spend():
    customer_service = FakeCustomerService()
    drink_service = FakeDrinkService()
    baked_good_service = FakeBakedGoodService()
    repository = PurchaseRepository()
    service = PurchaseService(
        repository, customer_service, drink_service, baked_good_service
    )

    purchase = Purchase(
        customer_id=1,
        items=[
            PurchaseItem(
                item_type="drink", item_id=7, quantity=2, unit_price=Decimal("0.00")
            ),
        ],
        timestamp=datetime.now(timezone.utc),
    )

    created = service.create_purchase(purchase)

    assert created.total_cost == Decimal("10.00")
    assert created.items[0].unit_price == Decimal("5.00")
    assert customer_service.recorded == [(1, Decimal("10.00"))]
    assert created.id == 1


@pytest.fixture
def shop():
    ingredient_repo = IngredientRepository()
    ingredient_service = IngredientService(ingredient_repo)
    drink_service = DrinkService(DrinkRepository(), ingredient_service)
    customer_service = CustomerService(CustomerRepository())
    purchase_service = PurchaseService(
        PurchaseRepository(),
        customer_service=customer_service,
        drink_service=drink_service,
        ingredient_service=ingredient_service,
    )

    milk = ingredient_service.add_ingredient(
        Ingredient(
            name="Milk",
            purchasing_cost=Decimal("1.00"),
            unit_amount=Decimal("10.00"),
            unit_of_measure="kg",
        )
    )
    drink = drink_service.add_drink(
        Drink(
            name="Latte",
            recipe=[RecipeItem(ingredient_id=milk.id, quantity=Decimal("2.00"))],
            markup_percentage=Decimal("0.50"),
            cost_to_produce=Decimal("2.00"),
            sale_price=Decimal("3.00"),
        )
    )
    return {
        "purchases": purchase_service,
        "ingredients": ingredient_repo,
        "customers": customer_service,
        "milk_id": milk.id,
        "drink_id": drink.id,
    }


class TestPurchaseADrink:
    def test_records_sale_and_deducts_stock(self, shop):
        purchase = shop["purchases"].purchase_a_drink(
            "Maria", "maria@example.com", shop["drink_id"]
        )

        assert purchase.total_cost == Decimal("3.00")
        assert shop["ingredients"].get_by_id(shop["milk_id"]).unit_amount == Decimal(
            "8.00"
        )
        assert shop["customers"].get_by_email(
            "maria@example.com"
        ).lifetime_spent == Decimal("3.00")

    def test_reuses_returning_customer(self, shop):
        shop["purchases"].purchase_a_drink(
            "Maria", "maria@example.com", shop["drink_id"]
        )
        shop["purchases"].purchase_a_drink(
            "Maria", "maria@example.com", shop["drink_id"]
        )

        assert len(shop["customers"].get_customers()) == 1
        assert shop["customers"].get_by_email(
            "maria@example.com"
        ).lifetime_spent == Decimal("6.00")

    def test_insufficient_stock_changes_nothing(self, shop):
        for _ in range(5):  # 5 lattes use all 10 milk
            shop["purchases"].purchase_a_drink(
                "Maria", "maria@example.com", shop["drink_id"]
            )

        with pytest.raises(InsufficientStockError):
            shop["purchases"].purchase_a_drink(
                "Maria", "maria@example.com", shop["drink_id"]
            )

        assert shop["ingredients"].get_by_id(shop["milk_id"]).unit_amount == Decimal(
            "0.00"
        )

    def test_unknown_drink_raises(self, shop):
        with pytest.raises(ValueError):
            shop["purchases"].purchase_a_drink("Maria", "maria@example.com", 999)
