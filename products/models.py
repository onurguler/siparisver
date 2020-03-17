from django.db import models

from siparisver.utils import unique_slug_generator
from django.db.models.signals import pre_save


class ProductCategory(models.Model):
    title = models.CharField(max_length=256)

    def __str__(self):
        return self.title

    def get_products(self):
        return self.products.order_by('title')


class Product(models.Model):
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


def slug_generator(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)


pre_save.connect(slug_generator, sender=Product)
