"""Purchase repository."""

# CHANGED: import kept consistent with project style and repository behavior is documented inline.
import copy
from src.models.purchase import Purchase
from repository import Repository


class PurchaseRepository(Repository[Purchase]):
    def __init__(self):
        self._purchases: list[Purchase] = []
        self._next_id: int = 1

    # CHANGED: get_all returns a deep copy so outside code cannot overwrite stored purchase data.
    def get_all(self) -> list[Purchase]:
        return copy.deepcopy(self._purchases)

    # CHANGED: get_by_id searches by purchase id and returns a copied object for safety.
    def get_by_id(self, id: int) -> Purchase | None:
        for purchase in self._purchases:
            if purchase.id == id:
                return copy.deepcopy(purchase)
        return None

    # CHANGED: add assigns the next available id before storing the record.
    def add(self, item: Purchase) -> Purchase:
        item.id = self._next_id
        self._next_id += 1
        self._purchases.append(copy.deepcopy(item))
        return item

    # CHANGED: update replaces the object stored under the matching purchase id.
    def update(self, id: int, updated_item: Purchase) -> Purchase | None:
        for index, existing_purchase in enumerate(self._purchases):
            if existing_purchase.id == id:
                updated_item.id = id
                self._purchases[index] = copy.deepcopy(updated_item)
                return updated_item
        return None

    # CHANGED: delete removes the matching purchase and returns True only when found.
    def delete(self, id: int) -> bool:
        for index, purchase in enumerate(self._purchases):
            if purchase.id == id:
                del self._purchases[index]
                return True
        return False
