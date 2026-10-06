"""Customer service."""

# Original version used bare imports and did not allow an update to keep the same email address. The new version
# uses the project package imports and ignores the current customer when checking email uniqueness.

from decimal import Decimal
from typing import cast

# CHANGED: package imports fixed to use `src.*` so the code runs from the project root.
from src.exceptions import (
    CustomerDuplicateEmailError,
    CustomerNotFoundError,
    CustomerLifetimeSpentIsIncorrectError,
)
from src.models.customer import Customer
from src.repositories.customer_repository import CustomerRepository
from src.validators import (
    validate_email,
    validate_money_decimal_positive_two_decimal_places,
    validate_name_not_empty,
)
from src.services.purchase_service import PurchaseService


class CustomerService:
    def __init__(
        self, repository: CustomerRepository, purchase_service: PurchaseService
    ):
        self._repository = repository
        self._purchase_service = purchase_service

    def create_customer(self, customer: Customer) -> Customer:
        self.validate_customer(customer)
        self.validate_email_unique(customer.email)

        customer.lifetime_spent = Decimal("0.00")

        return self._repository.add(customer)

    # CHANGED: added `customer_id` to email uniqueness check so updating the same customer does not fail.
    def update_customer(self, id: int, customer: Customer) -> Customer:
        self.validate_customer_exists(id)
        self.validate_customer(customer)
        self.validate_email_unique(customer.email, id)
        self.validate_customer_lifetime_spent(id, customer.lifetime_spent)
        return cast(Customer, self._repository.update(id, customer))

    def get_customers(self) -> list[Customer]:
        return self._repository.get_all()

    def get_customer(self, id: int) -> Customer:
        self.validate_customer_exists(id)
        return cast(Customer, self._repository.get_by_id(id))

    # CHANGED: added a direct lookup method so PurchaseService can inject this service cleanly.
    def get_customer_by_id(self, customer_id: int) -> Customer | None:
        return self._repository.get_by_id(customer_id)

    def get_customer_name(self, id: int) -> str:
        return self.get_customer(id).name

    def remove_customer(self, id: int):
        self.validate_customer_exists(id)
        self._repository.delete(id)

    # CHANGED: method added so a purchase can update the customer's lifetime spend after saving.
    def record_purchase(self, customer_id: int, total_cost: Decimal) -> Customer:
        customer = self._repository.get_by_id(customer_id)
        if customer is None:
            raise CustomerNotFoundError(f"Customer by id '{customer_id}' not found.")
        customer.lifetime_spent += total_cost
        updated_customer = self._repository.update(customer_id, customer)
        return cast(Customer, updated_customer)

    def validate_customer(self, customer: Customer):
        validate_name_not_empty(customer.name, "name")
        validate_email(customer.email)
        validate_money_decimal_positive_two_decimal_places(
            customer.lifetime_spent, "lifetime_spent"
        )

    def validate_customer_exists(self, customer_id: int):
        customer = self._repository.get_by_id(customer_id)
        if customer is None:
            raise CustomerNotFoundError(f"Customer by id '{customer_id}' not found.")

    def validate_customer_lifetime_spent(
        self, customer_id: int, lifetime_spent: Decimal
    ):
        purchases = self._purchase_service.get_all()
        purchase_totals: list[Decimal] = [
            purchase.total_cost
            for purchase in purchases
            if purchase.customer_id == customer_id
        ]
        calculated_lifetime_spent = sum(purchase_totals)

        if lifetime_spent != calculated_lifetime_spent:
            raise CustomerLifetimeSpentIsIncorrectError(
                f"Customer by id '{customer_id}' lifetime spent is incorrect."
            )

    # CHANGED: customer_id was added so the current customer is excluded from the duplicate-email check.
    def validate_email_unique(self, email: str, customer_id: int | None = None):
        """Validate that an email address is unique in the customer repository."""
        existing_customers = self._repository.get_all()
        for customer in existing_customers:
            if customer.email == email and customer.id != customer_id:
                raise CustomerDuplicateEmailError("Email address must be unique.")
