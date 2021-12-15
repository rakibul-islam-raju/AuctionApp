from datetime import date
from django.contrib import messages
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password

from .forms import UserLoginForm, CreateAutionItemForm
from .models import ProductBid, User, AuctionProduct


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
            print("error======", form.errors)
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
    context = {}
    # get the product
    product = get_object_or_404(AuctionProduct, pk=pk)
    # check if auction end date is not expired
    expired = False
    if product.end_date >= date.today():
        expired = False
    else:
        expired = True

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
        user_bid = product_bids.filter(user=request.user).first()
        context = {
            "product": product,
            "product_bids": product_bids,
            "user_bid": user_bid,
            "expired": expired,
        }
    return render(request, "product_details.html", context)
