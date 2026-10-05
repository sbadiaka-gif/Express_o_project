# PurchaseService

## What is PurchaseService?

`PurchaseService` is the business-logic layer for purchases in the Express-O project.

It is responsible for:
- validating purchase data
- checking that the customer exists
- checking that each item exists and is valid
- getting the current sale price for drinks or baked goods
- calculating the total cost
- saving the purchase
- updating the customer's lifetime spending

This service sits between the repository and the app logic.

- Model: describes what a purchase looks like
- Repository: stores purchase data
- Service: enforces business rules

---

## Why this service exists

A purchase is not just a simple record. It must follow rules like:
- a purchase must belong to a real customer
- it must contain at least one item
- items must have valid IDs and quantities
- the timestamp must be in UTC
- the item price must be taken from the current product record
- the final total must be calculated correctly

The service handles all of that logic.

---

## Class definition

```python
class PurchaseService:
    def __init__(
        self,
        repository: PurchaseRepository,
        customer_service=None,
        drink_service=None,
        baked_good_service=None,
    ):
        self._repository = repository
        self._customer_service = customer_service
        self._drink_service = drink_service
        self._baked_good_service = baked_good_service
```

### What the constructor does

The constructor receives dependencies:
- `repository`: the purchase repository used to save, read, update, and delete purchases
- `customer_service`: used to validate the customer and update customer spend
- `drink_service`: used to find a drink and get its current sale price
- `baked_good_service`: used to find a baked good and get its current sale price

This is dependency injection. The service is not creating its own dependencies; it is receiving them from outside.

---

## get_all

```python
def get_all(self) -> list[Purchase]:
    return self._repository.get_all()
```

This method returns every purchase in the repository.

Use cases:
- viewing all sales
- generating reports
- listing transactions

---

## get_by_id

```python
def get_by_id(self, purchase_id: int) -> Purchase | None:
    return self._repository.get_by_id(purchase_id)
```

This method looks up a single purchase by its ID.

Use cases:
- viewing one purchase
- checking whether a purchase exists before updating it

---

## create_purchase

```python
def create_purchase(self, purchase: Purchase) -> Purchase:
    self._validate_purchase(purchase)
    purchase.total_cost = self._calculate_total_cost(purchase)
    purchase.timestamp = self._normalize_timestamp(purchase.timestamp)

    created_purchase = self._repository.add(purchase)

    if purchase.customer_id is not None and self._customer_service is not None:
        record_purchase = getattr(self._customer_service, "record_purchase", None)
        if callable(record_purchase):
            record_purchase(purchase.customer_id, created_purchase.total_cost)

    return created_purchase
```

### Step-by-step explanation

1. `_validate_purchase(purchase)`
   - checks that the purchase is valid before saving

2. `purchase.total_cost = self._calculate_total_cost(purchase)`
   - calculates the total price of all items

3. `purchase.timestamp = self._normalize_timestamp(purchase.timestamp)`
   - ensures the timestamp is in UTC format

4. `created_purchase = self._repository.add(purchase)`
   - saves the purchase and gives it an ID

5. If the customer service has a `record_purchase` method, it updates the customer's lifetime spending

6. The final saved purchase is returned

### In plain English

This is the method used when a new purchase is being created.

---

## update_purchase

```python
def update_purchase(self, purchase_id: int, purchase: Purchase) -> Purchase | None:
    if self._repository.get_by_id(purchase_id) is None:
        raise ValueError("Purchase does not exist.")

    purchase.id = purchase_id
    self._validate_purchase(purchase)
    purchase.total_cost = self._calculate_total_cost(purchase)
    purchase.timestamp = self._normalize_timestamp(purchase.timestamp)

    updated_purchase = self._repository.update(purchase_id, purchase)
    if updated_purchase is not None and self._customer_service is not None:
        record_purchase = getattr(self._customer_service, "record_purchase", None)
        if callable(record_purchase):
            record_purchase(purchase.customer_id, updated_purchase.total_cost)

    return updated_purchase
```

This method updates an existing purchase.

It:
- checks the purchase exists
- validates the updated data
- recalculates the total
- confirms the timestamp is UTC
- saves the updated version
- updates the customer spend

---

## delete_purchase

```python
def delete_purchase(self, purchase_id: int) -> bool:
    return self._repository.delete(purchase_id)
```

This deletes a purchase from the repository.

Return value:
- `True` if the item was deleted
- `False` if no matching purchase was found

---

## _validate_purchase

```python
def _validate_purchase(self, purchase: Purchase) -> None:
    if purchase.customer_id is None:
        raise ValueError("Customer ID is required.")
    if purchase.items is None or len(purchase.items) == 0:
        raise ValueError("Purchase must include at least one item.")
    if purchase.timestamp is None:
        purchase.timestamp = datetime.now(timezone.utc)
    else:
        validate_purchase_timestamp_utc(purchase.timestamp)

    self._validate_customer_exists(purchase.customer_id)

    for item in purchase.items:
        if item.item_id is None:
            raise ValueError("Each purchase item must reference a valid item ID.")
        if item.quantity <= 0:
            raise ValueError("Item quantity must be greater than zero.")
        if item.item_type not in {"drink", "baked_good"}:
            raise ValueError("Item type must be 'drink' or 'baked_good'.")

        item.unit_price = self._get_current_item_price(item)
```

