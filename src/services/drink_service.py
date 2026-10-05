"""Drink service."""

from src.models.drink import Drink
from src.repositories.drink_repository import DrinkRepository
from src.repositories.ingredient_repository import IngredientRepository
from src.services.ingredient_service import IngredientService
from src.models import RecipeItem
from src.validators import validate_record_exists, validate_name_not_empty, validate_money_decimal_positive_two_decimal_places, validate_drink_name_unique
from decimal import Decimal
from exceptions import IngredientNotFoundError


class DrinkService:
    def __init__(self, drink_repository: DrinkRepository, ingredient_service: IngredientService, ingredient_repository: IngredientRepository):
        self.drink_repository = drink_repository
        self.ingredient_service = ingredient_service
        self.ingredient_repository = ingredient_repository

    def add_a_drink(self, drink: Drink) -> None:
        error_messages = []
        validate_name_not_empty(drink.name, "Drink name")
        validate_drink_name_unique(self.drink_repository, drink.name)
        validate_money_decimal_positive_two_decimal_places(drink.markup_percentage, "Markup percentage")
        validate_money_decimal_positive_two_decimal_places(drink.cost_to_produce, "Cost to produce")
        validate_money_decimal_positive_two_decimal_places(drink.sale_price, "Sale price")
        if error_messages:
            raise ValueError(" ".join(error_messages))
        
        self.drink_repository.add(drink)

    def change_drink_price(self, drink_id: int, new_sale_price: Decimal) -> None:
        drink = self._validate_and_get_drink(drink_id, new_sale_price, "New sale price")
        drink.sale_price = new_sale_price
        self.drink_repository.update(drink)

    def change_drink_markup(self, drink_id: int, new_markup_percentage: Decimal) -> None:
        drink = self._validate_and_get_drink(drink_id, new_markup_percentage, "New markup percentage")
        drink.markup_percentage = new_markup_percentage
        self.drink_repository.update(drink)

    def change_cost_to_produce(self, drink_id: int, new_cost_to_produce: Decimal) -> None:
        drink = self._validate_and_get_drink(drink_id, new_cost_to_produce, "New cost to produce")
        drink.cost_to_produce = new_cost_to_produce
        self.drink_repository.update(drink)

    def change_drink_recipe(self, drink_id: int, new_recipe_items: list[RecipeItem]) -> None:
        """Replace a drink's recipe definition. Does not affect ingredient stock."""
        for recipe_item in new_recipe_items:
            validate_record_exists(self.ingredient_repository, recipe_item.ingredient_id, "Ingredient")

        drink = self._validate_and_get_drink_only(drink_id)
        drink.recipe = new_recipe_items
        self.drink_repository.update(drink)

    def add_to_drink_recipe(self, drink_id: int, recipe_item: RecipeItem) -> None:
        """Add a single ingredient to a drink's recipe definition. Does not affect ingredient stock."""
        self.add_recipe_items(drink_id, [recipe_item])

    def remove_from_drink_recipe(self, drink_id: int, ingredient_id: int) -> None:
        """Remove a single ingredient from a drink's recipe definition. Does not affect ingredient stock."""
        self.remove_recipe_items(drink_id, [ingredient_id])

    def add_recipe_items(self, drink_id: int, recipe_items: list[RecipeItem]) -> None:
        """Add multiple ingredients to a drink's recipe definition. Does not affect ingredient stock."""
        for recipe_item in recipe_items:
            validate_record_exists(self.ingredient_repository, recipe_item.ingredient_id, "Ingredient")

        drink = self._validate_and_get_drink_only(drink_id)
        drink.recipe.extend(recipe_items)
        self.drink_repository.update(drink)

    def remove_recipe_items(self, drink_id: int, ingredient_ids: list[int]) -> None:
        """Remove multiple ingredients from a drink's recipe definition. Does not affect ingredient stock."""
        drink = self._validate_and_get_drink_only(drink_id)
        original_recipe_length = len(drink.recipe)
        drink.recipe = [item for item in drink.recipe if item.ingredient_id not in ingredient_ids]

        if len(drink.recipe) == original_recipe_length:
            raise IngredientNotFoundError("No matching ingredients found in the recipe to remove.")

        self.drink_repository.update(drink)

    def _validate_and_get_drink(self, drink_id: int, new_value: Decimal, value_name: str) -> Drink:
        error_messages = []
        validate_record_exists(self.drink_repository, drink_id, "Drink")
        validate_money_decimal_positive_two_decimal_places(new_value, value_name)
        if error_messages:
            raise ValueError(" ".join(error_messages))
        return self.drink_repository.get_by_id(drink_id)

    def _validate_and_get_drink_only(self, drink_id: int) -> Drink:
        """Validate that a drink exists and return it."""
        if validate_record_exists(self.drink_repository, drink_id):
            raise ValueError(f"Drink with ID {drink_id} does not exist.")
        return self.drink_repository.get_by_id(drink_id)