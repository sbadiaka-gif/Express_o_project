"""Purchase-item model."""

from dataclasses import dataclass
from typing import Literal
from decimal import Decimal


@dataclass
class PurchaseItem:
    item_type: Literal["drink", "baked_good"]
    item_id: int | None = None
    quantity: int = 1
    unit_price: Decimal = Decimal("0.00")
