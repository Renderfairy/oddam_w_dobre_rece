from django.shortcuts import render
from django.views import View
from django.views.generic import TemplateView
from django.db.models import Sum

from . import models


class LandingPageView(TemplateView):
    template_name = "donations/index.html"

    def get_context_data(self, **kwargs):
        context = super(LandingPageView, self).get_context_data(**kwargs)
        try:
            context['donations_quantity'] = models.Donation.objects.all().aggregate(Sum('quantity'))['quantity__sum']
            context['institutions'] = models.Institution.objects.all().count()
        except models.Donation.DoesNotExist or models.Institution.DoesNotExist:
            context['donations_quantity'] = None
            context['institutions'] = None
        return context


class AddDonationView(View):

    def get(self, request):
        return render(request, "donations/form.html")


class LoginView(View):

    def get(self, request):
        return render(request, "donations/login.html")


class RegisterView(View):

    def get(self, request):
        return render(request, "donations/register.html")
