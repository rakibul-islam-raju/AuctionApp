from django.urls import path

from django.contrib.auth.views import LogoutView

from .views import home_page, login_page, create_auction_item_page

urlpatterns = [
    path("", home_page, name="home"),
    path("login/", login_page, name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("new-auction-item/", create_auction_item_page, name="create_auction_item"),
]
