from django.urls import path
from apps.order.views import buy_now
app_name = 'order'
urlpatterns = [
    path('buy/<int:product_id>/', buy_now, name='buy-now'),
]