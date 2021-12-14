from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    email = models.EmailField(unique=True)


class AuctionProduct(models.Model):
    product_name = models.CharField(max_length=200)
    product_photo = models.ImageField(upload_to="products/")
    minimum_bid_price = models.DecimalField(max_digits=8, decimal_places=2)
    product_description = models.TextField()
    end_date = models.DateField()

    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    added_by = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="auction_products"
    )

    def __str__(self):
        return self.product_name
