from django.urls import path, include
from core.views import home, register, user_logout, add_donation
from django.contrib.auth.views import PasswordResetView, PasswordResetCompleteView, PasswordResetDoneView, \
    PasswordResetConfirmView, LoginView

app_name = 'core'

urlpatterns = [
    path('', home, name='home'),

    path('register/', register, name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', user_logout, name='logout'),
    path('password_reset/', PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', PasswordResetCompleteView.as_view(), name='password_reset_complete'),


    # path('', include('django.contrib.auth.urls')),


    path('add_donation/', add_donation, name='donation')
]