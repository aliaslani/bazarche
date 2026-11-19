from django.core.exceptions import PermissionDenied
from django.db import transaction

from apps.order.models import Order, Product, OrderItem
from django.db.models import F
from apps.core.exceptions import EmptyOrderError, InsufficientStockError
from apps.order.exceptions import OrderError, OrderStatusError

class ProductUnavailableError:
    pass

@transaction.atomic
def order_place(user, items:dict[int, int]) -> Order:
    items = {pid: qty for pid, qty in items.items() if qty > 0}
    if not items:
        raise EmptyOrderError("Your order has no items.")

    products = {
        p.id: p for p in Product.objects.select_for_update(

    ).active().filter(id__in=items).order_by('id')
    }

    order = Order.objects.create(user=user)
    order_items, total = [], 0
    for product_id, qty in items.items():
        product = products.get(product_id)
        if product is None:
            raise ProductUnavailableError(f"Product {product_id} is not available")

        if product.stock < qty:
            raise InsufficientStockError(product.name, product.stock)

        order_items.append(OrderItem(order=order, product=product, unit_price=product.price, quantity=qty))
        total += product.price * qty

    OrderItem.objects.bulk_create(order_items)
    order.total = total
    order.save(update_fields=['total', 'updated_at'])
    transaction.on_commit(lambda: print(f"Order {order.pk} placed by {user.pk}"))

    return order

@transaction.atomic
def order_cancel(*, order, by_user):
    order = Order.objects.select_for_update().get(pk=order.pk)
    is_owner = order.user_id == by_user
    if not (is_owner or by_user.is_staff):
        raise PermissionDenied("You can not cancel this order")
    if not order.can_transition_to(Order.Status.CANCELED):
        raise OrderStatusError(f"A {order.get_status_display().lower} order cannot be canceled")

    if not by_user.is_staff and not order.is_cacelable_by_customer:
        raise OrderStatusError("Paid orders can only be canceled by support")

    for item in order.items.all():
        Product.objects.filter(pk=item.product_id).update(stock=F('stock') + item.quantity)
        order.status = Order.Status.CANCELED
        order.save(update_fields=['status','updated_at'])


