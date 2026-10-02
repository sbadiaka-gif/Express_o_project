"""Customer service."""

from src.models.customer import Customer
from src.repositories.customer_repository import CustomerRepository
from decimal import Decimal


class CustomerService:
    def __init__(self, repository: CustomerRepository):
        self._repository = repository

    def create_customer(self, customer: Customer):
        pass

    def update_customer_name(self, id: int, new_name: str):
        pass

    def update_customer_email(self, id: int, email: str):
        pass

    def update_customer_lifetime_spent(self, id: int, new_lifetime_spent: Decimal):
        pass

    def get_customers(self):
        pass

    def get_customer(self, id: int):
        pass

    def remove_customer(self, id: int):
        pass
