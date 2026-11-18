# Flask REST API for the inventory
from flask import Flask, jsonify, request
import external_api

app = Flask(__name__)

# our "database" is just a list
inventory = [
    {"id": 1, "name": "Milk", "brand": "Brookside", "barcode": "", "price": 1.5, "stock": 20},
    {"id": 2, "name": "Bread", "brand": "Supaloaf", "barcode": "", "price": 0.9, "stock": 35},
]
next_id = 3


def find_item(item_id):
    for item in inventory:
        if item["id"] == item_id:
            return item
    return None


@app.route("/")
def home():
    return jsonify({"message": "Inventory Management System API"})


# ---------- CRUD ----------

@app.route("/inventory", methods=["GET"])
def get_all_items():
    return jsonify(inventory), 200


@app.route("/inventory/<int:item_id>", methods=["GET"])
def get_item(item_id):
    item = find_item(item_id)
    if item is None:
        return jsonify({"error": "Item not found"}), 404
    return jsonify(item), 200


@app.route("/inventory", methods=["POST"])
def add_item():
    global next_id
    data = request.get_json(silent=True)

    if data is None or "name" not in data:
        return jsonify({"error": "Name is required"}), 400

    new_item = {
        "id": next_id,
        "name": data["name"],
        "brand": data.get("brand", "Unknown"),
        "barcode": data.get("barcode", ""),
        "price": data.get("price", 0),
        "stock": data.get("stock", 0),
    }
    next_id = next_id + 1
    inventory.append(new_item)
    return jsonify(new_item), 201


@app.route("/inventory/<int:item_id>", methods=["PATCH"])
def update_item(item_id):
    item = find_item(item_id)
    if item is None:
        return jsonify({"error": "Item not found"}), 404

    data = request.get_json(silent=True)
    if data is None:
        return jsonify({"error": "No data sent"}), 400

    # only update fields that already exist (not the id)
    for key in data:
        if key in item and key != "id":
            item[key] = data[key]

    return jsonify(item), 200


@app.route("/inventory/<int:item_id>", methods=["DELETE"])
def delete_item(item_id):
    item = find_item(item_id)
    if item is None:
        return jsonify({"error": "Item not found"}), 404

    inventory.remove(item)
    return jsonify({"message": "Item deleted"}), 200


# ---------- helper routes ----------

@app.route("/inventory/search", methods=["GET"])
def search_items():
    name = request.args.get("name", "")
    results = []
    for item in inventory:
        if name.lower() in item["name"].lower():
            results.append(item)
    return jsonify(results), 200


@app.route("/lookup/barcode/<barcode>", methods=["GET"])
def lookup_barcode(barcode):
    product = external_api.get_product_by_barcode(barcode)
    if product is None:
        return jsonify({"error": "Product not found"}), 404
    return jsonify(product), 200


@app.route("/lookup/name/<name>", methods=["GET"])
def lookup_name(name):
    product = external_api.get_product_by_name(name)
    if product is None:
        return jsonify({"error": "Product not found"}), 404
    return jsonify(product), 200


@app.route("/inventory/import", methods=["POST"])
def import_item():
    # fetch from OpenFoodFacts and add it to our inventory list
    global next_id
    data = request.get_json(silent=True)

    if data is None or ("barcode" not in data and "name" not in data):
        return jsonify({"error": "Send a barcode or a name"}), 400

    if "barcode" in data:
        product = external_api.get_product_by_barcode(data["barcode"])
    else:
        product = external_api.get_product_by_name(data["name"])

    if product is None:
        return jsonify({"error": "Product not found"}), 404

    new_item = {
        "id": next_id,
        "name": product["name"],
        "brand": product["brand"],
        "barcode": product["barcode"],
        "price": data.get("price", 0),
        "stock": data.get("stock", 0),
    }
    next_id = next_id + 1
    inventory.append(new_item)
    return jsonify(new_item), 201


if __name__ == "__main__":
    app.run(debug=True)
