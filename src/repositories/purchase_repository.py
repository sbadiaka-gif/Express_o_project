"""Purchase repository."""

import copy
from src.models.purchase import Purchase


class PurchaseRepository:
    def __init__(self):
        self._purchases: list[Purchase] = []
        self._next_id: int = 1

    def get_all(self) -> list[Purchase]:
        return copy.deepcopy(self._purchases)

    def get_by_id(self, purchase_id: int) -> Purchase | None:
        for purchase in self._purchases:
            if purchase.id == purchase_id:
                return copy.deepcopy(purchase)
        return None

    def add(self, purchase: Purchase) -> Purchase:
        purchase.id = self._next_id
        self._next_id += 1
        self._purchases.append(copy.deepcopy(purchase))
        return purchase

    def update(self, purchase_id: int, purchase: Purchase) -> Purchase | None:
        for index, existing_purchase in enumerate(self._purchases):
            if existing_purchase.id == purchase_id:
                purchase.id = purchase_id
                self._purchases[index] = copy.deepcopy(purchase)
                return purchase
        return None

    def delete(self, purchase_id: int) -> bool:
        for index, purchase in enumerate(self._purchases):
            if purchase.id == purchase_id:
                del self._purchases[index]
                return True
        return False
