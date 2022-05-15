from django.shortcuts import render
from django.views import View
from django.views.generic import TemplateView


class LandingPageView(TemplateView):
    template_name = "donations/index.html"


class AddDonationView(View):

    def get(self, request):
        return render(request, "donations/form.html")


class LoginView(View):

    def get(self, request):
        return render(request, "donations/login.html")


class RegisterView(View):

    def get(self, request):
        return render(request, "donations/register.html")
