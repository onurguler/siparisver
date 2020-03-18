from django.urls import path

from . import views


app_name = 'core'

urlpatterns = [
    path('', views.index, name='index'),
    path('products/', views.ProductListView.as_view(), name='product_list'),
    path('order-summary/', views.order_summary, name='order_summary'),
    path('add-to-cart/<slug:slug>',
         views.add_to_cart, name='add_to_cart'),
    path('remove-from-cart/<slug:slug>',
         views.remove_from_cart, name='remove_from_cart'),
    path('remove-single-item-from-cart/<slug:slug>',
         views.remove_single_item_from_cart,
         name='remove_single_item_from_cart'),
    path('empty-cart/', views.empty_cart, name='empty_cart'),
]
