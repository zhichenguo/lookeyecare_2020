from django.urls import path

from .views import (
    HomeView,
    CollectionsView,
    LensTechView,
    OurServicesView,
    InsurancePromotionView,
    ContactsView,
    MeetUsView
)

app_name = 'website'

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('collections/', CollectionsView.as_view(), name='collections'),
    path('contacts/', ContactsView.as_view(), name='contacts'),
    path('lens_tech/', LensTechView.as_view(), name='lens_tech'),
    path('our_services/', OurServicesView.as_view(), name='our_services'),
    path('insurance_promotion/', InsurancePromotionView.as_view(), name='insurance_promotion'),
    path('meet_us/', MeetUsView.as_view(), name='meet_us'),
]
