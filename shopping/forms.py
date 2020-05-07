from django import forms
from django.forms import TextInput, Select

from .models import Address
from localflavor.us.us_states import CONTIGUOUS_STATES, US_STATES


class CheckoutForm(forms.Form):
    shipping_first_name = forms.CharField(required=False)
    shipping_last_name = forms.CharField(required=False)
    shipping_street_address = forms.CharField(required=False)
    shipping_apartment_address = forms.CharField(required=False)
    shipping_city = forms.CharField(required=False)
    shipping_state = forms.ChoiceField(choices=CONTIGUOUS_STATES, required=False)
    shipping_state.widget.attrs.update({'class': 'custom-select d-block w-100'})
    shipping_zipcode = forms.CharField(required=False)
    use_default_shipping = forms.BooleanField(required=False)
    set_default_shipping = forms.BooleanField(required=False)

    # same_billing_address = forms.BooleanField(required=False, widget=forms.CheckboxInput())
    # use_default_shipping = forms.BooleanField(required=False)
    # set_default_billing = forms.BooleanField(required=False)
    # use_default_billing = forms.BooleanField(required=False)

    # class Meta:
    #     model = Address
    #     fields = [
    #         'first_name', 'last_name', 'street_address', 'apartment_address', 'city', 'state', 'zipcode', 'default'
    #     ]
    #     widgets = {
    #         'street_address': TextInput(attrs={'placeholder': '123 Main St'}),
    #         'apartment_address': TextInput(attrs={'placeholder': 'Apartment or suite'}),
    #         'city': TextInput(attrs={'placeholder': 'Pittsburgh'}),
    #     }


class PaymentForm(forms.Form):
    billing_first_name = forms.CharField(required=False)
    billing_last_name = forms.CharField(required=False)
    billing_street_address = forms.CharField(required=False)
    billing_apartment_address = forms.CharField(required=False)
    billing_city = forms.CharField(required=False)
    billing_state = forms.ChoiceField(choices=CONTIGUOUS_STATES, required=False)
    billing_state.widget.attrs.update({'class': 'custom-select d-block w-100'})
    billing_zipcode = forms.CharField(required=False)
    use_default_billing = forms.BooleanField(required=False)
    same_billing_address = forms.BooleanField(required=False, widget=forms.CheckboxInput())
    set_default_billing = forms.BooleanField(required=False)


class CouponForm(forms.Form):
    code = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Promo Code',
                'aria-label': 'Recipient\'s username',
                'aria-describedby': 'basic-addon2'
            }
        )
    )


class ExchangeForm(forms.Form):
    ref_code = forms.CharField()
    message = forms.CharField(widget=forms.Textarea(attrs={
        'rows': 5
    }))
    email = forms.EmailField()


class RefundForm(forms.Form):
    ref_code = forms.CharField()
    message = forms.CharField(widget=forms.Textarea(attrs={
        'rows': 5
    }))
    email = forms.EmailField()
