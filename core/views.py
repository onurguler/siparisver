from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView
from django.contrib import messages

from .models import Product, ProductCategory, Order, OrderItem


class ProductListView(ListView):
    model = ProductCategory
    context_object_name = 'categories'
    template_name = 'products/product_list.html'

    def get_queryset(self):
        queryset = super().get_queryset().order_by('created_at')
        return queryset


def index(request):
    return render(request, 'index.html')


@login_required
def add_to_cart(request, slug):
    product = get_object_or_404(Product, slug=slug)
    order, created = Order.objects.get_or_create(
        user=request.user, ordered=False)
    order_item_queryset = order.items.filter(product=product)

    if order_item_queryset.exists():
        order_item = order_item_queryset[0]
        order_item.quantity += 1
        order_item.save()
    else:
        OrderItem.objects.create(order=order, product=product)

    messages.success(request, 'Ürün sepetinize eklenmiştir.')
    return redirect('core:order_summary')


@login_required
def order_summary(request):
    order = None
    order_qs = Order.objects.filter(user=request.user, ordered=False)

    if order_qs.exists():
        order = order_qs[0]

    context = {'order': order}

    return render(request, 'orders/order_summary.html', context)


@login_required
def remove_from_cart(request, slug):
    product = get_object_or_404(Product, slug=slug)
    order_qs = Order.objects.filter(user=request.user, ordered=False)

    if not order_qs.exists():
        # TODO: failure message => aktif sepetiniz henüz yoktur.
        return redirect('core:order_summary')

    order = order_qs[0]
    order_item_qs = order.items.filter(product=product)

    if not order_item_qs.exists():
        # TODO: failure message => Ürün sepetinizde bulunmamaktadır.
        return redirect('core:order_summary')

    order_item = order_item_qs[0]
    order_item.delete()

    messages.success(request, 'Ürün sepetinizden kaldırılmıştır.')
    return redirect('core:order_summary')


@login_required
def remove_single_item_from_cart(request, slug):
    product = get_object_or_404(Product, slug=slug)
    order_qs = Order.objects.filter(user=request.user, ordered=False)

    if not order_qs.exists():
        # TODO: failure message => aktif sepetiniz henüz yoktur.
        return redirect('core:order_summary')

    order = order_qs[0]
    order_item_qs = order.items.filter(product=product)

    if not order_item_qs.exists():
        # TODO: failure message => Ürün sepetinizde bulunmamaktadır.
        return redirect('core:order_summary')

    order_item = order_item_qs[0]

    if order_item.quantity > 1:
        order_item.quantity -= 1
        order_item.save()
    else:
        order_item.delete()

    return redirect('core:order_summary')


@login_required
def empty_cart(request):
    order_qs = Order.objects.filter(user=request.user, ordered=False)

    if order_qs.exists():
        order = order_qs[0]
        order.delete()

    messages.success(request, 'Sepetiniz boşaltılmıştır.')
    return redirect('core:order_summary')


"""
# TODO: Session based cart
# Session Tabanlı Sepet Denemesi
# Arka arkaya login olmamışken sepete ekleyip tekrar login olunduğunda
# Login olurken response dönmüyor refresh etmek gerekiyor
# Bu soruna daha sonra bak


def view_cart(request):
    cart = request.session.get('cart', {})

    order = []
    total_price = 0

    for key, value in cart.items():
        product = Product.objects.get(slug=key)
        order.append({'product': product, 'quantity': value})
        total_price += product.price

    context = {'order': order, 'total_price': total_price}

    return render(request, 'cart/cart.html', context)


def add_to_cart_session(request, slug):
    product = get_object_or_404(Product, slug=slug)
    cart = request.session.get('cart', {})

    cart[product.slug] = cart.get(product.slug, 0) + 1

    request.session['cart'] = cart

    messages.success(request, 'Ürün sepetinize eklenmiştir.')

    return redirect('core:cart')


def remove_from_cart_session(request, slug):
    product = get_object_or_404(Product, slug=slug)
    cart = request.session.get('cart', {})

    del cart[product.slug]

    request.session['cart'] = cart

    messages.success(request, 'Ürün sepetinizden kaldırılmıştır.')

    return redirect('core:cart')


def remove_single_item_from_cart_session(request, slug):
    # product = get_object_or_404(Product, slug=slug)
    cart = request.session.get('cart', {})

    if slug in cart:
        cart[slug] -= 1

        if cart[slug] <= 0:
            del cart[slug]

        request.session['cart'] = cart

    return redirect('core:cart')


def empty_cart_session(request):
    del request.session['cart']
    messages.success(request, 'Sepetiniz boşaltılmıştır.')
    return redirect('core:cart')
"""
