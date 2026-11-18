# talks to the OpenFoodFacts API
import requests

BASE_URL = "https://world.openfoodfacts.org"
HEADERS = {"User-Agent": "InventoryManagementSystem/1.0 (student project)"}


def clean_product(product):
    # pick only the fields we care about
    return {
        "name": product.get("product_name", "Unknown"),
        "brand": product.get("brands", "Unknown"),
        "barcode": product.get("code", ""),
        "ingredients": product.get("ingredients_text", ""),
    }


def get_product_by_barcode(barcode):
    url = BASE_URL + "/api/v0/product/" + str(barcode) + ".json"
    try:
        response = requests.get(url, headers=HEADERS, timeout=10)
        data = response.json()
    except (requests.RequestException, ValueError):
        return None

    if data.get("status") != 1:
        return None

    product = data["product"]
    product["code"] = barcode
    return clean_product(product)


def get_product_by_name(name):
    url = BASE_URL + "/cgi/search.pl"
    params = {
        "search_terms": name,
        "search_simple": 1,
        "action": "process",
        "json": 1,
        "page_size": 1,
    }
    try:
        response = requests.get(url, params=params, headers=HEADERS, timeout=10)
        data = response.json()
    except (requests.RequestException, ValueError):
        return None

    products = data.get("products", [])
    if len(products) == 0:
        return None

    return clean_product(products[0])
