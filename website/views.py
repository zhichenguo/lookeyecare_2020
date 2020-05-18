from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.views.generic import TemplateView


class HomeView(TemplateView):
    # View for home page of site.
    template_name = 'home.html'


class CollectionsView(TemplateView):
    # View for home page of site.
    template_name = 'website/collections.html'


class LensTechView(TemplateView):
    # View for home page of site.
    template_name = 'website/lens_tech.html'


class OurServicesView(TemplateView):
    # View for home page of site.
    template_name = 'website/our_services.html'


class InsurancePromotionView(TemplateView):
    # View for home page of site.
    template_name = 'website/insurance_promotion.html'


class MeetUsView(TemplateView):
    # View for home page of site.
    template_name = 'website/meet_us.html'


class BookExamView(TemplateView):
    # View for home page of site.
    template_name = 'website/book_exam.html'


class ContactsView(TemplateView):
    # View for home page of site.
    template_name = 'website/contacts.html'


class TomFordView(TemplateView):
    # View for tom_ford page of site.
    template_name = 'website/tom_ford.html'


class GucciView(TemplateView):
    # View for gucci page of site.
    template_name = 'website/gucci.html'


class CartierView(TemplateView):
    # View for cartier page of site.
    template_name = 'website/cartier.html'


class LindbergView(TemplateView):
    # View for lindberg page of site.
    template_name = 'website/lindberg.html'


class RayBanView(TemplateView):
    # View for ray_ban page of site.
    template_name = 'website/ray_ban.html'


class OakleyView(TemplateView):
    # View for oakley page of site.
    template_name = 'website/oakley.html'


class BurberryView(TemplateView):
    # View for burberry page of site.
    template_name = 'website/burberry.html'


class BoucheronView(TemplateView):
    # View for boucheron page of site.
    template_name = 'website/boucheron.html'


class SaintLaurentView(TemplateView):
    # View for saint_laurent page of site.
    template_name = 'website/saint_laurent.html'


class FreakshowView(TemplateView):
    # View for freakshow page of site.
    template_name = 'website/freakshow.html'


class VinylFactoryView(TemplateView):
    # View for vinyl_factory page of site.
    template_name = 'website/vinyl_factory.html'


class BottegaVenetaView(TemplateView):
    # View for bottega_veneta page of site.
    template_name = 'website/bottega_veneta.html'


class HenryJullienView(TemplateView):
    # View for henry_jullien page of site.
    template_name = 'website/henry_jullien.html'


class McqView(TemplateView):
    # View for mcq page of site.
    template_name = 'website/mcq.html'


class SwarovskiView(TemplateView):
    # View for swarovski page of site.
    template_name = 'website/swarovski.html'


class StellaKidsView(TemplateView):
    # View for stella_kids page of site.
    template_name = 'website/stella_kids.html'


class ZegnaView(TemplateView):
    # View for zegna page of site.
    template_name = 'website/zegna.html'


class PlmView(TemplateView):
    # View for plm page of site.
    template_name = 'website/plm.html'


class LookEyeWareView(TemplateView):
    # View for look_eyeware page of site.
    template_name = 'website/look_eyeware.html'
