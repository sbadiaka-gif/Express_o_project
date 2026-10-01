"""Ingredient model."""
from dataclasses import dataclass
from decimal import Decimal
from typing import Literal

@dataclass
class Ingredient:
    name: str
    unit_of_measure: Literal["kg"]
    purchasing_cost: Decimal = Decimal("0.00")
    unit_amount: Decimal = Decimal("0.00")
    id: int | None = None   