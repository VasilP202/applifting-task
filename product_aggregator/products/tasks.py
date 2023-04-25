import uuid

from api.use_cases.applifting import get_product_offers

from product_aggregator.celery import app

from .models import Product
from .use_cases.offers import (
    add_new_product_offer,
    remove_old_offers,
    update_product_offer,
)


@app.task
def update_product_offers():
    """Check for changes in product offers and update data in the DB."""
    for product in Product.objects.all():
        product_offers = get_product_offers(str(product.id))
        if product_offers is not None:
            offer_ids = [o.id for o in product.offers.all()]
            for offer in product_offers:
                if uuid.UUID(offer["id"]) in offer_ids:
                    # Offers are updated every minute
                    update_product_offer(offer)
                    offer_ids.remove(uuid.UUID(offer["id"]))
                else:
                    # Create new product offer
                    add_new_product_offer(offer, product)

            if offer_ids:
                # Old offers are removed from the DB
                remove_old_offers(offer_ids)
