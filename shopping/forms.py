from django import forms
from .models import Address


class CheckoutForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = "__all__"
        # or defined the fields by specifically
        # fields = ['name', 'category', 'description', 'price', 'inventory']
