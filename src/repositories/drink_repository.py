"""Drink repository."""

# CHANGED: repository layout remains consistent with the project pattern and keeps item storage isolated.
from src.models.drink import Drink
from copy import deepcopy


class DrinkRepository:
    def __init__(self):
        self._drinks: list[Drink] = []
        self._next_id: int = 1

    # CHANGED: add assigns the next id and stores a deep copy to protect the backing list.
    def add(self, drink: Drink) -> Drink:
        drink.id = self._next_id
        self._next_id += 1
        self._drinks.append(deepcopy(drink))
        return drink

    # CHANGED: lookup finds the matching drink id and returns a safe copied object.
    def get_by_id(self, drink_id: int) -> Drink | None:
        for drink in self._drinks:
            if drink.id == drink_id:
                return deepcopy(drink)
        return None

    # CHANGED: get_all returns a copy so the raw storage cannot be mutated by outside code.
    def get_all(self) -> list[Drink]:
        return deepcopy(self._drinks)

    # CHANGED: update matches on the drink id and replaces the stored object in place.
    def update(self, updated_drink: Drink) -> Drink | None:
        for index, drink in enumerate(self._drinks):
            if drink.id == updated_drink.id:
                self._drinks[index] = deepcopy(updated_drink)
                return updated_drink
        return None

    # CHANGED: delete removes the matching record and returns True only when found.
    def delete(self, drink_id: int) -> bool:
        for index, drink in enumerate(self._drinks):
            if drink.id == drink_id:
                del self._drinks[index]
                return True
        return False
