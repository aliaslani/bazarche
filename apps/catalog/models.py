from django.core.validators import MinValueValidator
from django.db import models
from decimal import Decimal

from django.urls import reverse

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

    def in_category(self, slug: str):
        return self.filter(category__slug=slug)

    def for_listing(self):
        return self.select_related('category').only('id','title','slug','price',
                                             'stock','category__name','category__slug')
class Product(TimeStampedModel):
    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name='products')
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
        constraints = [
            models.CheckConstraint(
                condition=models.Q(price__gte=0), name='product_price_non_negative'
            ),
        ]

    def __str__(self):
            return self.title

    def get_absolute_url(self):
            return reverse('catalog: product-detail', kwargs={'slug':self.slug})

    @property
    def is_available(self):
        return self.is_active and self.stock > 0

