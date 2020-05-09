from django.shortcuts import render

# Create your views here.
from django.views.generic import View


def profile_view(request):
    return render(request, 'profile/profile.html', {})

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
