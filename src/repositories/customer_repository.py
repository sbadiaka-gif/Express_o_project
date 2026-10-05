"""Customer repository."""

# CHANGED: repository imports kept in a project-structured format and are documented for clarity.
from src.models.customer import Customer
from copy import deepcopy
from repository import Repository


class CustomerRepository(Repository[Customer]):
    def __init__(self):
        self._customers: list[Customer] = []
        self._next_id: int = 1

    # CHANGED: repository assigns the next id and stores a deep copy to keep the in-memory list safe.
    def add(self, item: Customer) -> Customer:
        item.id = self._next_id
        self._next_id += 1
        self._customers.append(deepcopy(item))
        return item

    # CHANGED: lookup is done by id and returns a deep copy to avoid direct mutation of stored objects.
    def get_by_id(self, id: int) -> Customer | None:
        for Customer in self._customers:
            if Customer.id == id:
                return deepcopy(Customer)
        return None

    # CHANGED: get_all returns a copied list so callers cannot change repository storage accidentally.
    def get_all(self) -> list[Customer]:
        return deepcopy(self._customers)

    # CHANGED: update replaces the object at the matching id and keeps repository data consistent.
    def update(self, id: int, updated_item: Customer) -> Customer | None:
        for index, customer in enumerate(self._customers):
            if customer.id == id:
                self._customers[index] = deepcopy(updated_item)
                return updated_item
        return None

    # CHANGED: delete removes the matching record and returns False if it is not found.
    def delete(self, id: int) -> bool:
        for index, customer in enumerate(self._customers):
            if customer.id == id:
                del self._customers[index]
                return True
        return False
