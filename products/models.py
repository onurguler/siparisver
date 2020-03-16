from django.db import models


class ProductCategory(models.Model):
    name = models.CharField(max_length=256)

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=256)
    content = models.CharField(max_length=256)
    description = models.TextField()
    price = models.DecimalField(max_digits=6, decimal_places=2)
    discount_price = models.DecimalField(
        max_digits=6, decimal_places=2, null=True, blank=True
    )
    category = models.ForeignKey(
        ProductCategory, related_name='products',
        on_delete=models.SET_NULL, null=True, blank=True
    )

    def __str__(self):
        return self.name
