import json
from datetime import datetime, timedelta

import requests
from api.exceptions import ObtainAccessTokenError
from api.models import AccessToken
from django.conf import settings


def get_access_token() -> str:
    """Get valid token from DB or obtain new one"""
    access_token = AccessToken.objects.all().order_by("-created_at").first()
    if not access_token or access_token.is_expired:
        return get_new_access_token()

    return access_token.value


def get_new_access_token() -> str:
    """Obtain and save new token in the DB. Set expiration time to 5 minutes."""
    resp = requests.post(
        f"{settings.APPLIFTING_API_BASE_URL}auth",
        headers={"Bearer": settings.APPLIFTING_API_REFRESH_TOKEN},
    )
    now = datetime.now()

    if resp.status_code != 201:
        raise ObtainAccessTokenError(resp.text)

    access_token = AccessToken.objects.create(
        value=json.loads(resp.content)["access_token"],
        expiration=now + timedelta(minutes=5),
    )
    access_token.save()

    return access_token.value
