from django.db import models
from django.conf import settings
from django.db.models.signals import pre_save
from django.contrib import auth

from siparisver.utils import unique_slug_generator


class User(auth.models.AbstractUser):
    selected_address = models.ForeignKey('Address',
                                         null=True,
                                         blank=True,
                                         on_delete=models.SET_NULL,
                                         related_name='profile')

    def __str__(self):
        return self.username


class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class ProductCategory(TimeStampedModel):
    title = models.CharField(max_length=256)

    def __str__(self):
        return self.title

    def get_products(self):
        return self.products.order_by('created_at')


class Product(TimeStampedModel):
    title = models.CharField(max_length=256)
    content = models.CharField(max_length=256, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    discount_price = models.DecimalField(
        max_digits=6, decimal_places=2, null=True, blank=True
    )
    category = models.ForeignKey(
        ProductCategory, related_name='products',
        on_delete=models.SET_NULL, null=True, blank=True
    )
    slug = models.SlugField(null=True, blank=True)

    def __str__(self):
        return self.title


class Order(TimeStampedModel):
    PAYMENT_CHOICES = (
        ('credit_card', 'Credit Card'),
        ('cash', 'Cash')
    )
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    start_date = models.DateTimeField(auto_now_add=True)
    ordered_date = models.DateTimeField(null=True, blank=True)
    ordered = models.BooleanField(default=False)
    shipping_address = models.ForeignKey(
        'Address',
        null=True,
        blank=True,
        on_delete=models.SET_NULL
    )
    payment_option = models.CharField(
        choices=PAYMENT_CHOICES,
        null=True,
        blank=True,
        max_length=255
    )

    def __str__(self):
        return self.user.username

    def get_total_price(self):
        total = 0
        for order_item in self.items.all():
            total += order_item.get_final_price()
        return total


class OrderItem(TimeStampedModel):
    order = models.ForeignKey(
        Order, related_name='items', on_delete=models.CASCADE
    )
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return f'{self.quantity} of {self.product}'

    def get_total_price(self):
        return self.quantity * self.product.price

    def get_total_discount_price(self):
        return self.quantity * self.product.discount_price

    def get_final_price(self):
        if self.product.discount_price:
            return self.get_total_discount_price()
        return self.get_total_price()


class Address(TimeStampedModel):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE,
                             related_name='addresses')
    title = models.CharField(max_length=255)
    text = models.TextField()

    def __str__(self):
        return self.title


def slug_generator(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)


pre_save.connect(slug_generator, sender=Product)
