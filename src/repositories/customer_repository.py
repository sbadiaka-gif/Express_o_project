from src.models.customer import Customer
from copy import deepcopy
from src.repositories.repository import Repository


class CustomerRepository(Repository[Customer]):
    def __init__(self):
        self._customers: list[Customer] = []
        self._next_id: int = 1

    def add(self, item: Customer) -> Customer:
        """Add a new customer to the data."""
        item.id = self._next_id
        self._next_id += 1
        self._customers.append(deepcopy(item))
        return item

    def get_by_id(self, id: int) -> Customer | None:
        """Get a customer with the id."""
        for customer in self._customers:
            if customer.id == id:
                return deepcopy(customer)
        return None

    def get_all(self) -> list[Customer]:
        """Get the list of customer."""
        return deepcopy(self._customers)

    def update(self, id: int, updated_item: Customer) -> Customer | None:
        """Replace a customer with the id."""
        for index, customer in enumerate(self._customers):
            if customer.id == id:
                self._customers[index] = deepcopy(updated_item)
                return updated_item
        return None

    def delete(self, id: int) -> bool:
        """Remove a customer with the id."""
        for index, customer in enumerate(self._customers):
            if customer.id == id:
                del self._customers[index]
                return True
        return False

