"""Drink model."""
from src.models.recipe_item import RecipeItem
from dataclasses import dataclass, field
from decimal import Decimal

@dataclass
class Drink:
    name: str
    recipe: list[RecipeItem] = field(default_factory=list[RecipeItem])
    markup_percentage: Decimal = Decimal("0.00")
    cost_to_produce: Decimal = Decimal("0.00")
    sale_price: Decimal = Decimal("0.00")
    id: int | None = None
