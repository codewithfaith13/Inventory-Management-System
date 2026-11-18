# command line interface that talks to the Flask API
# run the server first (python app.py), then run this file
import requests

API = "http://127.0.0.1:5000"


def show_item(item):
    print(str(item["id"]) + ". " + item["name"] + " | " + item["brand"] +
          " | price: " + str(item["price"]) + " | stock: " + str(item["stock"]))


def view_all():
    response = requests.get(API + "/inventory")
    items = response.json()
    if len(items) == 0:
        print("Inventory is empty")
    for item in items:
        show_item(item)


def view_one():
    item_id = input("Item id: ")
    response = requests.get(API + "/inventory/" + item_id)
    if response.status_code == 200:
        show_item(response.json())
    else:
        print("Item not found")


def add_item():
    name = input("Name: ")
    brand = input("Brand: ")
    price = float(input("Price: "))
    stock = int(input("Stock: "))
    response = requests.post(API + "/inventory", json={
        "name": name, "brand": brand, "price": price, "stock": stock})
    if response.status_code == 201:
        print("Item added!")
    else:
        print("Could not add item")


def update_item():
    item_id = input("Item id to update: ")
    field = input("Field to change (name/brand/price/stock): ")
    value = input("New value: ")
    if field == "price":
        value = float(value)
    if field == "stock":
        value = int(value)
    response = requests.patch(API + "/inventory/" + item_id, json={field: value})
    if response.status_code == 200:
        print("Item updated!")
    else:
        print("Could not update item")


def delete_item():
    item_id = input("Item id to delete: ")
    response = requests.delete(API + "/inventory/" + item_id)
    if response.status_code == 200:
        print("Item deleted!")
    else:
        print("Item not found")


def import_item():
    choice = input("Search by (1) barcode or (2) name? ")
    data = {}
    if choice == "1":
        data["barcode"] = input("Barcode: ")
    else:
        data["name"] = input("Product name: ")
    data["price"] = float(input("Price: "))
    data["stock"] = int(input("Stock: "))
    response = requests.post(API + "/inventory/import", json=data)
    if response.status_code == 201:
        print("Product added from OpenFoodFacts:")
        show_item(response.json())
    else:
        print("Product not found")


def main():
    while True:
        print("\n--- Inventory Menu ---")
        print("1. View all items")
        print("2. View one item")
        print("3. Add item")
        print("4. Update item")
        print("5. Delete item")
        print("6. Import item from OpenFoodFacts")
        print("7. Quit")
        choice = input("Choose: ")

        try:
            if choice == "1":
                view_all()
            elif choice == "2":
                view_one()
            elif choice == "3":
                add_item()
            elif choice == "4":
                update_item()
            elif choice == "5":
                delete_item()
            elif choice == "6":
                import_item()
            elif choice == "7":
                print("Bye!")
                break
            else:
                print("Invalid choice")
        except requests.exceptions.ConnectionError:
            print("Cannot reach the API. Is the server running?")
        except ValueError:
            print("Please enter a valid number")


if __name__ == "__main__":
    main()
