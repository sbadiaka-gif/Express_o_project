"""Recipe-item model."""
# src/models/recipe_item.py
from dataclasses import dataclass
from decimal import Decimal

@dataclass
class RecipeItem:
    ingredient_id: int | None = None
    quantity: Decimal = Decimal("0.00")