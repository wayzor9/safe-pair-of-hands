from django.urls import path
from core.views import landing_page, FundsList, register, user_login

app_name = 'core'


urlpatterns = [
    path('', landing_page, name='landing'),
    path('', FundsList.as_view(), name= 'funds'),
    path('register', register, name='register'),
    path('login/', user_login, name='login'),

]