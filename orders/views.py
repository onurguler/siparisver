from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from django.views.generic import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ObjectDoesNotExist

from products.models import Product
from .models import Order, OrderItem


@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    order, created = Order.objects.get_or_create(
        user=request.user, ordered=False)
    order_item_queryset = order.items.filter(product=product)

    if order_item_queryset.exists():
        order_item = order_item_queryset[0]
        order_item.quantity += 1
        order_item.save()
        return redirect('products:product_list')

    OrderItem.objects.create(order=order, product=product)
    return redirect('products:product_list')


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
        return redirect(request.path)
