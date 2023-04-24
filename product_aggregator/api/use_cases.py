import json
from datetime import datetime, timedelta

import requests
from django.conf import settings

from products.models import Product

from .models import AccessToken


def register_product(product: Product):
    # TODO .env or settings.py
    url = "https://python.exercise.applifting.cz/api/v1/products/register"
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
        raise Exception(resp.text)  # TODO custom


def get_access_token() -> str:
    access_token = AccessToken.objects.all().order_by("-created_at").first()
    if not access_token or access_token.is_expired:
        return get_new_access_token()

    return access_token.value


def get_new_access_token() -> str:
    # TODO url env var
    resp = requests.post(
        "https://python.exercise.applifting.cz/api/v1/auth",
        headers={"Bearer": settings.APPLIFTING_API_REFRESH_TOKEN},
    )
    now = datetime.now()

    if resp.status_code != 201:
        raise Exception(resp.text)  # TODO custom

    access_token = AccessToken.objects.create(
        value=json.loads(resp.content)["access_token"],
        expiration=now + timedelta(minutes=5),
    )
    access_token.save()

    return access_token.value
