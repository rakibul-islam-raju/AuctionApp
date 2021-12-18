from django.urls import reverse
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import Max


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

    def get_absolute_url(self):
        return reverse("product_details", kwargs={"pk": self.pk})

    @property
    def get_top_bid(self):
        result = ProductBid.objects.filter(product=self)
        result = result.aggregate(Max("bid_price"))
        return result

    class Meta:
        ordering = ["-created_at"]


class ProductBid(models.Model):
    product = models.ForeignKey(
        AuctionProduct, on_delete=models.CASCADE, related_name="product_bid"
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="product_bid")
    bid_price = models.DecimalField(max_digits=8, decimal_places=2)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.product.product_name

    class Meta:
        ordering = ["-created_at"]