This is the validation gate before a purchase is saved.

It checks:
- customer ID is present
- purchase has at least one item
- timestamp is valid UTC
- customer exists
- each item has a valid ID
- quantity is greater than zero
- item type is allowed
- each item has a current price

If any rule fails, it raises a `ValueError`.

---

## _calculate_total_cost

```python
def _calculate_total_cost(self, purchase: Purchase) -> Decimal:
    total_cost = Decimal("0.00")
    for item in purchase.items:
        total_cost += Decimal(item.quantity) * item.unit_price
    return total_cost.quantize(Decimal("0.01"))
```

This method adds up all item costs.

For each purchase item:
- multiply quantity by unit price
- add it to the running total
- round to 2 decimal places

This keeps money accurate and prevents floating-point rounding problems.

---

## _normalize_timestamp

```python
def _normalize_timestamp(self, timestamp: datetime) -> datetime:
    if timestamp.tzinfo is None:
        raise ValueError("Timestamp must be in UTC format.")
    validate_purchase_timestamp_utc(timestamp)
    return timestamp.astimezone(timezone.utc)
```

This method makes sure the timestamp:
- has timezone information
- is actually in UTC
- gets converted to UTC before being saved

This follows the project rule that all purchase timestamps must be UTC.

---

## _validate_customer_exists

```python
def _validate_customer_exists(self, customer_id: int) -> None:
    if self._customer_service is None:
        raise ValueError("Customer service is required.")

    get_customer_method = getattr(
        self._customer_service, "get_customer_by_id", None
    )
    if get_customer_method is None:
        get_customer_method = getattr(self._customer_service, "get_by_id", None)

    if get_customer_method is None:
        raise ValueError("Customer service does not support customer lookup.")

    if get_customer_method(customer_id) is None:
        raise ValueError("Customer does not exist.")
```

This method verifies the customer exists before creating a purchase.

If no customer with that ID is found, the service stops and raises an error.

---

## _get_current_item_price

```python
def _get_current_item_price(self, item):
    if item.item_type == "drink":
        if self._drink_service is None:
            raise ValueError("Drink service is required to price a drink purchase.")

        get_drink_method = getattr(self._drink_service, "get_drink_by_id", None)
        if get_drink_method is None:
            get_drink_method = getattr(self._drink_service, "get_by_id", None)

        if get_drink_method is None:
            raise ValueError("Drink service does not support drink lookup.")

        drink = get_drink_method(item.item_id)
        if drink is None:
            raise ValueError("Drink does not exist.")
        return drink.sale_price

    if item.item_type == "baked_good":
        if self._baked_good_service is None:
            raise ValueError(
                "Baked good service is required to price a baked good purchase."
            )

        get_baked_good_method = getattr(
            self._baked_good_service, "get_baked_good_by_id", None
        )
        if get_baked_good_method is None:
            get_baked_good_method = getattr(
                self._baked_good_service, "get_by_id", None
            )

        if get_baked_good_method is None:
            raise ValueError(
                "Baked good service does not support baked good lookup."
            )

        baked_good = get_baked_good_method(item.item_id)
        if baked_good is None:
            raise ValueError("Baked good does not exist.")
        return baked_good.sale_price

    raise ValueError("Item type must be 'drink' or 'baked_good'.")
```

This method gets the current price of each item before calculating the purchase total.

- if the item is a drink, it uses `drink.sale_price`
- if the item is a baked good, it uses `baked_good.sale_price`
- if it is neither, it raises an error

This is important because purchases should use the current sale price, not a stale or wrong value.

---

## Real-world example

```python
purchase = Purchase(
    customer_id=1,
    items=[
        PurchaseItem(item_type="drink", item_id=7, quantity=2),
    ],
    timestamp=datetime.now(timezone.utc),
)

saved_purchase = purchase_service.create_purchase(purchase)
```

### Example flow

1. Customer 1 exists
2. Drink 7 exists
3. Drink 7 has a sale price of $5.00
4. Quantity is 2
5. Total is $10.00
6. The purchase is saved
7. Customer lifetime spending is updated

---

## Summary

`PurchaseService` is the logic layer for purchases.

It makes sure every purchase is:
- valid
- connected to a real customer
- made of valid items
- priced correctly
- saved in UTC time
- added to the customer’s lifetime totals

This is exactly the kind of service you want in a layered architecture.

---

## Quick one-line summary

`PurchaseService` handles all purchase business rules: validation, price lookup, total calculation, saving, and customer spend tracking.
