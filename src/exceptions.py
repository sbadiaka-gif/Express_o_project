"""Application-specific exceptions."""


class DrinkNotFoundError(Exception):
    """Raised when a requested drink does not exist."""

    pass


class IngredientNotFoundError(Exception):
    """Raised when a requested ingredient does not exist."""

    pass


class BakedGoodNotFoundError(Exception):
    """Raised when a requested baked good does not exist."""

    pass


class BakedGoodDuplicateItemError(Exception):
    """Raised when there are a duplicate baked goods."""

    pass


class CustomerDuplicateEmailError(Exception):
    """Raised when there are a duplicate emails."""

    pass


class CustomerNotFoundError(Exception):
    """Raised when a requested customer does not exist."""

    pass


class CustomerLifetimeSpentIsIncorrectError(Exception):
    """Raised when the customers lifetime_spent doesn't match purchases."""

    pass


class InsufficientStockError(Exception):
    """Raised when there isn't enough of an ingredient to fulfill an order."""

    pass
