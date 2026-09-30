"""Ingredient model."""
from dataclasses import dataclass
from decimal import Decimal

@dataclass
class Ingredient:
    name: str
    purchasing_cost: Decimal = Decimal("0.00")
    unit_amount: Decimal = Decimal("0.00")
    unit_of_measure: str
    id: int | None = None   