from django.db.models import QuerySet
from django.shortcuts import get_object_or_404
from apps.catalog.models import Category, Product


def product_list(category_slug: str | None = None, search:str = '') -> QuerySet[Product]:
    qs = Product.objects.active().for_listing().search(search)
    if category_slug:
        qs = qs.in_category(category_slug)
    return qs

def product_get(slug:str) -> Product:
    return get_object_or_404(Product.objects.active().select_related('category'), slug=slug)

def category_list() -> QuerySet[Category]:
    return Category.objects.active()



