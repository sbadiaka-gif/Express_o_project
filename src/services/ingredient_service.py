"""Ingredient service."""

# CHANGED: original code used bare imports (`from validators` and `from exceptions`), which breaks when the project is
# run from the repository root because Python must import from the `src` package namespace.

from decimal import Decimal
from src.models.ingredient import Ingredient
from src.exceptions import InsufficientStockError
from src.repositories.ingredient_repository import IngredientRepository
from src.validators import (
    validate_money_decimal_positive_two_decimal_places,
    validate_record_exists,
    validate_name_not_empty,
)


class IngredientService:
    def __init__(self, ingredient_repository: IngredientRepository):
        self.ingredient_repository = ingredient_repository

    def add_ingredient(self, ingredient: Ingredient) -> Ingredient:
        """Validate and store a new ingredient."""
        validate_name_not_empty(ingredient.name, "Ingredient name")
        validate_money_decimal_positive_two_decimal_places(
            ingredient.purchasing_cost, "Purchasing cost"
        )
        validate_money_decimal_positive_two_decimal_places(
            ingredient.unit_amount, "Unit amount"
        )
        return self.ingredient_repository.add(ingredient)

    def get_by_id(self, ingredient_id: int) -> Ingredient | None:
        return self.ingredient_repository.get_by_id(ingredient_id)

    def restock_ingredient(self, ingredient_id: int, amount: Decimal) -> None:
        """Restock an ingredient by increasing its unit_amount."""
        validate_record_exists(self.ingredient_repository, ingredient_id, "Ingredient")
        validate_money_decimal_positive_two_decimal_places(amount, "Amount")

        ingredient = self.ingredient_repository.get_by_id(ingredient_id)
        ingredient.unit_amount += amount
        self.ingredient_repository.update(ingredient.id, ingredient)

    def is_ingredient_amount_sufficient(
        self, ingredient_id: int, required_amount: Decimal
    ) -> bool:
        """Check if the ingredient's unit_amount is sufficient for the required amount."""
        validate_record_exists(self.ingredient_repository, ingredient_id, "Ingredient")
        validate_money_decimal_positive_two_decimal_places(
            required_amount, "Required Amount"
        )

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
        self.ingredient_repository.update(ingredient.id, ingredient)

    def validate_ingredient_exists(self, ingredient_id: int) -> None:
        validate_record_exists(self.ingredient_repository, ingredient_id, "Ingredient")
