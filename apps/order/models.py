from django.db import models
from django.conf import settings
from django.urls import reverse

from apps.catalog.models import Product
from apps.core.models import TimeStampedModel


class Order(TimeStampedModel):
    class Status(models.TextChoices):
        PENDING = "pending", "در انتظار پرداخت"
        PAID = 'paid', 'پرداخت شده'
        SHIPPED = 'shipped'
        CANCELED = 'canceled'
        DELIVERED = 'delivered', 'تحویل شده'
    TRANSITION = {
        Status.PENDING: {Status.PAID, Status.CANCELED},
        Status.PAID: {Status.SHIPPED, Status.CANCELED},
        Status.SHIPPED: {Status.DELIVERED},
        Status.CANCELED: set(),
    }
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT,
                             related_name='orders')
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PENDING)
    total = models.DecimalField(max_digits=14, decimal_places=0, default=0)
    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Order #{self.pk} ({self.get_status_display()}"

    def get_absolute_url(self):
        reverse("order: detail", args=[self.pk])

    def can_transition_to(self, new_status):
        return new_status in self.TRANSITION[self.status]

    @property
    def is_cacelable_by_customer(self):
        return self.status == self.Status.PENDING

class OrderItem(TimeStampedModel):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.PROTECT, related_name="+")
    unit_price = models.DecimalField(max_digits=12, decimal_places=0)
    quantity = models.PositiveSmallIntegerField()

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['order', 'product'],
                name='uniq_order_product'
            ),
            models.CheckConstraint(
                condition=models.Q(quantity__gt=0),
                name='item_qty_positive'
            )

        ]
    @property
    def line_total(self):
        return self.unit_price * self.quantity