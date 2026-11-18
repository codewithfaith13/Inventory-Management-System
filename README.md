# Inventory Management System

A Flask REST API for managing a small shop's inventory. It can fetch real product details from the [OpenFoodFacts API](https://openfoodfacts.github.io/openfoodfacts-server/api/) and comes with a command-line menu to use it.

## Features
- Add, view, update and delete inventory items
- Search items by name
- Look up products on OpenFoodFacts by barcode or name
- Import an OpenFoodFacts product straight into the inventory
- CLI menu to use everything from the terminal
- Unit tests (the external API is mocked)

## Tech Stack
Python 3, Flask, Requests, Pytest

## Project Structure
```
├── app.py              # Flask API routes
├── external_api.py     # OpenFoodFacts functions
├── cli.py              # Command-line menu
├── tests/              # Unit tests
├── requirements.txt
└── README.md
```

## Installation
```
git clone https://github.com/codewithfaith13/Inventory-Management-System.git
cd Inventory-Management-System
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

## Usage
Start the API in one terminal:
```
python app.py
```
Then start the CLI in a second terminal:
```
python cli.py
```
The API runs at `http://127.0.0.1:5000`.

## API Endpoints
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/inventory` | Get all items |
| GET | `/inventory/<id>` | Get one item |
| POST | `/inventory` | Add an item |
| PATCH | `/inventory/<id>` | Update an item |
| DELETE | `/inventory/<id>` | Delete an item |
| GET | `/inventory/search?name=milk` | Search items by name |
| GET | `/lookup/barcode/<barcode>` | Look up a product by barcode |
| GET | `/lookup/name/<name>` | Look up a product by name |
| POST | `/inventory/import` | Fetch a product from OpenFoodFacts and add it |

**Example: add an item**
```
POST /inventory
{"name": "Eggs", "brand": "Kenchic", "price": 3.5, "stock": 10}
```
Response (`201 Created`):
```
{"id": 3, "name": "Eggs", "brand": "Kenchic", "barcode": "", "price": 3.5, "stock": 10}
```

**Example: import by barcode**
```
POST /inventory/import
{"barcode": "3017620422003", "price": 5, "stock": 4}
```

Errors return a JSON message with `400` (bad request) or `404` (not found).

## Running Tests
```
pytest
```

## Limitations
Items are stored in a Python list, so data resets when the server restarts.

## Author
Faith, Moringa School
