import unittest
from unittest.mock import patch
import app as app_module


class TestInventoryAPI(unittest.TestCase):

    def setUp(self):
        # reset the data before every test
        app_module.inventory.clear()
        app_module.inventory.append(
            {"id": 1, "name": "Milk", "brand": "Brookside", "barcode": "", "price": 1.5, "stock": 20})
        app_module.inventory.append(
            {"id": 2, "name": "Bread", "brand": "Supaloaf", "barcode": "", "price": 0.9, "stock": 35})
        app_module.next_id = 3
        self.client = app_module.app.test_client()

    # ----- READ -----
    def test_home(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)

    def test_get_all(self):
        response = self.client.get("/inventory")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.get_json()), 2)

    def test_get_one(self):
        response = self.client.get("/inventory/1")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json()["name"], "Milk")

    def test_get_one_not_found(self):
        response = self.client.get("/inventory/99")
        self.assertEqual(response.status_code, 404)

    # ----- CREATE -----
    def test_add_item(self):
        response = self.client.post("/inventory", json={"name": "Eggs", "price": 3, "stock": 10})
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.get_json()["id"], 3)
        self.assertEqual(len(app_module.inventory), 3)

    def test_add_item_without_name(self):
        response = self.client.post("/inventory", json={"price": 3})
        self.assertEqual(response.status_code, 400)

    def test_add_item_no_body(self):
        response = self.client.post("/inventory")
        self.assertEqual(response.status_code, 400)

    # ----- UPDATE -----
    def test_update_item(self):
        response = self.client.patch("/inventory/1", json={"stock": 5})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json()["stock"], 5)

    def test_update_cannot_change_id(self):
        self.client.patch("/inventory/1", json={"id": 50})
        self.assertEqual(app_module.inventory[0]["id"], 1)

    def test_update_not_found(self):
        response = self.client.patch("/inventory/99", json={"stock": 5})
        self.assertEqual(response.status_code, 404)

    def test_update_no_body(self):
        response = self.client.patch("/inventory/1")
        self.assertEqual(response.status_code, 400)

    # ----- DELETE -----
    def test_delete_item(self):
        response = self.client.delete("/inventory/1")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(app_module.inventory), 1)

    def test_delete_not_found(self):
        response = self.client.delete("/inventory/99")
        self.assertEqual(response.status_code, 404)

    # ----- SEARCH -----
    def test_search_found(self):
        response = self.client.get("/inventory/search?name=mil")
        self.assertEqual(len(response.get_json()), 1)

    def test_search_not_found(self):
        response = self.client.get("/inventory/search?name=zzz")
        self.assertEqual(response.get_json(), [])

    # ----- EXTERNAL API ROUTES (mocked) -----
    @patch("app.external_api.get_product_by_barcode")
    def test_lookup_barcode(self, mock_get):
        mock_get.return_value = {"name": "Nutella", "brand": "Ferrero", "barcode": "123", "ingredients": ""}
        response = self.client.get("/lookup/barcode/123")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json()["name"], "Nutella")

    @patch("app.external_api.get_product_by_barcode")
    def test_lookup_barcode_not_found(self, mock_get):
        mock_get.return_value = None
        response = self.client.get("/lookup/barcode/000")
        self.assertEqual(response.status_code, 404)

    @patch("app.external_api.get_product_by_name")
    def test_lookup_name(self, mock_get):
        mock_get.return_value = {"name": "Nutella", "brand": "Ferrero", "barcode": "123", "ingredients": ""}
        response = self.client.get("/lookup/name/nutella")
        self.assertEqual(response.status_code, 200)

    @patch("app.external_api.get_product_by_name")
    def test_lookup_name_not_found(self, mock_get):
        mock_get.return_value = None
        response = self.client.get("/lookup/name/zzz")
        self.assertEqual(response.status_code, 404)

    @patch("app.external_api.get_product_by_barcode")
    def test_import_by_barcode(self, mock_get):
        mock_get.return_value = {"name": "Nutella", "brand": "Ferrero", "barcode": "123", "ingredients": ""}
        response = self.client.post("/inventory/import", json={"barcode": "123", "price": 5, "stock": 4})
        self.assertEqual(response.status_code, 201)
        self.assertEqual(len(app_module.inventory), 3)
        self.assertEqual(app_module.inventory[2]["name"], "Nutella")

    @patch("app.external_api.get_product_by_name")
    def test_import_by_name(self, mock_get):
        mock_get.return_value = {"name": "Nutella", "brand": "Ferrero", "barcode": "123", "ingredients": ""}
        response = self.client.post("/inventory/import", json={"name": "nutella"})
        self.assertEqual(response.status_code, 201)

    @patch("app.external_api.get_product_by_barcode")
    def test_import_not_found(self, mock_get):
        mock_get.return_value = None
        response = self.client.post("/inventory/import", json={"barcode": "000"})
        self.assertEqual(response.status_code, 404)
        self.assertEqual(len(app_module.inventory), 2)

    def test_import_bad_request(self):
        response = self.client.post("/inventory/import", json={"price": 5})
        self.assertEqual(response.status_code, 400)


if __name__ == "__main__":
    unittest.main()
