from rest_framework.serializers import ModelSerializer

from products.models import Offer, Product


class ProductSerializer(ModelSerializer):
    class Meta:
        model = Product
        fields = ["id", "name", "description"]


class OfferSerializer(ModelSerializer):
    class Meta:
        model = Offer
        fields = ["id", "price", "items_in_stock"]
