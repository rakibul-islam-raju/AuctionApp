from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.forms import widgets

from .models import AuctionProduct


class UserLoginForm(forms.Form):
    email = forms.EmailField(required=True)
    password = forms.CharField(widget=forms.PasswordInput())


class CreateAutionItemForm(forms.ModelForm):
    class Meta:
        model = AuctionProduct
        exclude = [
            "created_at",
            "is_active",
            "added_by",
        ]

        widgets = {
            "product_description": forms.Textarea(
                attrs={
                    "rows": "5",
                },
            ),
            "end_date": forms.DateInput(
                attrs={
                    "type": "date",
                },
            ),
        }
