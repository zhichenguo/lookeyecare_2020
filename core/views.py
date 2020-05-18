from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import View
from .models import Profile, User
from shopping.models import Address
from .forms import EditProfileForm
from localflavor.us.us_states import CONTIGUOUS_STATES, US_STATES


def profile_view(request):
    return render(request, 'profile/profile.html', {})


class EditProfileView(View):
    # context_object_name = 'profile'
    template_name = 'profile/edit_profile.html'

    def get(self, *args, **kwargs):
        profile = get_object_or_404(Profile, user=self.request.user)
        # default_shipping_address = profile.default_shipping_address
        # default_billing_address = profile.default_billing_address
        # name_form = EditNameForm()
        # phone_form = EditPhoneForm()
        form = EditProfileForm()
        context = {
            'profile': profile,
            'form': form,
            'states_choices': CONTIGUOUS_STATES,
        }
        return render(self.request, self.template_name, context)

    def post(self, *args, **kwargs):
        profile = get_object_or_404(Profile, user=self.request.user)
        user = self.request.user
        default_shipping_address = profile.default_shipping_address
        default_billing_address = profile.default_billing_address
        # name_form = EditNameForm()
        # phone_form = EditPhoneForm()
        form = EditProfileForm(self.request.POST or None)
        # context = {
        #     'profile': profile,
        #     'form': form,
        #     # 'name_form': name_form,
        #     # 'phone_form': phone_form,
        # }
        # print(self.request.POST)
        if 'save_name' in self.request.POST:
            if form.is_valid():
                first_name = form.cleaned_data.get('first_name')
                last_name = form.cleaned_data.get('last_name')
                user.first_name = first_name
                user.last_name = last_name
                user.save()
                return redirect('core:edit_profile')
            else:
                messages.warning(self.request, form.errors.as_data())
                return redirect('core:edit_profile')

        elif 'save_phone' in self.request.POST:
            if form.is_valid():
                phone_number = form.cleaned_data.get('phone_num')
                profile.phone_num = phone_number
                profile.save()
                return redirect('core:edit_profile')
            else:
                messages.warning(self.request, form.errors.as_data())
                return redirect('core:edit_profile')

        elif 'save_shipping' in self.request.POST:
            if form.is_valid():
                default_shipping_address.first_name = form.cleaned_data.get('shipping_first_name')
                default_shipping_address.last_name = form.cleaned_data.get('shipping_last_name')
                default_shipping_address.street_address = form.cleaned_data.get('shipping_street_address')
                default_shipping_address.apartment_address = form.cleaned_data.get('shipping_apartment_address')
                default_shipping_address.city = form.cleaned_data.get('shipping_city')
                default_shipping_address.state = form.cleaned_data.get('shipping_state')
                default_shipping_address.zipcode = form.cleaned_data.get('shipping_zipcode')
                default_shipping_address.address_type = 'S'
                default_shipping_address.save()
                profile.save()
                return redirect('core:edit_profile')
            else:
                messages.warning(self.request, form.errors.as_data())
                return redirect('core:edit_profile')

        elif 'save_billing' in self.request.POST:
            if form.is_valid():
                default_billing_address.first_name = form.cleaned_data.get('billing_first_name')
                default_billing_address.last_name = form.cleaned_data.get('billing_last_name')
                default_billing_address.street_address = form.cleaned_data.get('billing_street_address')
                default_billing_address.apartment_address = form.cleaned_data.get('billing_apartment_address')
                default_billing_address.city = form.cleaned_data.get('billing_city')
                default_billing_address.state = form.cleaned_data.get('billing_state')
                default_billing_address.zipcode = form.cleaned_data.get('billing_zipcode')
                default_billing_address.address_type = 'B'
                default_billing_address.save()
                profile.save()
                return redirect('core:edit_profile')
            else:
                messages.warning(self.request, form.errors.as_data())
                return redirect('core:edit_profile')

        messages.warning(self.request, "Invalid Shipping Information")
        return redirect('core:edit_profile')

# class ManageAddressesView(View):
#
#     def get(self, *args, **kwargs):
#         cart = get_object_or_404(Cart, user=self.request.user)
#         profile = Profile.objects.get(user=self.request.user)
#         form = CheckoutForm()
#         context = {
#             'cart': cart,
#             'profile': profile,
#             'form': form,
#             'couponform': CouponForm()
#         }
#         return render(self.request, self.template_name, context)
