from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.views.decorators.http import require_POST
from apps.order.services import order_place
from apps.core.exceptions import ApplicationError
from django.contrib import messages
from django.shortcuts import redirect

@login_required
@require_POST
def buy_now(request, product_id):
    try:
        qty = max(1, int(request.POST.get('quantity')))
    except ValueError:
        qty = 1

    try:
        order = order_place(user=request.user, items={product_id: qty})
    except ApplicationError as exc:
        messages.error(request, str(exc))
        return redirect(('catalog:product-list'))

    messages.success(request, f"Order #{order.pk} placed successfully")
    return redirect("catalog:product-list")


