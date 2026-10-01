"""Application-specific exceptions."""
class DrinkNotFoundError(Exception):
    """Raised when a requested drink does not exist."""
    pass

class IngredientNotFoundError(Exception):
    """Raised when a requested ingredient does not exist."""
    pass

class InsufficientStockError(Exception):
    """Raised when there isn't enough of an ingredient to fulfill an order."""
    pass