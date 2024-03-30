# from django.contrib.auth.mixins import UserPassesTestMixin
# from accounts.models import Employee
# from django.shortcuts import get_object_or_404
#
#
# class UserOwnsObjectMixin(UserPassesTestMixin):
#     def test_func(self):
#         username = self.kwargs['username']  # Предполагается, что в URL передается параметр 'uuid'
#         employee = get_object_or_404(Employee, username=username)  # Получаем объект Employee по UUID или возвращаем ошибку 404
#         return self.request.user == employee.user

from django.http import HttpResponseForbidden
from django.contrib import messages
from django.shortcuts import redirect
from django.urls import reverse

class BalanceRequiredMixin:
    def dispatch(self, request, *args, **kwargs):

        if hasattr(request.user, 'balance'):

            if request.user.balance >= 10:
                return super().dispatch(request, *args, **kwargs)

        error_message = "Ooops.. Balance error. <a href='{}'>Top up balance</a>".format(
            reverse('accounts:payment'))
        messages.error(request, error_message, extra_tags='danger')


        return redirect(reverse('blog:article_list'))
