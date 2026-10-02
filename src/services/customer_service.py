"""Customer service."""

from src.models.customer import Customer
from src.repositories.customer_repository import CustomerRepository
from validators import (
    validate_email,
    validate_name_not_empty,
    validate_money_decimal_positive_two_decimal_places,
)
from exceptions import CustomerDuplicateEmailError, CustomerNotFoundError
from typing import cast


class CustomerService:
    def __init__(self, repository: CustomerRepository):
        self._repository = repository

    def create_customer(self, customer: Customer) -> Customer:
        self.validate_customer(customer)
        self.validate_email_unique(customer.email)

        return self._repository.add(customer)

    def update_customer(self, id: int, customer: Customer) -> Customer:
        self.validate_customer_exists(id)
        self.validate_customer(customer)
        self.validate_email_unique(customer.email)

        return cast(Customer, self._repository.update(id, customer))

    def get_customers(self) -> list[Customer]:
        return self._repository.get_all()

    def get_customer(self, id: int) -> Customer:
        self.validate_customer_exists(id)
        return cast(Customer, self._repository.get_by_id(id))

    def get_customer_name(self, id: int) -> str:
        return self.get_customer(id).name

    def remove_customer(self, id: int):
        self.validate_customer_exists(id)
        self._repository.delete(id)

    def validate_customer(self, customer: Customer):
        validate_name_not_empty(customer.name, "name")
        validate_email(customer.email)
        validate_money_decimal_positive_two_decimal_places(
            customer.lifetime_spent, "lifetime_spent"
        )

    def validate_customer_exists(self, id: int):
        customer = self._repository.get_by_id(id)
        if customer == None:
            raise CustomerNotFoundError(f"Customer by id '{int}' not found.")

    def validate_email_unique(self, email: str):
        """Validate that an email address is unique in the customer repository."""
        existing_customers = self._repository.get_all()
        for customer in existing_customers:
            if customer.email == email:
                raise CustomerDuplicateEmailError("Email address must be unique.")
