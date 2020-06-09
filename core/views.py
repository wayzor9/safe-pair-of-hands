from django.conf import settings
from django.contrib.auth import login, authenticate, logout
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail, EmailMessage
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib import messages

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
        else:
            messages.error(request, 'Coś poszło nie tak. Spróbuj jeszcze raz.')
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


def user_logout(request):

    logout(request)
    return redirect('core:home')


def home(request):
    return render(request, 'core/index.html', {} )


def add_donation(request):

    form = DonationForm()
    categories = Category.objects.all()
    institution_to_get = Institution.objects.all()

    return render(request, 'core/form.html', {'form': form, 'categories': categories,
                                              'institution_to_get': institution_to_get})


def create_donation(request):

    if request.is_ajax() and request.method == 'POST':

        form = DonationForm(request.POST)
        categories_ids = request.POST.getlist('categories')
        categories = Category.objects.filter(id__in=categories_ids)

        if form.is_valid():
            donation = form.save(commit=False)
            donation.user = request.user
            donation.save()
            donation.categories.set(categories)
            return JsonResponse({'success': True})
        else:
            return JsonResponse({'error': form.errors})


def form_confirmation(request):
    return render(request, 'core/form-confirmation.html', {})


def user_account(request):
    user = request.user
    user_detail_form = Donator(instance=user)
    user_donations = Donation.objects.filter(user=user)

    taken = user_donations.filter(is_taken=True).order_by('pick_up_date')
    not_taken = user_donations.filter(is_taken=False).order_by('pick_up_date')

    if request.method == 'POST':
        user_detail_form = Donator(request.POST, instance=user)
        if user_detail_form.is_valid():
            user_detail_form.save()
            messages.success(request, "Zmiany zapisane!")

    return render(request, 'core/account.html', {'form': user_detail_form, 'user_donations': user_donations,
                                                 "taken": taken, "not_taken": not_taken})
#     return Donation.objects.filter(user__user= self.request.user)


def donation_is_taken(request, id):

    donation = Donation.objects.get(id=id)
    donation.is_taken = True
    donation.save()
    return redirect('core:profile')


def contact_form(request):

    form = ContactForm()
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            superusers_emails = CustomUser.objects.filter(is_superuser=True).values_list('email', flat=True)
            subject = f"Formularz kontaktowy od użytkownika: {cd['name']} {cd['surname']}"
            send_mail(subject, cd['message'], settings.EMAIL_HOST_USER,
                      superusers_emails)
            return render(request, 'core/form-confirmation.html')
        else:
            messages.warning(request, 'Nie udało się wysłać formularza. Wszystkie pola muszą być wypełnione')
    return render(request, 'core/base.html', {'form':form})