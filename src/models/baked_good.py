"""Baked-good model."""
from dataclasses import dataclass, field
from decimal import Decimal

@dataclass
class BakedGood:
    name: str
    purchasing_cost: Decimal = Decimal("0.00")
    markup_percentage: Decimal = Decimal("0.00")
    vendor_name: str = ""
    allergens: list[str] = field(default_factory=list[str])
    sale_price: Decimal = Decimal("0.00")
    id: int | None = None