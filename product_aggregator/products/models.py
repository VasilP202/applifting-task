import uuid

from django.db import models


class Product(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    name = models.CharField(max_length=127)
    description = models.CharField(max_length=511)

    def __str__(self) -> str:
        return self.name


class Offer(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="offers"
    )

    price = models.IntegerField()
    items_in_stock = models.IntegerField()
