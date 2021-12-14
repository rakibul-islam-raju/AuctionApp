from django.contrib import messages
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password

from .forms import UserLoginForm, CreateAutionItemForm
from .models import User, AuctionProduct


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
