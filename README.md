# Fresh Basket Fruits Inventory Management System

## 1. Project Overview

Fresh Basket Fruits Inventory Management System is a Python-based inventory management application designed for a fruit retail business.

The system allows employees to manage fruit stock, including adding new fruits, viewing available inventory, updating product information, deleting products and monitoring low-stock items.

It also integrates with the OpenFoodFacts API to retrieve external product information using keyword searches and product barcodes.

## 2. Features

- Add new fruits to the inventory.
- View all available fruits.
- Search for a fruit using its inventory ID.
- Update existing fruit details.
- Delete fruits from inventory.
- Monitor low-stock fruits.
- Search external food products using OpenFoodFacts.
- Retrieve product information using barcodes.
- REST API built with Flask.
- Command-line interface for inventory management.
- Automated testing using Pytest.

## 3. Technologies Used

- Python 3
- Flask
- Requests
- OpenFoodFacts API
- Pytest
- Git and GitHub

## 4. Project Structure

```text
fresh-basket-inventory/
│
├── app.py
├── models.py
├── external_api.py
├── cli.py
├── requirements.txt
├── README.md
├── .gitignore
│
└── tests/
    ├── __init__.py
    ├── test_app.py
    ├── test_cli.py
    └── test_external_api.py
```

## 5. Installation and Setup

Clone the repository:

```bash
git clone <YOUR_GITHUB_REPOSITORY_URL>
```

Navigate into the project directory:

```bash
cd fresh-basket-inventory
```

Create a virtual environment:

```bash
python3 -m venv venv
```

Activate the virtual environment:

```bash
source venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

## 6. Running the Flask API

Start the Flask development server:

```bash
flask --app app run --debug --port 5001
```

The API will be available at:

```text
http://127.0.0.1:5001
```

## 7. API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/` | Welcome message |
| GET | `/inventory` | Retrieve all fruits |
| GET | `/inventory/<id>` | Retrieve one fruit |
| POST | `/inventory` | Add a new fruit |
| PATCH | `/inventory/<id>` | Update a fruit |
| DELETE | `/inventory/<id>` | Delete a fruit |
| GET | `/inventory/low-stock` | Retrieve low-stock fruits |
| GET | `/api/products/search?query=mango` | Search OpenFoodFacts |
| GET | `/api/products/<barcode>` | Retrieve a product by barcode |

## 8. Example API Requests

Retrieve all fruits:

```bash
curl http://127.0.0.1:5001/inventory
```

Retrieve one fruit:

```bash
curl http://127.0.0.1:5001/inventory/1
```

Add a fruit:

```bash
curl -X POST http://127.0.0.1:5001/inventory \
-H "Content-Type: application/json" \
-d '{"name":"Pineapples","category":"Tropical Fruits","price":150,"quantity":20,"unit":"piece","origin":"Kenya"}'
```

Update a fruit:

```bash
curl -X PATCH http://127.0.0.1:5001/inventory/1 \
-H "Content-Type: application/json" \
-d '{"quantity":65,"price":120}'
```

Delete a fruit:

```bash
curl -X DELETE http://127.0.0.1:5001/inventory/1
```

Retrieve low-stock fruits:

```bash
curl http://127.0.0.1:5001/inventory/low-stock
```

Search OpenFoodFacts:

```bash
curl "http://127.0.0.1:5001/api/products/search?query=mango"
```

Look up a product by barcode:

```bash
curl http://127.0.0.1:5001/api/products/20208639
```

## 9. Running the Command-Line Interface

Run:

```bash
python cli.py
```

The CLI provides the following options:

1. View all fruits.
2. Add a fruit.
3. Search fruit by ID.
4. Update fruit.
5. Delete fruit.
6. View low-stock fruits.
7. Search OpenFoodFacts.
8. Look up product by barcode.
9. Exit.

## 10. Running Automated Tests

Run all project tests:

```bash
pytest -v
```

Run individual test files:

```bash
pytest -v tests/test_app.py
pytest -v tests/test_cli.py
pytest -v tests/test_external_api.py
```

The project currently has 25 automated tests covering the Flask API, CLI and external API integration.

## 11. External API Integration

The application integrates with the OpenFoodFacts API to retrieve food product information.

It supports:

- Searching for products using keywords.
- Retrieving product information using barcodes.
- Handling missing products.
- Handling connection errors and request timeouts.
- Handling invalid API responses.

OpenFoodFacts website:

https://world.openfoodfacts.org/

## 12. Data Storage

The current application uses in-memory Python data structures to manage inventory records.

Inventory changes are available while the application process is running. Data resets when the application is restarted.

## 13. Future Improvements

- Integrate SQLite or another persistent database.
- Add user authentication and authorization.
- Add inventory reports.
- Implement stock transaction history.
- Add automated inventory backup functionality.

## 14. Author
Fresh Basket Fruits Inventory Management System

Developed as a Python and Flask inventory management project.

Rozeline Gitau