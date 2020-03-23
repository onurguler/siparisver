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
    path('checkout/', views.CheckoutView.as_view(), name='checkout'),
    path('addresses/', views.AddressListView.as_view(), name='address_list'),
    path('create-address/',
         views.AddressCreateView.as_view(), name='create_address'),
    path('update-address/<int:pk>/',
         views.AddressUpdateView.as_view(), name='update_address'),
    path('delete-address/<int:pk>/',
         views.AddressDeleteView.as_view(), name='delete_address'),
    path('set-selected-address/<int:address_id>/',
         views.set_selected_address, name='set_selected_address'),
    # Session based cart urls
    # path('cart/', views.view_cart, name='cart'),
    # path('add-to-cart-session/<slug:slug>',
    #     views.add_to_cart_session, name='add_to_cart_session'),
    # path('remove-from-cart-session/<slug:slug>',
    #     views.remove_from_cart_session, name='remove_from_cart_session'),
    # path('remove-single-item-from-cart-session/<slug:slug>',
    #     views.remove_single_item_from_cart_session,
    #     name='remove_single_item_from_cart_session'),
    # path('empty-cart-session/',
    #     views.empty_cart_session, name='empty_cart_session'),
]
