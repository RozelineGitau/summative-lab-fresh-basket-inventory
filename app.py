
from flask import Flask, jsonify, request

from models import (
    get_all_fruits,
    get_fruit_by_id,
    add_fruit,
    update_fruit,
    delete_fruit,
    get_low_stock_fruits
)

from external_api import (
    search_products,
    get_product_by_barcode
)


app = Flask(__name__)


# -----------------------------------
# HOME ROUTE
# -----------------------------------

@app.route("/", methods=["GET"])
def home():
    return jsonify({
        "message": "Welcome to Fresh Basket Fruits Inventory Management System",
        "available_routes": [
            "/inventory",
            "/inventory/<id>",
            "/inventory/low-stock",
            "/api/products/search?query=mango",
            "/api/products/<barcode>"
        ]
    }), 200


# -----------------------------------
# GET ALL INVENTORY
# -----------------------------------

@app.route("/inventory", methods=["GET"])
def get_inventory():
    return jsonify(get_all_fruits()), 200


# -----------------------------------
# GET ONE FRUIT
# -----------------------------------

@app.route("/inventory/<int:fruit_id>", methods=["GET"])
def get_inventory_item(fruit_id):
    fruit = get_fruit_by_id(fruit_id)

    if fruit is None:
        return jsonify({
            "error": "Fruit not found"
        }), 404

    return jsonify(fruit), 200


# -----------------------------------
# ADD A NEW FRUIT
# -----------------------------------

@app.route("/inventory", methods=["POST"])
def create_inventory_item():
    data = request.get_json(silent=True)

    if not isinstance(data, dict):
        return jsonify({
            "error": "Request body must be valid JSON"
        }), 400

    try:
        new_fruit = add_fruit(data)

        return jsonify(new_fruit), 201

    except ValueError as error:
        return jsonify({
            "error": str(error)
        }), 400


# -----------------------------------
# UPDATE A FRUIT
# -----------------------------------

@app.route("/inventory/<int:fruit_id>", methods=["PATCH"])
def update_inventory_item(fruit_id):
    data = request.get_json(silent=True)

    if not isinstance(data, dict) or not data:
        return jsonify({
            "error": "Provide valid JSON data to update"
        }), 400

    try:
        updated_fruit = update_fruit(fruit_id, data)

        if updated_fruit is None:
            return jsonify({
                "error": "Fruit not found"
            }), 404

        return jsonify(updated_fruit), 200

    except ValueError as error:
        return jsonify({
            "error": str(error)
        }), 400


# -----------------------------------
# DELETE A FRUIT
# -----------------------------------

@app.route("/inventory/<int:fruit_id>", methods=["DELETE"])
def remove_inventory_item(fruit_id):
    deleted_fruit = delete_fruit(fruit_id)

    if deleted_fruit is None:
        return jsonify({
            "error": "Fruit not found"
        }), 404

    return "", 204


# -----------------------------------
# LOW-STOCK INVENTORY
# -----------------------------------

@app.route("/inventory/low-stock", methods=["GET"])
def low_stock():
    return jsonify(get_low_stock_fruits()), 200


# -----------------------------------
# SEARCH PRODUCTS ON OPENFOODFACTS
# -----------------------------------

@app.route("/api/products/search", methods=["GET"])
def search_external_products():
    query = request.args.get("query", "").strip()

    if not query:
        return jsonify({
            "error": "Search query is required"
        }), 400

    try:
        products = search_products(query)

        return jsonify({
            "query": query,
            "products": products
        }), 200

    except ValueError as error:
        return jsonify({
            "error": str(error)
        }), 400

    except RuntimeError as error:
        return jsonify({
            "error": str(error)
        }), 502


# -----------------------------------
# LOOK UP PRODUCT USING BARCODE
# -----------------------------------

@app.route("/api/products/<barcode>", methods=["GET"])
def lookup_external_product(barcode):
    try:
        product = get_product_by_barcode(barcode)

        if product is None:
            return jsonify({
                "error": "Product not found"
            }), 404

        return jsonify(product), 200

    except ValueError as error:
        return jsonify({
            "error": str(error)
        }), 400

    except RuntimeError as error:
        return jsonify({
            "error": str(error)
        }), 502


# -----------------------------------
# RUN FLASK APPLICATION
# -----------------------------------

if __name__ == "__main__":
    app.run(debug=True, port=5001)
