from django.urls import path

from . import views

app_name = 'order'

urlpatterns = [
    path('add-to-cart/<int:product_id>',
         views.add_to_cart, name='add_to_cart'),
    path('summary/', views.order_summary, name='order_summary'),
]
