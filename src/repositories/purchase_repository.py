"""Purchase repository."""

from src.models.purchase import Purchase


class PurchaseRepository:
    def __init__(self):
        self._purchases: list[Purchase] = []
        self._next_id: int = 1

    def get_all(self) -> list[Purchase]:
        return list(self._purchases)

    def get_by_id(self, purchase_id: int) -> Purchase | None:
        for purchase in self._purchases:
            if purchase.id == purchase_id:
                return purchase
        return None

    def add(self, purchase: Purchase) -> Purchase:
        purchase.id = self._next_id
        self._next_id += 1
        self._purchases.append(purchase)
        return purchase

    def update(self, purchase_id: int, purchase: Purchase) -> Purchase | None:
        for index, existing_purchase in enumerate(self._purchases):
            if existing_purchase.id == purchase_id:
                purchase.id = purchase_id
                self._purchases[index] = purchase
                return purchase
        return None

    def delete(self, purchase_id: int) -> bool:
        for index, purchase in enumerate(self._purchases):
            if purchase.id == purchase_id:
                del self._purchases[index]
                return True
        return False
