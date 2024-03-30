from django.contrib.auth.views import (LoginView,
                                       PasswordResetConfirmView as BasePasswordResetConfirmView,
                                       PasswordResetView as BasePasswordResetView)
from django.shortcuts import get_object_or_404
from accounts.forms import CustomLoginForm
from django.urls import reverse_lazy
from django.utils.http import url_has_allowed_host_and_scheme
from accounts.forms import RegistrationForm
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import (
    CreateView, DetailView, TemplateView,
)

from accounts.models import Employee


class PaymentPageView(LoginRequiredMixin,
                      TemplateView):
    template_name = 'payment.html'


class CustomLoginView(LoginView):
    template_name = 'login.html'
    form_class = CustomLoginForm

    def get_success_url(self):
        next_url = self.request.GET.get('next')
        if next_url and url_has_allowed_host_and_scheme(
                url=next_url,
                allowed_hosts={self.request.get_host()},
                require_https=self.request.is_secure(),
        ):
            return next_url

        return reverse_lazy('home')


class UserProfileView(LoginRequiredMixin, DetailView):
    model = Employee
    template_name = 'user_profile.html'
    context_object_name = 'user_profile'

    def get_object(self, queryset=None):
        return get_object_or_404(Employee, username=self.kwargs['username'])


class RegistrationView(CreateView):
    model = Employee
    form_class = RegistrationForm
    template_name = 'registration.html'
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, 'Your account has been created')
        return response


class PasswordResetView(BasePasswordResetView):
    email_template_name = 'password_reset_email.txt'
    html_email_template_name = 'password_reset_email.html'
    template_name = 'password_reset_form.html'
    success_url = reverse_lazy('accounts:password_reset_done')


class PasswordResetConfirmView(BasePasswordResetConfirmView):
    success_url = reverse_lazy('accounts:password_reset_complete')
    template_name = 'password_reset_confirm.html'
