from django.urls import path

from .views import profile_view, EditProfileView

app_name = 'core'

urlpatterns = [
    path('profile/', profile_view, name='profile'),
    path('edit_profile/', EditProfileView.as_view(), name='edit_profile'),
    path('addresses/', profile_view, name='manage_address'),
]
