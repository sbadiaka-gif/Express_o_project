"""Drink repository."""
from src.models.drink import Drink
from copy import deepcopy

class DrinkRepository:
    def __init__(self):
        self._drinks: list[Drink] = []
        self._next_id: int = 1

    def add(self, drink: Drink) -> Drink:
        drink.id = self._next_id
        self._next_id += 1
        self._drinks.append(deepcopy(drink))
        return drink

    def get_by_id(self, drink_id: int) -> Drink | None:
        for drink in self._drinks:
            if drink.id == drink_id:
                return deepcopy(drink)
        return None

    def get_all(self) -> list[Drink]:
        return deepcopy(self._drinks)

    def update(self, updated_drink: Drink) -> Drink | None:
        for index, drink in enumerate(self._drinks):
            if drink.id == updated_drink.id:
                self._drinks[index] = deepcopy(updated_drink)
                return updated_drink
        return None

    def delete(self, drink_id: int) -> bool:
        for index, drink in enumerate(self._drinks):
            if drink.id == drink_id:
                del self._drinks[index]
                return True
        return False