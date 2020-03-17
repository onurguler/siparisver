from django.shortcuts import render
from django.views.generic import ListView

from .models import ProductCategory, Product


class ProductListView(ListView):
    model = ProductCategory
    context_object_name = 'categories'
    template_name = 'products/product_list.html'

    def get_queryset(self):
        queryset = super().get_queryset().order_by('name')
        return queryset
