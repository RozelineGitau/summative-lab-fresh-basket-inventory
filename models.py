
fruits = [
    {
        "id": 1,
        "name": "Mangoes",
        "category": "Tropical Fruits",
        "price": 100.00,
        "quantity": 50,
        "unit": "piece",
        "origin": "Kenya"
    },
    {
        "id": 2,
        "name": "Bananas",
        "category": "Tropical Fruits",
        "price": 120.00,
        "quantity": 80,
        "unit": "bunch",
        "origin": "Uganda"
    },
    {
        "id": 3,
        "name": "Apples",
        "category": "Temperate Fruits",
        "price": 50.00,
        "quantity": 100,
        "unit": "piece",
        "origin": "South Africa"
    },
    {
        "id": 4,
        "name": "Avocados",
        "category": "Tropical Fruits",
        "price": 30.00,
        "quantity": 8,
        "unit": "piece",
        "origin": "Kenya"
    },
    {
        "id": 5,
        "name": "Oranges",
        "category": "Citrus Fruits",
        "price": 25.00,
        "quantity": 0,
        "unit": "piece",
        "origin": "Kenya"
    }
]


# Generate the next available ID
def generate_id():
    if not fruits:
        return 1

    return max(fruit["id"] for fruit in fruits) + 1


# Retrieve all fruits
def get_all_fruits():
    return fruits


# Retrieve one fruit using its ID
def get_fruit_by_id(fruit_id):
    for fruit in fruits:
        if fruit["id"] == fruit_id:
            return fruit

    return None


# Add a new fruit
def add_fruit(data):
    required_fields = ["name", "category", "price", "quantity", "unit", "origin"]

    for field in required_fields:
        if field not in data or data[field] in (None, ""):
            raise ValueError(f"{field} is required")

    try:
        price = float(data["price"])
        quantity = int(data["quantity"])
    except (ValueError, TypeError):
        raise ValueError("Price must be a number and quantity must be a whole number")

    if price < 0 or quantity < 0:
        raise ValueError("Price and quantity cannot be negative")

    new_fruit = {
        "id": generate_id(),
        "name": str(data["name"]).strip(),
        "category": str(data["category"]).strip(),
        "price": price,
        "quantity": quantity,
        "unit": str(data["unit"]).strip(),
        "origin": str(data["origin"]).strip()
    }

    fruits.append(new_fruit)

    return new_fruit


# Update an existing fruit
def update_fruit(fruit_id, data):
    fruit = get_fruit_by_id(fruit_id)

    if fruit is None:
        return None

    allowed_fields = ["name", "category", "price", "quantity", "unit", "origin"]

    for field, value in data.items():
        if field not in allowed_fields:
            raise ValueError(f"Invalid field: {field}")

        if value is None or value == "":
            raise ValueError(f"{field} cannot be empty")

        if field == "price":
            try:
                value = float(value)
            except (ValueError, TypeError):
                raise ValueError("Price must be a number")

            if value < 0:
                raise ValueError("Price cannot be negative")

        elif field == "quantity":
            try:
                value = int(value)
            except (ValueError, TypeError):
                raise ValueError("Quantity must be a whole number")

            if value < 0:
                raise ValueError("Quantity cannot be negative")

        elif isinstance(value, str):
            value = value.strip()

            if not value:
                raise ValueError(f"{field} cannot be empty")

        fruit[field] = value

    return fruit


# Delete a fruit
def delete_fruit(fruit_id):
    fruit = get_fruit_by_id(fruit_id)

    if fruit is None:
        return None

    fruits.remove(fruit)

    return fruit


# Retrieve fruits with low stock
def get_low_stock_fruits(threshold=10):
    return [
        fruit for fruit in fruits
        if fruit["quantity"] <= threshold
    ]
