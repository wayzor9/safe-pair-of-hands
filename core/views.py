from django.conf import settings
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.views import LoginView
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail, EmailMessage
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.views.generic import ListView
from django.contrib import messages
from .models import Institution, Category, CustomUser
from core.forms import UserRegistrationForm, Donator
from .tokens import account_activation_token


def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            new_user = user_form.save(commit=False)
            new_user.set_password(
                user_form.cleaned_data['password'])
            new_user.save()
            current_site = get_current_site(request)
            mail_subject = 'Aktywuj swoje konto na "Oddam w Dobre Ręce"'
            message = render_to_string('core/acc_active_email.html', {
                'user': new_user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(new_user.pk)),
                'token': account_activation_token.make_token(new_user),
            })
            to_email = user_form.cleaned_data.get('email')
            email = EmailMessage(
                mail_subject, message, to=[to_email]
            )
            email.send()
            return HttpResponse('Please confirm your email address to complete the registration')
            # messages.success(request, "Konto dla użytkownika " + new_user.first_name + ' zostało utworzone')
            # return redirect('core:login')
    else:
        user_form = UserRegistrationForm()
    return render(request,
                  'core/register.html',
                  {'user_form': user_form})

def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = CustomUser.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, CustomUser.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        # return redirect('home')
        messages.success(request, 'Dziękujemy za potwierdzenie. Możesz się zalogować')
        return redirect('core:login')
    else:
        return HttpResponse('Activation link is invalid!')


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