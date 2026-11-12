#Thin View
from typing import Any

from django.core.paginator import _SupportsPagination
from django.db.models import QuerySet
from django.shortcuts import render
from django.views.generic import DetailView, ListView
from django.views.generic.list import _M

from apps.catalog.selectors import product_get, product_list, category_list


class ProductListView(ListView):
    template_name = 'catelog/product_list.html'
    context_object_name = 'products'
    paginate_by = 12

    def get_queryset(self):
        return product_list(category_slug=self.kwargs.get('category_slug'),
                search=self.request.Get.get('q').strip(),)


    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['categories'] = category_list()
        ctx['q'] = self.request.GET.get('q')
        return ctx


class ProductDetailView(DetailView):
    template_name = 'categlog/product_detail.html'
    context_object_name = 'product'
    def get_object(self, queryset=None):
        return product_get(slug=self.kwargs.get('slug'))



