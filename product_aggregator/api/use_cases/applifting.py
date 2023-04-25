import json
from typing import Optional

import requests
from django.conf import settings

from api.exceptions import ProductRegistrationError
from products.models import Product

from .auth import get_access_token


def register_product(product: Product):
    """Register new product via Applifting API"""
    url = f"{settings.APPLIFTING_API_BASE_URL}products/register"
    product_data = {
        "id": str(product.id),
        "name": product.name,
        "description": product.description,
    }
    resp = requests.post(
        url,
        json=product_data,
        headers={
            "Bearer": get_access_token(),
            "Content-Type": "application/json",
        },
    )
    if resp.status_code != 201:
        raise ProductRegistrationError(resp.text)


def get_product_offers(product_id: str) -> Optional[list[dict]]:
    """Obtain offers for a single product"""
    resp = requests.get(
        f"{settings.APPLIFTING_API_BASE_URL}products/{product_id}/offers",
        headers={
            "Bearer": get_access_token(),
        },
    )
    if resp.status_code == 200:
        return json.loads(resp.content)
