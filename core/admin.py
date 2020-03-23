from django.contrib import admin

from .models import ProductCategory, Product, OrderItem, Order, User, Address


class OrderItemInline(admin.TabularInline):
    model = OrderItem


class OrderAdmin(admin.ModelAdmin):
    inlines = [OrderItemInline]


admin.site.register(ProductCategory)
admin.site.register(Product)
admin.site.register(OrderItem)
admin.site.register(Order, OrderAdmin)
admin.site.register(User)
admin.site.register(Address)
