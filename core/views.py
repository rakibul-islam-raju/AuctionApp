import json
from django.core import serializers
from datetime import datetime
from django.db.models.aggregates import Count
from django.urls import reverse
from django.db.models import Max, fields
from django.db.models.functions import TruncDay
from django.contrib import messages
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password

from .forms import UserLoginForm, CreateAutionItemForm
from .models import ProductBid, User, AuctionProduct
from .decorators import staff_required
from .utils import get_auction_expired_or_not


def login_page(request):
    if request.method == "POST":
        form = UserLoginForm(request.POST or None)
        if form.is_valid():
            email = form.cleaned_data.get("email")
            password = form.cleaned_data.get("password")
            user_instance = User.objects.filter(email=email).first()

            # create new user
            if user_instance is None:
                try:
                    user_instance = User.objects.create(
                        email=email, username=email, password=make_password(password)
                    )
                except:
                    messages.error(request, "Invalid form data.")
                    return redirect("login")

            # user authenticate and login
            user = authenticate(
                request,
                username=user_instance.username,
                password=form.cleaned_data.get("password"),
            )
            if user:
                login(request, user)
                messages.success(request, f"Welcome {user.username}")
                return redirect("home")
            else:
                messages.error(request, "Invalid Credentials.")
        else:
            messages.error(request, "Invalid form data")
            return redirect("home")
    else:
        form = UserLoginForm()

    context = {
        "form": form,
    }
    return render(request, "login.html", context)


@login_required()
def home_page(request):
    products = AuctionProduct.objects.filter(is_active=True)
    context = {
        "products": products,
    }
    return render(request, "home.html", context)


@login_required()
def create_auction_item_page(request):
    if request.method == "POST":
        form = CreateAutionItemForm(request.POST, request.FILES or None)
        if form.is_valid():
            new_item = form.save(commit=False)
            new_item.added_by = request.user
            new_item.save()
            messages.success(request, "Item successfully added.")
            return redirect("home")
    else:
        form = CreateAutionItemForm()

    context = {
        "form": form,
    }
    return render(request, "create_action_item.html", context)


@login_required()
def update_auction_item_page(request, pk):
    auction = get_object_or_404(AuctionProduct, pk=pk)
    # check if requested user is ther owner of this auction
    if auction.added_by == request.user:
        if request.method == "POST":
            form = CreateAutionItemForm(
                request.POST, request.FILES or None, instance=auction
            )
            if form.is_valid():
                new_item = form.save()
                new_item.save()
                messages.success(request, "Item updated added.")
                return redirect(reverse("product_details", kwargs={"pk": auction.pk}))
        else:
            form = CreateAutionItemForm(instance=auction)
    else:
        return redirect("home")

    context = {
        "form": form,
    }
    return render(request, "create_action_item.html", context)


@login_required()
def posted_items_page(request):
    # if user has not items then redirect to create page.
    if request.user.auction_products.count() < 1:
        messages.info(request, "You don't have any items yet. Please create one.")
        return redirect("create_auction_item")
    # get all the items
    items = AuctionProduct.objects.filter(added_by=request.user)
    context = {
        "products": items,
    }
    return render(request, "home.html", context)


@login_required()
def product_details_page(request, pk):
    # get the product
    product = get_object_or_404(AuctionProduct, pk=pk)
    # check if aution not expired
    expired = get_auction_expired_or_not(product.end_date)
    if request.method == "POST":
        # if this auction not expired
        if not expired:
            # get bid price
            bid_price = request.POST.get("bid_price")
            if bid_price:
                # check if this user bid for this product or create new bid
                obj, created = ProductBid.objects.get_or_create(
                    user=request.user,
                    product=product,
                    defaults={"bid_price": bid_price},
                )
                if created:
                    # create new bid
                    messages.success(request, "Your bid was placed successfully.")
                else:
                    # update bid price if used bid was existed
                    obj.bid_price = bid_price
                    obj.save()
                    messages.success(request, "Your bid was updated successfully.")
            else:
                messages.error(request, "Invalid request.")
        else:
            messages.error(request, "This auction has been expired.")

        return redirect("./")
    else:
        product_bids = ProductBid.objects.filter(product=product)
        winner = product_bids.aggregate(Max("bid_price"))
        user_bid = product_bids.filter(user=request.user).first()
        context = {
            "product": product,
            "product_bids": product_bids,
            "winner": winner,
            "user_bid": user_bid,
            "expired": expired,
        }
    return render(request, "product_details.html", context)


"""
=======================
Admin views starts here
=======================
"""


@staff_required()
def dashboard(request):
    today = datetime.today()
    auctions = AuctionProduct.objects.all()
    total_running_auction = auctions.filter(end_date__gte=today)
    finished_auction = auctions.filter(end_date__lt=today)
    # calculate total running auction value
    running_auction_value = 0
    for i in total_running_auction:
        running_auction_value += i.get_top_bid

    # calculate total finished auction value
    finished_auction_value = 0
    for i in finished_auction:
        finished_auction_value += i.get_top_bid

    # count auction by created_at
    auction_data = list(
        auctions.annotate(date=TruncDay("created_at"))
        .values("date")
        .annotate(created_count=Count("id"))
        .order_by("-date")
    )

    context = {
        "total_running_auction": total_running_auction.count(),
        "finished_auction": finished_auction.count(),
        "running_auction_value": running_auction_value,
        "finished_auction_value": finished_auction_value,
        "auctions": auction_data,
    }
    return render(request, "admin/statistics.html", context)


@staff_required()
def auctions(request):
    auctions = AuctionProduct.objects.all().order_by("-created_at")
    context = {
        "auctions": auctions,
    }
    return render(request, "admin/auctions.html", context)


@staff_required()
def auction_details(request, pk):
    product = get_object_or_404(AuctionProduct, pk=pk)
    product_bids = ProductBid.objects.filter(product=product)
    winner = product_bids.aggregate(Max("bid_price"))
    user_bid = product_bids.filter(user=request.user).first()
    expired = get_auction_expired_or_not(product.end_date)
    context = {
        "product": product,
        "product_bids": product_bids,
        "winner": winner,
        "user_bid": user_bid,
        "expired": expired,
    }
    return render(request, "admin/auction_details.html", context)
