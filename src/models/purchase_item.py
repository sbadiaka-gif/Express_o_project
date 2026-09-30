"""Purchase-item model."""

from dataclasses import dataclass
from decimal import Decimal


@dataclass
class PurchaseItem:
    item_type: str = ""  # Should be "drink" or "baked_good"
    item_id: int = 0
    quantity: int = 1
    unit_price: Decimal = Decimal("0.00")
