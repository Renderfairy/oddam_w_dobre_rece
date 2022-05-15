from django.urls import path

from . import views

app_name = 'donations'

urlpatterns = [
    path('', views.LandingPageView.as_view(), name='landing_page'),
    path('donation', views.AddDonationView.as_view(), name='add_donation'),
    path('login', views.LoginView.as_view(), name='login'),
    path('register', views.RegisterView.as_view(), name='register'),
]
