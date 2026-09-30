"""Ingredient repository."""
from src.models.ingredient import Ingredient

class IngredientRepository:
    def __init__(self):
        self._ingredients: list[Ingredient] = []
        self._next_id: int = 1

    def add_ingredient(self, ingredient: Ingredient) -> Ingredient:
        ingredient.id = self._next_id
        self._next_id += 1
        self._ingredients.append(ingredient)
        return ingredient
    def get_ingredient_by_id(self, ingredient_id: int) -> Ingredient | None:
        for ingredient in self._ingredients:
            if ingredient.id == ingredient_id:
                return ingredient
        return None
    def get_all_ingredients(self) -> list[Ingredient]:
        return list(self._ingredients)
    
    def update_ingredient(self, updated_ingredient: Ingredient) -> bool:
        for index, ingredient in enumerate(self._ingredients):
            if ingredient.id == updated_ingredient.id:
                self._ingredients[index] = updated_ingredient
                return True
        return False
    def delete_ingredient(self, ingredient_id: int) -> bool:
        for index, ingredient in enumerate(self._ingredients):
            if ingredient.id == ingredient_id:
                del self._ingredients[index]
                return True
        return False