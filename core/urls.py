from django.contrib.auth.views import LoginView
from django.urls import path
from core.views import home, register, user_login, user_logout

app_name = 'core'


urlpatterns = [
    path('', home, name='home'),
    # path('/', FundsList.as_view(), name= 'funds'),
    path('register/', register, name='register'),
    path('login/', user_login, name='login'),
    path('logout/', user_logout, name='logout'),
]