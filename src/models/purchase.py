"""Purchase model."""

from dataclasses import dataclass, field
from decimal import Decimal
from datetime import datetime
from .purchase_item import PurchaseItem


@dataclass
class Purchase:
    customer_id: int | None = None
    timestamp: datetime = field(default_factory=datetime.now)
    total_cost: Decimal = Decimal("0.00")
    items: list[PurchaseItem] = field(default_factory=list)
    id: int | None = None
