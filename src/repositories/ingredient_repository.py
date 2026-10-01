"""Ingredient repository."""
from src.models.ingredient import Ingredient
from copy import deepcopy

class IngredientRepository:
    def __init__(self):
        self._ingredients: list[Ingredient] = []
        self._next_id: int = 1

    def add(self, ingredient: Ingredient) -> Ingredient:
        ingredient.id = self._next_id
        self._next_id += 1
        self._ingredients.append(deepcopy(ingredient))
        return ingredient
    def get_by_id(self, ingredient_id: int) -> Ingredient | None:
        for ingredient in self._ingredients:
            if ingredient.id == ingredient_id:
                return deepcopy(ingredient)
        return None
    def get_all(self) -> list[Ingredient]:
        return deepcopy(self._ingredients)
    
    def update(self, updated_ingredient: Ingredient) -> None:
        for index, ingredient in enumerate(self._ingredients):
            if ingredient.id == updated_ingredient.id:
                self._ingredients[index] = deepcopy(updated_ingredient)
                return updated_ingredient
        return None
    def delete(self, ingredient_id: int) -> bool:
        for index, ingredient in enumerate(self._ingredients):
            if ingredient.id == ingredient_id:
                del self._ingredients[index]
                return True
        return False
