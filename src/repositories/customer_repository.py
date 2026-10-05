from src.models.customer import Customer
from copy import deepcopy


class CustomerRepository:
    def __init__(self):
        self._customers: list[Customer] = []
        self._next_id: int = 1

    def add(self, customer: Customer) -> Customer:
        """Add a new customer to the data."""
        customer.id = self._next_id
        self._next_id += 1
        self._customers.append(deepcopy(customer))
        return customer

    def get_by_id(self, id: int) -> Customer | None:
        """Get a customer with the id."""
        for customer in self._customers:
            if customer.id == id:
                return deepcopy(customer)

        return None

    def get_all(self) -> list[Customer]:
        """Get the list of customer."""
        return deepcopy(self._customers)

    def update(self, id: int, updated_customer: Customer) -> Customer | None:
        """Replace a customer with the id."""
        for index, customer in enumerate(self._customers):
            if customer.id == id:
                self._customers[index] = deepcopy(updated_customer)
                return updated_customer

        return None

    def delete(self, id: int) -> bool:
        """Remove a customer with the id."""
        for index, customer in enumerate(self._customers):
            if customer.id == id:
                del self._customers[index]
                return True

        return False
