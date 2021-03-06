from django.urls import path
from core.views import register, user_logout, add_donation, user_account, activate, contact_form, create_donation, \
    form_confirmation, donation_is_taken, HomeView
from django.contrib.auth.views import LoginView

app_name = 'core'

urlpatterns = [


    path('register/', register, name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', user_logout, name='logout'),


    path('activate/<uidb64>/<token>/', activate, name='activate'),

    path('contact/', contact_form, name='contact_form'),
    path('', HomeView.as_view(), name='home'),
    path('donation/', add_donation, name='donation'),
    path('create_donation/', create_donation, name='create_donation'),
    path('form_confirmation/', form_confirmation, name="form_confirmation"),
    path('profile/', user_account, name='profile'),
    path('taken-item/<id>/', donation_is_taken, name="taken"),
]