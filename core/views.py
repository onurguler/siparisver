from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import (
    ListView, View, CreateView, UpdateView, DeleteView)
from django.contrib import messages

from .models import Product, ProductCategory, Order, OrderItem, Address


class ProductListView(ListView):
    model = ProductCategory
    context_object_name = 'categories'
    template_name = 'products/product_list.html'

    def get_queryset(self):
        queryset = super().get_queryset().order_by('created_at')
        return queryset


class CheckoutView(LoginRequiredMixin, View):

    def get(self, *args, **kwargs):
        order_qs = Order.objects.filter(user=self.request.user, ordered=False)

        if not order_qs.exists():
            return redirect('core:order_summary')

        order = order_qs[0]
        order_items = order.items.all()

        if order_items.count() < 1:
            return redirect('core:order_summary')

        context = {'order': order, 'order_items': order_items}

        return render(self.request, 'checkout/checkout.html', context)

    def post(self, *args, **kwargs):
        order_qs = Order.objects.filter(user=self.request.user, ordered=False)

        if not order_qs.exists():
            return redirect('core:order_summary')

        order = order_qs[0]
        order_items = order.items.all()

        if order_items.count() < 1:
            return redirect('core:order_summary')

        if not self.request.user.selected_address:
            messages.error(
                self.request,
                'Adres seçimi yapmadınız. Lütfen bir adres seçin.'
            )
            return redirect('core:checkout')

        payment_option = self.request.POST.get('payment_option')

        if payment_option != Order.PAYMENT_CHOICES[0][0] and payment_option != Order.PAYMENT_CHOICES[1][0]:
            messages.error(
                self.request, 'Lütfen geçerli bir ödeme yöntemi seçin.')
            return redirect('core:checkout')

        order.payment_option = payment_option
        order.shipping_address = self.request.user.selected_address
        order.ordered = True

        order.save()

        messages.success(
            self.request, 'Siparişiniz alınmıştır. Afiyet olsun :)')

        return redirect('core:checkout')


class AddressListView(LoginRequiredMixin, ListView):
    model = Address
    context_object_name = 'addresses'
    template_name = 'addresses/address_list.html'

    def get_queryset(self):
        qs = self.request.user.addresses.order_by('-updated_at')
        return qs


class AddressCreateView(LoginRequiredMixin, CreateView):
    model = Address
    fields = ('title', 'text')
    success_url = reverse_lazy('core:address_list')
    template_name = 'addresses/create_address.html'

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.save()

        self.request.user.selected_address = self.object
        self.request.user.save()

        return redirect(self.get_success_url())


class AddressUpdateView(LoginRequiredMixin, UpdateView):
    model = Address
    fields = ('title', 'text')
    success_url = reverse_lazy('core:address_list')
    template_name = 'addresses/update_address.html'

    def get_queryset(self):
        qs = super().get_queryset().filter(user=self.request.user)
        return qs


class AddressDeleteView(LoginRequiredMixin, DeleteView):
    model = Address
    success_url = reverse_lazy('core:address_list')
    template_name = 'addresses/address_confirm_delete.html'

    def get_queryset(self):
        qs = super().get_queryset().filter(user=self.request.user)
        return qs


# TODO: Order List view: Kullanıcının siparişlerini listele
class OrderListView(LoginRequiredMixin, ListView):
    model = Order


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


@login_required
def set_selected_address(request, address_id):
    address = get_object_or_404(Address, user=request.user, pk=address_id)
    request.user.selected_address = address
    request.user.save()
    return redirect('core:address_list')


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
