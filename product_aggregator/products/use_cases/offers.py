import uuid

from products.models import Offer, Product


def update_product_offer(data: dict[str | int]):
    """Update existing `Offer` entry"""
    offer = Offer.objects.get(id=data["id"])
    offer.price = data["price"]
    offer.items_in_stock = data["items_in_stock"]
    offer.save()


def add_new_product_offer(data: dict[str | int], product: Product):
    """Create new `Offer` entry"""
    offer = Offer.objects.create(
        id=uuid.UUID(data["id"]),
        price=data["price"],
        items_in_stock=data["items_in_stock"],
        product=product,
    )
    offer.save()


def remove_old_offers(offer_ids: list[str]):
    """Remove old `Offer` entries"""
    for offer_id in offer_ids:
        offer = Offer.objects.get(id=offer_id)
        offer.delete()
