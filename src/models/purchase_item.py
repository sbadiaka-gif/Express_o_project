"""Purchase-item model."""

from dataclasses import dataclass
from decimal import Decimal


@dataclass
class PurchaseItem:
    item_type: str  # Should be "drink" or "baked_good"
    item_id: int
    quantity: int
    unit_price: Decimal
