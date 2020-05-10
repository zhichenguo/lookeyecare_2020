from allauth.account.forms import AddEmailForm
from django import forms
from localflavor.us.us_states import CONTIGUOUS_STATES, US_STATES


class MyCustomAddEmailForm(AddEmailForm):

    def save(self):
        # Ensure you call the parent class's save.
        # .save() returns an allauth.account.models.EmailAddress object.
        email_address_obj = super(MyCustomAddEmailForm, self).save()

        # Add your own processing here.

        # You must return the original result.
        return email_address_obj


# class EditNameForm(forms.Form):
#     first_name = forms.CharField(required=False)
#     last_name = forms.CharField(required=False)
#
#
# class EditPhoneForm(forms.Form):
#     phone_num = forms.CharField(required=False)


class EditProfileForm(forms.Form):
    first_name = forms.CharField(required=False)
    last_name = forms.CharField(required=False)
    phone_num = forms.CharField(required=False)

    shipping_first_name = forms.CharField(required=False)
    shipping_last_name = forms.CharField(required=False)
    shipping_street_address = forms.CharField(required=False)
    shipping_apartment_address = forms.CharField(required=False)
    shipping_city = forms.CharField(required=False)
    shipping_state = forms.CharField(required=False)
    shipping_zipcode = forms.CharField(required=False)

    billing_first_name = forms.CharField(required=False)
    billing_last_name = forms.CharField(required=False)
    billing_street_address = forms.CharField(required=False)
    billing_apartment_address = forms.CharField(required=False)
    billing_city = forms.CharField(required=False)
    billing_state = forms.CharField(required=False)
    billing_zipcode = forms.CharField(required=False)

    # state_data = {
    #     # 'class': 'custom-select d-block w-100',
    #     'id': 'shipping_state',
    #     'name': 'shipping_state',
    #     'value': '{{ profile.default_shipping_address.state }}'
    # }
    # shipping_state = forms.ChoiceField(choices=CONTIGUOUS_STATES, required=False)
    # shipping_state.widget.attrs.update({
    #     'class': 'custom-select d-block w-100',
    #     'id': 'shipping_state',
    #     'name': 'shipping_state'
    # })

    # billing_state = forms.ChoiceField(choices=CONTIGUOUS_STATES, required=False)
    # billing_state.widget.attrs.update({'class': 'custom-select d-block w-100'})
