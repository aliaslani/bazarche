import random

from django.core.management.base import BaseCommand
from django.db import transaction
from django.utils.text import slugify

from apps.catalog.models import Category, Product


DATA =  {
    "Groceries": ["Saffron", "Basmati Rice", "Black Tea", "Pistachio", "Dates"],
    "Digital": ['USB-C Cable', 'Wireless Mouse', 'Power Bank', 'Headphone'],

}

class Command(BaseCommand):
    help = "Seed Bazarche with demo categories and products"
    @transaction.atomic
    def handle(self, *args, **kwargs):
        for cat_name, products in DATA.items():
            category, _ = Category.objects.get_or_create(
                slug=slugify(cat_name), defaults={'name': cat_name}
            )
            for name in products:
                Product.objects.get_or_create(slug=slugify(
                    name), defaults = {"category": category,
                                  "title":name,
                                  'price':random.randint(5,500) * 10000,
                                  'stock': random.randint(0,20)}
                )

        transaction.on_commit(lambda: self.stdout.write(self.style.SUCCESS(f"Catalog has {Product.objects.count()} products")))


