"""Customer model."""
from dataclasses import dataclass
from decimal import Decimal

@dataclass
class Customer:
    name: str
    email: str
    lifetime_spent: Decimal
    id: int