from django.urls import path
from apps.catalog.views import ProductDetailView, ProductListView
app_name = 'catalog'
urlpatterns = [
    path("", ProductListView.as_view(), name='product-list'),
    path('<str:slug>/', ProductDetailView.as_view(),name='product-detail'),
    path("c/<str:category_slug>/", ProductListView.as_view(), name='category'),
]

