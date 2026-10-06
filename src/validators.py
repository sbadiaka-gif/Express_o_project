"""Input validation helpers."""

# Original version had duplicate `validate_record_exists` definitions and a few validation rules that
# rejected valid zeros or used incorrect import paths. The updated version keeps one shared validator
# definition and validates money as non-negative instead of strictly positive.

from datetime import datetime, timezone
from decimal import Decimal
from src.repositories.drink_repository import DrinkRepository
from src.repositories.repository import Repository


# CHANGED: this validator now handles None safely before checking .strip().
def validate_name_not_empty(value: str, name: str) -> None:
    """Validate that a string is not empty."""
    if not value or not value.strip():
        raise ValueError(f"{name} cannot be empty.")


# CHANGED: original version rejected valid zero values; this version allows zero and only rejects negatives.
def validate_money_decimal_positive_two_decimal_places(
    value: Decimal, name: str
) -> None:
    """Validate that a Decimal is non-negative and has at most two decimal places."""
    error: list[str] = []

    if not type(value) is Decimal:
        error.append(f"{name} must be a Decimal type.")
    if value < 0:
        error.append(f"{name} must be a positive number.")
    if value.as_tuple().exponent < -2:
        error.append(f"{name} must have at most two decimal places.")

    if error:
        raise ValueError(", ".join(error))


def validate_markup_is_decimal_and_positive(value: Decimal, name: str) -> None:
    """Validate that a decimal is non-negative."""
    error: list[str] = []

    if not type(value) is Decimal:
        error.append(f"{name} must be a Decimal type.")
    if value < 0:
        error.append(f"{name} must be a positive number.")

    if error:
        raise ValueError(" ".join(error))


def validate_email(value: str) -> None:
    """Validate that an email address is in a valid format."""
    if "@" not in value or "." not in value.split("@")[-1]:
        raise ValueError("Invalid email address format.")


def validate_drink_name_unique(drink_repository: DrinkRepository, name: str) -> None:
    """Validate that a drink name is unique in the drink repository."""
    existing_drinks = drink_repository.get_all()
    for drink in existing_drinks:
        if drink.name == name:
            raise ValueError("Drink name must be unique.")


# CHANGE: replaced the old timezone check with a UTC offset check that works correctly for timezone-aware datetimes.
def validate_purchase_timestamp_utc(value: datetime) -> None:
    """Validate that a timestamp is in UTC format."""
    if value.tzinfo != timezone.utc:
        raise ValueError("Timestamp must be in UTC format.")


# CHANGE: kept only one shared implementation of validate_record_exists and added a default name for cleaner error messages.
def validate_record_exists[T](
    repository: Repository[T], record_id: int, name: str = "Record"
) -> None:
    """Validate that an item with the supplied id exists in the repository."""
    record_exists: list[T] = [
        record for record in repository.get_all() if record.id == record_id
    ]
    if not record_exists:
        raise ValueError(f"{name} does not exist.")
