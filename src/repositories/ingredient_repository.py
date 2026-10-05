"""Ingredient repository."""

# CHANGED: import ordering kept consistent with the project package structure.
from src.models.ingredient import Ingredient
from copy import deepcopy


class IngredientRepository:
    def __init__(self):
        self._ingredients: list[Ingredient] = []
        self._next_id: int = 1

    # CHANGED: add assigns a new id automatically and appends a deep copy of the ingredient.
    def add(self, ingredient: Ingredient) -> Ingredient:
        ingredient.id = self._next_id
        self._next_id += 1
        self._ingredients.append(deepcopy(ingredient))
        return ingredient

    # CHANGED: get_by_id searches the id and returns a copied ingredient to prevent raw mutation.
    def get_by_id(self, ingredient_id: int) -> Ingredient | None:
        for ingredient in self._ingredients:
            if ingredient.id == ingredient_id:
                return deepcopy(ingredient)
        return None

    # CHANGED: get_all now returns a copied list so external code cannot edit storage directly.
    def get_all(self) -> list[Ingredient]:
        return deepcopy(self._ingredients)

    # CHANGED: update replaces the matching ingredient while preserving the repository contract.
    def update(self, updated_ingredient: Ingredient) -> Ingredient | None:
        for index, ingredient in enumerate(self._ingredients):
            if ingredient.id == updated_ingredient.id:
                self._ingredients[index] = deepcopy(updated_ingredient)
                return updated_ingredient
        return None

    # CHANGED: delete removes the ingredient by id and returns False if it is not present.
    def delete(self, ingredient_id: int) -> bool:
        for index, ingredient in enumerate(self._ingredients):
            if ingredient.id == ingredient_id:
                del self._ingredients[index]
                return True
        return False
