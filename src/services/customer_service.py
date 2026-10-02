"""Customer service."""

from src.models.customer import Customer
from src.repositories.customer_repository import CustomerRepository


class CustomerService:
    def __init__(self, repository: CustomerRepository):
        self._repository = repository

    def create_customer(self, customer: Customer):
        pass
