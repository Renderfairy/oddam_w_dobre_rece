from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import TemplateView, CreateView
from django.db.models import Sum


from random import sample

from . import models, forms


class LandingPageView(TemplateView):
    template_name = "donations/index.html"

    def get_context_data(self, **kwargs):
        context = super(LandingPageView, self).get_context_data(**kwargs)
        foundations = list(models.Institution.objects.filter(type=0).order_by('name'))
        listed_foundations = sample(foundations, 3)
        non_gov_org = list(models.Institution.objects.filter(type=1).order_by('name'))
        listed_non_gov_org = sample(non_gov_org, 3)
        fund_raisers = list(models.Institution.objects.filter(type=2).order_by('name'))
        listed_fund_raisers = sample(fund_raisers, 3)
        try:
            context['donations_quantity'] = models.Donation.objects.all().aggregate(Sum('quantity'))['quantity__sum']
            context['institutions'] = models.Institution.objects.all().count()
            context['three_foundations'] = listed_foundations
            context['three_non_gov_org'] = listed_non_gov_org
            context['three_fund_raisers'] = listed_fund_raisers
            context['css_class'] = 'header--main-page'
        except models.Donation.DoesNotExist or models.Institution.DoesNotExist:
            context['donations_quantity'] = None
            context['institutions'] = None
        return context


class AddDonationView(TemplateView):
    template_name = 'donations/form.html'

    def get_context_data(self, **kwargs):
        context = super(AddDonationView, self).get_context_data(**kwargs)
        context['css_class'] = 'header--form-page'

        return context


class LoginView(TemplateView):

    template_name = 'donations/login.html'


class RegisterView(SuccessMessageMixin, CreateView):
    template_name = 'donations/register.html'
    success_url = reverse_lazy('donations:login')
    form_class = forms.UserRegisterForm
    success_message = 'Twoje konto zostało stworzone'
