from django.contrib.admin.sites import AlreadyRegistered
from django.contrib import admin
from django.apps import apps

from .models import AuctionProduct


@admin.register(AuctionProduct)
class AuctionProductAdmin(admin.ModelAdmin):
    list_display = ["product_name", "minimum_bid_price", "end_date", "is_active"]
    list_filter = ["is_active"]
    search_fields = ["product_name"]


""" 
    register all the models from this app
"""
app_models = apps.get_app_config("core").get_models()
for model in app_models:
    try:
        admin.site.register(model)
    except AlreadyRegistered:
        pass
