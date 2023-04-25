import json

from django.test import TestCase
from model_bakery import baker
from rest_framework.test import APIClient

from products.models import Product


class TestProducts(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_get_products(self):
        baker.make(Product, _quantity=3)

        resp = self.client.get("/api/products/", format="json")
        data = json.loads(resp.content)

        self.assertEqual(resp.status_code, 200)
        self.assertEqual(len(data), 3)

    def test_get_product_details(self):
        p = baker.make(Product)

        resp = self.client.get(f"/api/products/{p.id}/", format="json")
        data = json.loads(resp.content)

        self.assertEqual(resp.status_code, 200)
        self.assertEqual(data["id"], str(p.id))
        self.assertEqual(data["name"], p.name)
        self.assertEqual(data["description"], p.description)

    def test_add_product(self):
        data = {
            "name": "test product",
            "description": "test product description",
        }
        self.client.post("/api/products/", data, format="json")

        p = Product.objects.first()
        self.assertEqual(data["name"], p.name)
        self.assertEqual(data["description"], p.description)

    def test_update_product(self):
        data = {
            "name": "test product",
            "description": "test product description",
        }
        self.client.post("/api/products/", data, format="json")

        p = Product.objects.first()  # Get product

        data_update = {"name": "test update"}  # Partial update only
        resp = self.client.put(f"/api/products/{p.id}/", data_update, format="json")

        p.refresh_from_db()

        self.assertEqual(resp.status_code, 204)
        self.assertEqual(p.name, data_update["name"])

    def test_delete_product(self):
        p = baker.make(Product)
        self.client.delete(f"/api/products/{p.id}/")

        self.assertEqual(Product.objects.count(), 0)

    def test_get_offers(self):
        pass
