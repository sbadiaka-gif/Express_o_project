"""Ingredient service."""
from decimal import Decimal
from validators import validate_record_exists, validate_money_decimal_positive_two_decimal_places
from src.repositories.ingredient_repository import IngredientRepository
from exceptions import  InsufficientStockError


class IngredientService:
    def __init__(self, ingredient_repository: IngredientRepository):
        self.ingredient_repository = ingredient_repository

    def restock_ingredient(self, ingredient_id, amount: Decimal) -> None:
        """Restock an ingredient by increasing its unit_amount."""
        validate_record_exists(self.ingredient_repository, ingredient_id, "Ingredient")
        validate_money_decimal_positive_two_decimal_places(amount, "Amount")

        ingredient = self.ingredient_repository.get_by_id(ingredient_id)
        ingredient.unit_amount += amount
        self.ingredient_repository.update(ingredient)

    def is_ingredient_amount_sufficient(self, ingredient_id, required_amount: Decimal) -> bool:
        """Check if the ingredient's unit_amount is sufficient for the required amount."""
        validate_record_exists(self.ingredient_repository, ingredient_id, "Ingredient")
        validate_money_decimal_positive_two_decimal_places(required_amount, "Required Amount")

        ingredient = self.ingredient_repository.get_by_id(ingredient_id)
        return ingredient.unit_amount >= required_amount

    def deduct_ingredient_amount(self, ingredient_id, amount: Decimal) -> None:
        """Deduct a specified amount from the ingredient's unit_amount."""
        validate_record_exists(self.ingredient_repository, ingredient_id, "Ingredient")
        validate_money_decimal_positive_two_decimal_places(amount, "Amount")

        ingredient = self.ingredient_repository.get_by_id(ingredient_id)
        if ingredient.unit_amount < amount:
            raise InsufficientStockError(
                f"Not enough {ingredient.name} in stock to deduct {amount}."
            )
        ingredient.unit_amount -= amount
        self.ingredient_repository.update(ingredient)