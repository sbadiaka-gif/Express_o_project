"""Ingredient model."""
from dataclasses import dataclass
from decimal import Decimal
from typing import Literal

@dataclass
class Ingredient:
    name: str
    purchasing_cost: Decimal = Decimal("0.00")
    unit_amount: Decimal = Decimal("0.00")
    unit_of_measure: Literal["kg"]
    id: int | None = None   