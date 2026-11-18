import unittest
from unittest.mock import patch, MagicMock
import requests
import external_api


class TestExternalAPI(unittest.TestCase):

    @patch("external_api.requests.get")
    def test_barcode_found(self, mock_get):
        fake = MagicMock()
        fake.json.return_value = {
            "status": 1,
            "product": {"product_name": "Nutella", "brands": "Ferrero", "ingredients_text": "sugar"},
        }
        mock_get.return_value = fake
        result = external_api.get_product_by_barcode("3017620422003")
        self.assertEqual(result["name"], "Nutella")
        self.assertEqual(result["barcode"], "3017620422003")

    @patch("external_api.requests.get")
    def test_barcode_not_found(self, mock_get):
        fake = MagicMock()
        fake.json.return_value = {"status": 0}
        mock_get.return_value = fake
        self.assertIsNone(external_api.get_product_by_barcode("000"))

    @patch("external_api.requests.get")
    def test_barcode_network_error(self, mock_get):
        mock_get.side_effect = requests.RequestException("no internet")
        self.assertIsNone(external_api.get_product_by_barcode("123"))

    @patch("external_api.requests.get")
    def test_name_found(self, mock_get):
        fake = MagicMock()
        fake.json.return_value = {
            "products": [{"product_name": "Nutella", "brands": "Ferrero", "code": "123"}]
        }
        mock_get.return_value = fake
        result = external_api.get_product_by_name("nutella")
        self.assertEqual(result["brand"], "Ferrero")

    @patch("external_api.requests.get")
    def test_name_no_results(self, mock_get):
        fake = MagicMock()
        fake.json.return_value = {"products": []}
        mock_get.return_value = fake
        self.assertIsNone(external_api.get_product_by_name("zzzz"))

    @patch("external_api.requests.get")
    def test_name_network_error(self, mock_get):
        mock_get.side_effect = requests.RequestException("no internet")
        self.assertIsNone(external_api.get_product_by_name("nutella"))


if __name__ == "__main__":
    unittest.main()
