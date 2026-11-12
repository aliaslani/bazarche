from apps.order.models import Order
from apps.core.exceptions import EmptyOrderError

def order_place(user, items:dict[int, int]) -> Order:
    items = {pid: qty for pid, qty in items.items() if qty > 0}
    if not items:
        raise EmptyOrderError("Your order has no items.")


