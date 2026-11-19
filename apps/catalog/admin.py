from django.contrib import admin
from apps.catalog.models import Category, Product


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {"slug": ["name"]}



@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['title','stock', 'price', 'is_active', 'category']
    list_filter = ['is_active', 'category']
    list_editable = ['price', 'stock','is_active']
    search_fields = ['title']
    prepopulated_fields = {'slug': ['title']}
    list_select_related = ['category']