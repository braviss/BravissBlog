from django.urls import path
from django.contrib.auth import views as auth_views
from accounts.views import (CustomLoginView,
                            PasswordResetView,
                            PasswordResetConfirmView,
                            PaymentPageView)
from accounts import views


urlpatterns = [
    path('login/',
         CustomLoginView.as_view(), name='login'),
    path('logout/',
         auth_views.LogoutView.as_view(), name='logout'),
    path('profile/<str:username>',
         views.UserProfileView.as_view(), name='user_profile'),
    path('register/',
         views.RegistrationView.as_view(), name='register'),
    path('password_reset/',
         PasswordResetView.as_view(),
         name='password_reset'),
    path(
        'password_reset/done/',
        auth_views.PasswordResetDoneView.as_view(template_name='password_reset_done.html'),
        name='password_reset_done',
    ),
    path(
        'reset/<uidb64>/<token>/',
        PasswordResetConfirmView.as_view(template_name='password_reset_confirm.html'),
        name='password_reset_confirm',
    ),
    path(
        'reset/done/',
        auth_views.PasswordResetCompleteView.as_view(template_name='password_reset_complete.html'),
        name='password_reset_complete',
    ),
    path('payment',
         PaymentPageView.as_view(), name='payment'),
    # path('edit/<str:username>',
    #      views.UserProfileView.as_view(), name='user_profile'),
]
