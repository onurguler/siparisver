from django.urls import path

from . import views

app_name = 'order'

urlpatterns = [
    path('add-to-cart/<slug:slug>',
         views.add_to_cart, name='add_to_cart'),
    path('summary/', views.order_summary, name='order_summary'),
    path('remove-from-cart/<slug:slug>',
         views.remove_from_cart, name='remove_from_cart'),
    path('remove-single-item-from-cart/<slug:slug>',
         views.remove_single_item_from_cart,
         name='remove_single_item_from_cart')
]
