from datetime import datetime

from django.db import models


class AccessToken(models.Model):
    value = models.CharField(max_length=512)
    expiration = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def is_expired(self):
        return datetime.now() > self.expiration
