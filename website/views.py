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


class ContactsView(TemplateView):
    # View for home page of site.
    template_name = 'website/contacts.html'
