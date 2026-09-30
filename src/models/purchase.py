"""Purchase model."""

from dataclasses import dataclass, field
from decimal import Decimal
from datetime import datetime

# Assuming purchase_item.py is in the same 'models' folder
from .purchase_item import PurchaseItem


@dataclass
class Purchase:
    customer_id: int
    timestamp: datetime
    total_cost: Decimal
    items: list[PurchaseItem] = field(default_factory=list)
    id: int | None = None
