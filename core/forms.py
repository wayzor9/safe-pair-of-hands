from django import forms

from core.models import CustomUser, Donation


class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(label='Hasło',
                               widget=forms.PasswordInput)
    password2 = forms.CharField(label='Powtórz Hasło',
                                widget=forms.PasswordInput)

    class Meta:
        model = CustomUser
        fields = ('first_name', 'last_name', 'email')

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
                'All fields required')


class DonationForm(forms.ModelForm):
    class Meta:
        model = Donation
        fields = ("quantity", "categories", "institution", "address", "phone_number", "zip_code",
                  "pick_up_date", "pick_up_time", "pick_up_comment", "is_taken")
