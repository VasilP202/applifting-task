import json
import uuid
from datetime import datetime, timedelta

import requests
from django.test import TestCase
from model_bakery import baker
from rest_framework.test import APIClient

from api.use_cases import get_access_token, register_product
from products.models import Offer, Product


class TestCRUDProducts(TestCase):
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
            # "id": str(uuid.uuid4()),
            "name": "test product",
            "description": "test product description",
        }
        self.client.post("/api/products/", data, format="json")

        p = Product.objects.first()
        # self.assertEqual(data["id"], str(p.id))
        self.assertEqual(data["name"], p.name)
        self.assertEqual(data["description"], p.description)

    def test_update_product(self):
        data = {
            # "id": str(uuid.uuid4()),
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

    def test_register_product(self):
        p = baker.make(Product)
        register_product(p)

    def test_offers(self):
        id = "a0d60e80-59eb-412a-ab7f-06b929e92eb4"

        url = f"https://python.exercise.applifting.cz/api/v1/products/{id}/offers"
        resp = requests.get(
            url,
            headers={
                "Bearer": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbiI6ImIxZGY2MjdmLTFlMWUtNGMwYy1iZmNhLWEyYzA0NzZkMGE4NiIsImV4cGlyZXMiOjE2ODIzNDQ2OTR9.OkhErquMnsEAp6e_-iuGyqu7_Xz37hdXFbG48TZBYpE",
                "Content-Type": "application/json",
            },
        )
        # data = json.loads(resp.content)
        print(resp.status_code)
        print(resp.content)
