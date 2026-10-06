"""Drink repository."""

from src.models.drink import Drink
from copy import deepcopy
from repository import Repository


class DrinkRepository(Repository[Drink]):
    def __init__(self):
        self._drinks: list[Drink] = []
        self._next_id: int = 1

    def add(self, item: Drink) -> Drink:
        item.id = self._next_id
        self._next_id += 1
        self._drinks.append(deepcopy(item))
        return item

    def get_by_id(self, id: int) -> Drink | None:
        for drink in self._drinks:
            if drink.id == id:
                return deepcopy(drink)
        return None

    def get_all(self) -> list[Drink]:
        return deepcopy(self._drinks)

    def update(self, id: int, updated_item: Drink) -> Drink | None:
        for index, drink in enumerate(self._drinks):
            if drink.id == id:
                self._drinks[index] = deepcopy(updated_item)
                return updated_item
        return None

    def delete(self, id: int) -> bool:
        for index, drink in enumerate(self._drinks):
            if drink.id == id:
                del self._drinks[index]
                return True
        return False
