from django.conf import settings
from django.contrib.auth import login, authenticate, logout
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail, EmailMessage
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib import messages
from django.views.generic import ListView

from .models import Institution, Category, CustomUser, Donation
from core.forms import UserRegistrationForm, Donator, ContactForm, DonationForm
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
            messages.success(request, "Wysłaliśmy na Twój adres email link aktywacyjny do konta.")
            return HttpResponseRedirect(request.META.get("HTTP_REFERER"))
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
        return HttpResponse('Link aktywacyjny jest nieważny')


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

    form = DonationForm()
    categories = Category.objects.all()
    # cat_ids = request.GET.getlist('category')
    # institution_to_get = Institution.objects.filter(categories__id__in=cat_ids)
    institution_to_get = Institution.objects.all()


    return render(request, 'core/form.html', {'form':form, 'categories': categories,
                                              'institution_to_get': institution_to_get})

def create_donation(request):

    if request.is_ajax() and request.method =='POST':

        quantity = request.POST.get('bags')
        address = request.POST.get('address')
        zip_code = request.POST.get('postcode')
        phone_number = request.POST.get('phone')
        pick_up_date = request.POST.get('data')
        pick_up_time = request.POST.get('time')
        pick_up_comment = request.POST.get('more_info')

        user = request.user

        donation = Donation.objects.create(quantity=quantity, address=address, phone_number=phone_number,
                                           zip_code=zip_code, pick_up_date=pick_up_date, pick_up_time=pick_up_time,
                                           pick_up_comment=pick_up_comment, user=user)

        categories_ids = request.POST.getlist('categories')
        categories = Category.objects.filter(id__in=categories_ids)
        donation.categories.set(categories)

        institution_id = request.POST.getlist('organization')
        institution = Category.objects.filter(id__in=institution_id)
        donation.categories.set(institution)

    return redirect('core:form_confirmation')



def form_confirmation(request):

    return render(request, 'core/form-confirmation.html', {})


def user_account(request):
    user = request.user
    form = Donator(instance=user)
    user_donations = Donation.objects.filter(user=user)

    if request.method == 'POST':
        form = Donator(request.POST, instance=user)
        if form.is_valid():
            form.save()

    return render(request, 'core/account.html', {'form': form, 'user_donations': user_donations})

#
# def show_user_donation(request):
#     user= request.user
#     user_donations= Donation.objects.filter(user=user)
#
#     return Donation.objects.filter(user__user= self.request.user)


def contact_form(request):

    form  = ContactForm()
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            superusers_emails = CustomUser.objects.filter(is_superuser=True).values_list('email', flat=True)
            subject = f"Formularz kontaktowy od użytkownika: {cd['name']} {cd['surname']}"
            print(subject)
            print(cd)
            send_mail(subject, cd['message'], settings.EMAIL_HOST_USER,
                      superusers_emails)
            return redirect('core:home')
    return render(request, 'core/base.html', {'form':form})