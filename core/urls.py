from django.urls import path

from .views import profile_view

app_name = 'core'

urlpatterns = [
    path('profile/', profile_view, name='profile'),
    path('addresses/', profile_view, name='manage_address'),
]
