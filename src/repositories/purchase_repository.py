"""Purchase repository."""

# CHANGED: import kept consistent with project style and repository behavior is documented inline.
import copy
from src.models.purchase import Purchase


class PurchaseRepository:
    def __init__(self):
        self._purchases: list[Purchase] = []
        self._next_id: int = 1

    # CHANGED: get_all returns a deep copy so outside code cannot overwrite stored purchase data.
    def get_all(self) -> list[Purchase]:
        return copy.deepcopy(self._purchases)

    # CHANGED: get_by_id searches by purchase id and returns a copied object for safety.
    def get_by_id(self, purchase_id: int) -> Purchase | None:
        for purchase in self._purchases:
            if purchase.id == purchase_id:
                return copy.deepcopy(purchase)
        return None

    # CHANGED: add assigns the next available id before storing the record.
    def add(self, purchase: Purchase) -> Purchase:
        purchase.id = self._next_id
        self._next_id += 1
        self._purchases.append(copy.deepcopy(purchase))
        return purchase

    # CHANGED: update replaces the object stored under the matching purchase id.
    def update(self, purchase_id: int, purchase: Purchase) -> Purchase | None:
        for index, existing_purchase in enumerate(self._purchases):
            if existing_purchase.id == purchase_id:
                purchase.id = purchase_id
                self._purchases[index] = copy.deepcopy(purchase)
                return purchase
        return None

    # CHANGED: delete removes the matching purchase and returns True only when found.
    def delete(self, purchase_id: int) -> bool:
        for index, purchase in enumerate(self._purchases):
            if purchase.id == purchase_id:
                del self._purchases[index]
                return True
        return False
