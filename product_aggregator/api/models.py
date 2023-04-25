from django.db import models
from django.utils import timezone


class AccessToken(models.Model):
    value = models.CharField(max_length=512)
    expiration = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def is_expired(self):
        return timezone.now() > self.expiration
