from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from django.views.generic import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ObjectDoesNotExist

from products.models import Product
from .models import Order, OrderItem


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

    # TODO: success message => Ürün sepetinize eklenmiştir
    return redirect('orders:order_summary')


class OrderSummaryView(LoginRequiredMixin, View):
    def get(self, *args, **kwargs):
        try:
            order = Order.objects.get(user=self.request.user, ordered=False)
        except ObjectDoesNotExist:
            return redirect('/')

        context = {'order': order}
        return render(self.request, 'orders/order_summary.html', context)


@login_required
def order_summary(request):
    try:
        order = Order.objects.get(user=request.user, ordered=False)
        context = {'order': order}
        return render(request, 'orders/order_summary.html', context)
    except ObjectDoesNotExist:
        # TODO: failure message => Sepetiniz boştur.
        return redirect(request.path)


@login_required
def remove_from_cart(request, slug):
    product = get_object_or_404(Product, slug=slug)
    order_qs = Order.objects.filter(user=request.user, ordered=False)

    if not order_qs.exists():
        # TODO: failure message => aktif sepetiniz henüz yoktur.
        return redirect(request.path)

    order = order_qs[0]
    order_item_qs = order.items.filter(product=product)

    if not order_item_qs.exists():
        # TODO: failure message => Ürün sepetinizde bulunmamaktadır.
        return redirect(request.path)

    order_item = order_item_qs[0]
    order_item.delete()

    # TODO: success message => Ürün sepetinizden kaldırılmıştır
    return redirect('orders:order_summary')


@login_required
def remove_single_item_from_cart(request, slug):
    product = get_object_or_404(Product, slug=slug)
    order_qs = Order.objects.filter(user=request.user, ordered=False)

    if not order_qs.exists():
        # TODO: failure message => aktif sepetiniz henüz yoktur.
        return redirect(request.path)

    order = order_qs[0]
    order_item_qs = order.items.filter(product=product)

    if not order_item_qs.exists():
        # TODO: failure message => Ürün sepetinizde bulunmamaktadır.
        return redirect(request.path)

    order_item = order_item_qs[0]

    if order_item.quantity > 1:
        order_item.quantity -= 1
        order_item.save()
    else:
        order_item.delete()

    return redirect('orders:order_summary')
