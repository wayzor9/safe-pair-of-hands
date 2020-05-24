from django.contrib.auth import login, authenticate, logout
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views.generic import ListView
from django.contrib import messages
from .models import Institution, Category
from core.forms import UserRegistrationForm, LoginForm


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

def user_login(request):
    next = request.GET.get('next')
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request,
                                email=cd['email'],
                                password=cd['password'])
            if user is not None:
                if user.is_active:
                    login(request, user)
                    if next:
                        return redirect(next)
                    return redirect ('core:home')

            else:
                messages.info(request, "Podany login lub hasło jest niepoprawne")

        # return render(request, 'core/login.html', {'form': form})

    else:
        form = LoginForm()
    return render(request, 'core/login.html', {'form': form})


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

    if request.is_ajax():
        pass



    return render(request, 'core/form.html', {'categories':categories,
                            'institution_to_get':institution_to_get})
