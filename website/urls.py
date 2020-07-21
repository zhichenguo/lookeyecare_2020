from django.urls import path

from .views import (
    HomeView, CollectionsView, LensTechView, OurServicesView, BookExamView, InsurancePromotionView, ContactsView,
    MeetUsView,
    TomFordView, GucciView, CartierView, LindbergView, RayBanView, OakleyView, BurberryView, BoucheronView,
    SaintLaurentView, FreakshowView, VinylFactoryView, BottegaVenetaView, HenryJullienView, McqView, SwarovskiView,
    StellaKidsView, ZegnaView, PlmView, LookEyeWareView
)

app_name = 'website'

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('collections/', CollectionsView.as_view(), name='collections'),
    path('contacts/', ContactsView.as_view(), name='contacts'),
    path('lens_tech/', LensTechView.as_view(), name='lens_tech'),
    path('our_services/', OurServicesView.as_view(), name='our_services'),
    path('book_exam/', BookExamView.as_view(), name='book_exam'),
    path('insurance_promotion/', InsurancePromotionView.as_view(), name='insurance_promotion'),
    path('meet_us/', MeetUsView.as_view(), name='meet_us'),

    path('tom_ford/', TomFordView.as_view(), name='tom_ford'),
    path('gucci/', GucciView.as_view(), name='gucci'),
    path('cartier/', CartierView.as_view(), name='cartier'),
    path('lindberg/', LindbergView.as_view(), name='lindberg'),
    path('ray_ban/', RayBanView.as_view(), name='ray_ban'),
    path('oakley/', OakleyView.as_view(), name='oakley'),
    path('burberry/', BurberryView.as_view(), name='burberry'),
    path('boucheron/', BoucheronView.as_view(), name='boucheron'),
    path('saint_laurent/', SaintLaurentView.as_view(), name='saint_laurent'),
    path('freakshow/', FreakshowView.as_view(), name='freakshow'),
    path('vinyl_factory/', VinylFactoryView.as_view(), name='vinyl_factory'),
    path('bottega_veneta/', BottegaVenetaView.as_view(), name='bottega_veneta'),
    path('henry_jullien/', HenryJullienView.as_view(), name='henry_jullien'),
    path('mcq/', McqView.as_view(), name='mcq'),
    path('swarovski/', SwarovskiView.as_view(), name='swarovski'),
    path('stella_kids/', StellaKidsView.as_view(), name='stella_kids'),
    path('zegna/', ZegnaView.as_view(), name='zegna'),
    path('plm/', PlmView.as_view(), name='plm'),
    path('look_eyeware/', LookEyeWareView.as_view(), name='look_eyeware'),
]
