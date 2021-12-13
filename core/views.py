from django.contrib import messages
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password

from .forms import UserLoginForm
from .models import User


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

    context = {
        "form": UserLoginForm(),
    }
    return render(request, "login.html", context)


@login_required(login_url="login")
def home_page(request):
    return render(request, "home.html")
