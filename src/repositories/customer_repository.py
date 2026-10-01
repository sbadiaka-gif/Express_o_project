"""Customer repository."""

from src.models.customer import Customer
from copy import deepcopy


class CustomerRepository:
    def __init__(self):
        self._customers: list[Customer] = []
        self._next_id: int = 1

    def add(self, customer: Customer) -> Customer:
        customer.id = self._next_id
        self._next_id += 1
        self._customers.append(deepcopy(customer))
        return customer

    def get_by_id(self, customer_id: int) -> Customer | None:
        for Customer in self._customers:
            if Customer.id == customer_id:
                return deepcopy(Customer)

        return None

    def get_all(self) -> list[Customer]:
        return deepcopy(self._customers)

    def update(self, customer_id: int, updated_customer: Customer) -> Customer | None:
        for index, customer in enumerate(self._customers):
            if customer.id == customer_id:
                self._customers[index] = deepcopy(updated_customer)
                return updated_customer

        return None

    def delete(self, customer_id: int) -> bool:
        for index, customer in enumerate(self._customers):
            if customer.id == customer_id:
                del self._customers[index]
                return True

        return False
