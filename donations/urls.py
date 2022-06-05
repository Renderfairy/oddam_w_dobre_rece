from django.urls import path

from . import views

app_name = 'donations'

urlpatterns = [
    path('', views.LandingPageView.as_view(), name='landing_page'),
    path('donation', views.AddDonationView.as_view(), name='add_donation'),
    path('donation-is-taken/<int:donation_id>', views.DonationIsTakenView.as_view(), name='donation_taken'),
    path('donation/success', views.SuccessAddDonationView.as_view(), name='success_add_donation'),
    path('login', views.DonationsLoginView.as_view(), name='login'),
    path('logout', views.DonationsLogoutView.as_view(), name='logout'),
    path('register', views.RegisterView.as_view(), name='register'),
    path('profile', views.UserProfileView.as_view(), name='user_profile'),
    # path('edit', views.edit_user_profile_view, name='user_change'),
]
