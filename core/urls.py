from django.urls import path, include
from core.views import home, register, user_logout, add_donation, user_account, activate
from django.contrib.auth.views import LoginView, PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, \
    PasswordResetCompleteView

app_name = 'core'


urlpatterns = [

    # path('/', FundsList.as_view(), name= 'funds'),
    path('register/', register, name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', user_logout, name='logout'),

    path('', include('django.contrib.auth.urls')),

    path('activate/<uidb64>/<token>/', activate, name='activate'),

    # path('password_reset/', PasswordResetView.as_view(), name='password_reset'),
    # path('password_reset/done/', PasswordResetDoneView.as_view(), name='password_reset_done'),
    # path('reset/<uidb64>/<token>/', PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    # path('reset/done/', PasswordResetCompleteView.as_view(), name='password_reset_complete'),

    path('', home, name='home'),
    path('donation/', add_donation , name='donation'),
    path('profile/', user_account, name='profile'),

]