from django.contrib.auth import authenticate, login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.messages.views import SuccessMessageMixin
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import TemplateView, CreateView
from django.db.models import Sum, Count
from django.db.models.functions import Length
from django.db.models import F


from random import sample

from django.views.generic.edit import FormMixin

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


class AddDonationView(LoginRequiredMixin, View, FormMixin):
    login_url = reverse_lazy('donations:login')
    form_class = forms.AddDonationForm

    def get(self, request):
        category_ids = self.request.GET.getlist('category_ids')
        categories = models.Category.objects.all().order_by(Length('name')).reverse()
        institutions = models.Institution.objects.all()
        if len(category_ids) != 0 and category_ids is not None:
            institutions = models.Institution.objects.filter(categories__in=category_ids).distinct()
            print({'categories': categories, 'institutions': institutions})
            return render(request, 'api_intitutions.html', {'categories': categories, 'institutions': institutions, 'form': self.form_class})

        return render(request, 'donations/form.html', {'categories': categories, 'institutions': institutions, 'form': self.form_class})

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            donation = form.save(commit=False)
            donation.user = request.user
            donation.categories = request.categories
            donation.institution = request.institution
            donation.save()
            return redirect(reverse_lazy('donations:landing_page'))
        else:
            return render(request, 'donations/form.html', {'form': form})

    # def post(self, request):
    #     form = forms.AddDonationForm(request.POST or None)
    #     if form.is_valid():
    #         donation = form.save(commit=False)
    #         donation.user = request.user
    #         print(donation)
    #         donation.save()
    #         return redirect(reverse_lazy('donations:landing_page'))
    #     else:
    #         form = forms.AddDonationForm
    #         return render(request, 'donations/form.html', {'form': form})


class DonationsLoginView(LoginView):

    template_name = 'donations/login.html'
    authentication_form = forms.UserLoginForm

    def form_valid(self, form):
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')

        user = authenticate(username=username, password=password)

        if user is not None:
            if user.is_active:
                login(self.request, form.get_user())
                return redirect(reverse_lazy('donations:landing_page'))
        else:
            return redirect(reverse_lazy('donations:register'))


class DonationsLogoutView(LogoutView):
    next_page = reverse_lazy('donations:landing_page')


class RegisterView(SuccessMessageMixin, CreateView):
    template_name = 'donations/register.html'
    success_url = reverse_lazy('donations:login')
    form_class = forms.UserRegisterForm
    success_message = 'Twoje konto zostało stworzone'


