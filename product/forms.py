from django import forms
from django.contrib.auth import get_user_model, authenticate
from .models import Product


# from django.conf import settings


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = "__all__"
        # or defined the fields by specifically
        # fields = ['name', 'category', 'description', 'price', 'inventory']


User = get_user_model()

# Register and Login Form are took care of by django-allauth

# class UserRegisterForm(forms.ModelForm):
#     password = forms.CharField(widget=forms.PasswordInput)
#     confirm_password = forms.CharField(widget=forms.PasswordInput)
#
#     class Meta:
#         model = User
#         fields = [
#             'username', 'email', 'password', 'confirm_password'
#         ]
#
#     def clean(self, *args, **kwargs):
#         password = self.cleaned_data.get('password')
#         confirm_password = self.cleaned_data.get('confirm_password')
#         if password != confirm_password:
#             raise forms.ValidationError('The passwords do not match')
#         return super(UserRegisterForm, self).clean(*args, **kwargs)
#
#
# class UserLoginForm(forms.Form):
#     username = forms.CharField()
#     password = forms.CharField(widget=forms.PasswordInput)
#
#     def clean(self, *args, **kwargs):
#         username = self.cleaned_data.get('username')
#         password = self.cleaned_data.get('password')
#
#         if username and password:
#             user = authenticate(username=username, password=password)
#             if not user:
#                 raise forms.ValidationError('This user does not exist')
#             if not user.check_password(password):
#                 raise forms.ValidationError('The username or password was incorrect')
#             if not user.is_active:
#                 raise forms.ValidationError('This user is not active')
#         return super(UserLoginForm, self).clean(*args, **kwargs)
