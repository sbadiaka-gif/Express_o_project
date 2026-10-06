from decimal import Decimal
from typing import cast

from src.exceptions import CustomerDuplicateEmailError, CustomerNotFoundError
from src.models.customer import Customer
from src.repositories.customer_repository import CustomerRepository
from src.validators import (
    validate_email,
    validate_money_decimal_positive_two_decimal_places,
    validate_name_not_empty,
)


class CustomerService:
    def __init__(self, repository: CustomerRepository):
        self._repository = repository

    def create_customer(self, customer: Customer) -> Customer:
        self._validate_customer(customer)
        self._validate_email_unique(customer.email)

        customer.lifetime_spent = Decimal("0.00")

        return self._repository.add(customer)

    def get_by_email(self, email: str) -> Customer | None:
        for customer in self._repository.get_all():
            if customer.email == email:
                return customer
        return None

    def get_customers(self) -> list[Customer]:
        return self._repository.get_all()

    def get_customer(self, id: int) -> Customer:
        self._validate_customer_exists(id)
        return cast(Customer, self._repository.get_by_id(id))

    def get_customer_by_id(self, customer_id: int) -> Customer | None:
        return self._repository.get_by_id(customer_id)

    def get_customer_name(self, id: int) -> str:
        return self.get_customer(id).name

    def update_customer(self, id: int, customer: Customer) -> Customer:
        self._validate_customer_exists(id)
        self._validate_customer(customer)
        self._validate_email_unique(customer.email, id)
        return cast(Customer, self._repository.update(id, customer))

    def remove_customer(self, id: int):
        self._validate_customer_exists(id)
        self._repository.delete(id)

    def record_purchase(self, customer_id: int, total_cost: Decimal) -> Customer:
        customer = self._repository.get_by_id(customer_id)
        if customer is None:
            raise CustomerNotFoundError(f"Customer by id '{customer_id}' not found.")
        customer.lifetime_spent += total_cost
        updated_customer = self._repository.update(customer_id, customer)
        return cast(Customer, updated_customer)

    def _validate_customer(self, customer: Customer):
        validate_name_not_empty(customer.name, "name")
        validate_email(customer.email)
        validate_money_decimal_positive_two_decimal_places(
            customer.lifetime_spent, "lifetime_spent"
        )

    def _validate_customer_exists(self, customer_id: int):
        customer = self._repository.get_by_id(customer_id)
        if customer is None:
            raise CustomerNotFoundError(f"Customer by id '{customer_id}' not found.")

    def _validate_email_unique(self, email: str, customer_id: int | None = None):
        """Validate that an email address is unique in the customer repository."""
        existing_customers = self._repository.get_all()
        for customer in existing_customers:
            if customer.email == email and customer.id != customer_id:
                raise CustomerDuplicateEmailError("Email address must be unique.")
