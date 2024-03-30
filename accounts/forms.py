from django_recaptcha.fields import ReCaptchaField
from django_recaptcha.widgets import ReCaptchaV2Checkbox
from django.contrib.auth.forms import AuthenticationForm

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from accounts.models import Employee


class CustomLoginForm(AuthenticationForm):
    captcha = ReCaptchaField(
        widget=ReCaptchaV2Checkbox,
    )


class RegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    captcha = ReCaptchaField(
        widget=ReCaptchaV2Checkbox,
    )

    class Meta:
        model = Employee
        fields = ('username', 'email', 'password1', 'password2')
