from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.forms import AuthenticationForm

from core.models import CustomUser, Donation


# class LoginView(AuthenticationForm):
#     email = forms.CharField()
#     password = forms.CharField(widget=forms.PasswordInput)
#
#     def clean(self, *args, **kwargs):
#         email = self.cleaned_data['email']
#         password = self.cleaned_data['password']
#
#         if email and password:
#             user = authenticate(email=email, password=password)
#             if not user:
#                 raise forms.ValidationError('Nie ma takiego użytkownika :(')
#             if not user.check_password(password):
#                 raise forms.ValidationError('Podany email lub hasło są niepoprawne')
#             if not user.is_active:
#                 raise forms.ValidationError('Użytkownik aktywny')
#         return super(AuthenticationForm, self).clean(*args, **kwargs)


class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(label='Hasło',
                               widget=forms.PasswordInput)
    password2 = forms.CharField(label='Powtórz Hasło',
                                widget=forms.PasswordInput)

    class Meta:
        model = CustomUser
        fields = ('first_name', 'last_name','email')

    def clean_password2(self, *args, **kwargs):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Hasła nie są takie same')
        elif len(cd['password']) < 8:
            raise forms.ValidationError("Hasło musi mieć przynajmniej 8 znaków.")
        elif not any(c.isdigit() for c in cd['password']):
            raise forms.ValidationError("Hasło musi zawierać przynajmniej jedną cyfrę.")
        return super(UserRegistrationForm, self).clean(*args, **kwargs)


class Donator(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ('first_name', 'last_name', 'email')


class ContactForm(forms.Form):
    name = forms.CharField(max_length=23, required=True)
    surname = forms.CharField(max_length=33, required=True)
    message = forms.CharField(widget=forms.Textarea, required=True)

    def clean(self):
        cleaned_data = super().clean()
        name = cleaned_data.get("name")
        surname = cleaned_data.get("surname")
        message = cleaned_data.get("message")
        if not name and surname and message:
                raise forms.ValidationError(
                    'Wszystkie pola są wymagane')


class DonationForm(forms.ModelForm):
    class Meta:
        model = Donation
        fields = '__all__'
        exclude = ['categories', 'institution', 'user']
