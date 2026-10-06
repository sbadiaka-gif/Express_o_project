"""Ingredient repository."""

# CHANGED: import ordering kept consistent with the project package structure.
from src.models.ingredient import Ingredient
from copy import deepcopy
from repository import Repository


class IngredientRepository(Repository[Ingredient]):
    def __init__(self):
        self._ingredients: list[Ingredient] = []
        self._next_id: int = 1

    # CHANGED: add assigns a new id automatically and appends a deep copy of the ingredient.
    def add(self, item: Ingredient) -> Ingredient:
        item.id = self._next_id
        self._next_id += 1
        self._ingredients.append(deepcopy(item))
        return item

    # CHANGED: get_by_id searches the id and returns a copied ingredient to prevent raw mutation.
    def get_by_id(self, id: int) -> Ingredient | None:
        for ingredient in self._ingredients:
            if ingredient.id == id:
                return deepcopy(ingredient)
        return None

    # CHANGED: get_all now returns a copied list so external code cannot edit storage directly.
    def get_all(self) -> list[Ingredient]:
        return deepcopy(self._ingredients)

    # CHANGED: update replaces the matching ingredient while preserving the repository contract.
    def update(self, id: int, updated_item: Ingredient) -> Ingredient | None:
        for index, ingredient in enumerate(self._ingredients):
            if ingredient.id == id:
                self._ingredients[index] = deepcopy(updated_item)
                return updated_item
        return None

    # CHANGED: delete removes the ingredient by id and returns False if it is not present.
    def delete(self, id: int) -> bool:
        for index, ingredient in enumerate(self._ingredients):
            if ingredient.id == id:
                del self._ingredients[index]
                return True
        return False
