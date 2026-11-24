
from models import (
    get_all_fruits,
    get_fruit_by_id,
    add_fruit,
    update_fruit,
    delete_fruit,
    get_low_stock_fruits
)

from external_api import search_products, get_product_by_barcode


def display_inventory():
    """Display all fruits in the inventory."""
    fruits = get_all_fruits()

    if not fruits:
        print("Inventory is empty.")
        return

    print("\n===== FRUIT INVENTORY =====")

    for fruit in fruits:
        print(
            f"ID: {fruit['id']} | "
            f"Name: {fruit['name']} | "
            f"Category: {fruit['category']} | "
            f"Price: KES {fruit['price']} | "
            f"Quantity: {fruit['quantity']} {fruit['unit']} | "
            f"Origin: {fruit['origin']}"
        )


def add_new_fruit():
    """Collect information and add a new fruit."""
    try:
        data = {
            "name": input("Fruit name: "),
            "category": input("Category: "),
            "price": input("Price (KES): "),
            "quantity": input("Quantity: "),
            "unit": input("Unit: "),
            "origin": input("Origin: ")
        }

        fruit = add_fruit(data)

        print(f"Successfully added {fruit['name']}!")

    except ValueError as error:
        print(f"Error: {error}")


def search_fruit():
    """Search for a fruit using its inventory ID."""
    try:
        fruit_id = int(input("Enter fruit ID: "))

        fruit = get_fruit_by_id(fruit_id)

        if fruit:
            print("\nFruit found:")
            print(fruit)
        else:
            print("Fruit not found.")

    except ValueError:
        print("Please enter a valid ID.")


def edit_fruit():
    """Update an existing fruit."""
    try:
        fruit_id = int(input("Enter fruit ID: "))

        existing_fruit = get_fruit_by_id(fruit_id)

        if not existing_fruit:
            print("Fruit not found.")
            return

        print("\nEnter new values.")
        print("Leave a field blank to keep its current value.")

        data = {}

        for field in [
            "name",
            "category",
            "price",
            "quantity",
            "unit",
            "origin"
        ]:
            value = input(
                f"{field.capitalize()} "
                f"({existing_fruit[field]}): "
            )

            if value.strip():
                data[field] = value.strip()

        if not data:
            print("No changes made.")
            return

        fruit = update_fruit(fruit_id, data)

        if fruit:
            print("Fruit updated successfully.")
        else:
            print("Fruit not found.")

    except ValueError as error:
        print(f"Error: {error}")


def remove_fruit():
    """Delete a fruit from the inventory."""
    try:
        fruit_id = int(input("Enter fruit ID: "))

        fruit = delete_fruit(fruit_id)

        if fruit:
            print(f"{fruit['name']} deleted successfully.")
        else:
            print("Fruit not found.")

    except ValueError:
        print("Please enter a valid ID.")


def show_low_stock():
    """Display fruits with low stock."""
    fruits = get_low_stock_fruits()

    if not fruits:
        print("No low-stock fruits.")
        return

    print("\n===== LOW STOCK FRUITS =====")

    for fruit in fruits:
        print(
            f"{fruit['name']} - "
            f"Quantity: {fruit['quantity']} {fruit['unit']}"
        )


def search_external_product():
    """Search OpenFoodFacts using a product keyword."""
    query = input("Enter product name: ").strip()

    try:
        products = search_products(query)

        if not products:
            print("No products found.")
            return

        print("\n===== OPENFOODFACTS SEARCH RESULTS =====")

        for product in products:
            print(f"Name: {product.get('name')}")
            print(f"Brand: {product.get('brand')}")
            print(f"Barcode: {product.get('barcode')}")
            print(f"Category: {product.get('category')}")
            print("-" * 40)

    except (ValueError, RuntimeError) as error:
        print(f"Error: {error}")


def lookup_barcode():
    """Look up an OpenFoodFacts product using its barcode."""
    barcode = input("Enter product barcode: ").strip()

    try:
        product = get_product_by_barcode(barcode)

        if product:
            print("\n===== PRODUCT DETAILS =====")
            print(f"Name: {product.get('name')}")
            print(f"Brand: {product.get('brand')}")
            print(f"Barcode: {product.get('barcode')}")
            print(f"Category: {product.get('category')}")
            print(f"Image: {product.get('image')}")
        else:
            print("Product not found.")

    except (ValueError, RuntimeError) as error:
        print(f"Error: {error}")


def main():
    """Run the Fresh Basket inventory management CLI."""

    while True:
        print("\n===== FRESH BASKET FRUITS INVENTORY =====")
        print("1. View all fruits")
        print("2. Add a fruit")
        print("3. Search fruit by ID")
        print("4. Update fruit")
        print("5. Delete fruit")
        print("6. View low-stock fruits")
        print("7. Search OpenFoodFacts")
        print("8. Look up product by barcode")
        print("9. Exit")

        choice = input("Choose an option (1-9): ").strip()

        if choice == "1":
            display_inventory()

        elif choice == "2":
            add_new_fruit()

        elif choice == "3":
            search_fruit()

        elif choice == "4":
            edit_fruit()

        elif choice == "5":
            remove_fruit()

        elif choice == "6":
            show_low_stock()

        elif choice == "7":
            search_external_product()

        elif choice == "8":
            lookup_barcode()

        elif choice == "9":
            print("Thank you for using Fresh Basket!")
            break

        else:
            print("Invalid choice. Please select 1-9.")


if __name__ == "__main__":
    main()
