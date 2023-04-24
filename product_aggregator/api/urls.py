from django.urls import path

from .views import product_offers_list, products_detail, products_list

urlpatterns = [
    path("products/", products_list, name="products-list"),
    path("products/<uuid:product_id>/", products_detail, name="products-detail"),
    path("<uuid:product_id>/offers/", product_offers_list, name="product-offers-list"),
]
