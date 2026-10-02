"""Input validation helpers."""

from decimal import Decimal
from datetime import datetime
from src.repositories.drink_repository import DrinkRepository


def validate_name_not_empty(value: str, name: str) -> None:
    """Validate that a string is not empty."""
    if not value.strip():
        raise ValueError(f"{name} cannot be empty.")


def validate_money_decimal_positive_two_decimal_places(
    value: Decimal, name: str
) -> None:
    """Validate that a float is positive and has at most two decimal places."""
    error =[]
    if not isinstance(value, Decimal):
        error.append(f"{name} must be a Decimal type.")
    if value <= 0:
        error.append(f"{name} must be a positive number.")
    if value.as_tuple().exponent < -2:
        error.append(f"{name} must have at most two decimal places.")
    if error:
        raise ValueError(" ".join(error))

def validate_markup_is_decimal_and_positive(value: Decimal, name: str) -> None:
    """Validate that a decimal is positive."""
    error = []
    if not isinstance(value, Decimal):
            error.append(f"{name} must be a Decimal type.")
    if value < 0:
        error.append(f"{name} must be a positive number.")
    if error:
        raise ValueError(" ".join(error))


def validate_email(value: str) -> None:
    """Validate that an email address is in a valid format."""
    if "@" not in value or "." not in value.split("@")[-1]:
        raise ValueError("Invalid email address format.")


def validate_drink_name_unique(drink_repository, name: str) -> None:
    """Validate that a drink name is unique in the drink repository."""
    existing_drinks = drink_repository.get_all()
    for drink in existing_drinks:
        if drink.name == name:
            raise ValueError("Drink name must be unique.")


def validate_purchase_timestamp_utc(value: datetime) -> None:
    """Validate that a timestamp is in UTC format."""
    if value.tzinfo != datetime.timezone.utc:
        raise ValueError("Timestamp must be in UTC format.")

def validate_record_exists(repository, record_id: int, name: str) -> None:
   record_exists = [record for record in repository.get_all() if record.id == record_id]
   if not record_exists:
       raise ValueError(f"{name} does not exist.")

def validate_record_exists(repository, record_id: int) -> None:
    record_exists = [
        record for record in repository.get_all() if record.id == record_id
    ]
    if not record_exists:
        raise ValueError("Record does not exist.")
