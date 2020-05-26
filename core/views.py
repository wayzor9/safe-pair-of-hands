from django.conf import settings
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.views import LoginView
from django.core.mail import send_mail
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views.generic import ListView
from django.contrib import messages
from .models import Institution, Category, CustomUser
from core.forms import UserRegistrationForm, Donator


def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            new_user = user_form.save(commit=False)
            new_user.set_password(
                user_form.cleaned_data['password'])
            new_user.save()
            messages.success(request, "Konto dla użytkownika " + new_user.first_name + ' zostało utworzone')
            return redirect('core:login')
    else:
        user_form = UserRegistrationForm()
    return render(request,
                  'core/register.html',
                  {'user_form': user_form})




# def user_login(request):
#     next = request.GET.get('next')
#     if request.method == 'POST':
#         form = LoginForm(request.POST)
#         if form.is_valid():
#             cd = form.cleaned_data
#             user = authenticate(request,
#                                 email=cd['email'],
#                                 password=cd['password'])
#             if user is not None:
#                 if user.is_active:
#                     login(request, user)
#                     if next:
#                         return redirect(next)
#                     return redirect ('core:home')
#
#             else:
#                 messages.info(request, "Podany login lub hasło jest niepoprawne")
#
#     else:
#         form = LoginForm()
#     return render(request, 'core/login.html', {'form': form})


def user_logout(request):
    logout(request)
    return redirect('core:home')


def home(request):
    return render(request, 'core/index.html', {} )


def add_donation(request):

    categories = Category.objects.all()
    # cat_ids = request.GET.getlist('category')
    # institution_to_get = Institution.objects.filter(categories__id__in=cat_ids)
    institution_to_get = Institution.objects.all()

    return render(request, 'core/form.html', {'categories': categories,
                                              'institution_to_get': institution_to_get})

def create_donation(request):

    if request.is_ajax() and request.method=='POST':
        pass



def user_account(request):
    app_user = request.user
    form = Donator(instance=app_user)

    if request.method == 'POST':
        form = Donator(request.POST, instance=app_user)
        if form.is_valid():
            form.save()

    return render(request, 'core/account.html', {'form': form})



def contact_form(request):
    # form  = ContactForm()
    sent= False
    if request.method == 'POST':
        # form = ContactForm(request.POST)
        # if form.is_valid():
        name = request.post['name']
        surname = request.post['surname']
        message = request.post['message']
        superusers_emails = CustomUser.objects.filter(is_superuser=True).values_list('email')
        subject = f'Formularz kontaktowy od użytkownika: {name} {surname}'
        send_mail(subject, message, settings.EMAIL_HOST_USER,
                  superusers_emails, fail_silently=False)
        sent = True
        if sent:
            redirect('core:home')
    # return render(request, 'core/base.html', {})