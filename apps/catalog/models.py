from django.core.validators import MinValueValidator
from django.db import models
from decimal import Decimal
from apps.core.models import TimeStampedModel


class Category(TimeStampedModel):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=120, unique=True, allow_unicode=True)

    class Meta:
        ordering = ['name']
        verbose_name = ' دسته بندی'
        verbose_name_plural = 'دسته بندی‌ها'

    def __str__(self):
        return self.name

class ProductQuerySet(models.QuerySet):
    def active(self):
        return self.filter(is_active=True)

    def in_stock(self):
        return self.filter(stock__gt=0)

    def search(self, term: str):
        return self.filter(title__icontains=term) if term else self


class Product(TimeStampedModel):
    category: models.ForeignKey(Category, on_delete=models.PROTECT, related_name='products')
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=120, unique=True, allow_unicode=True)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=12, decimal_places=0, validators=[MinValueValidator(Decimal('0'), 'قیمت نمی تواند صفر یا منفی باشد')])
    stock = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    objects = ProductQuerySet.as_manager()


    class Meta:
        ordering = ['-created_at', 'title']
        verbose_name = 'محصول'
        verbose_name_plural = 'محصولات'

