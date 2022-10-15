from django.contrib.auth import views as auth_views
from django.urls import path

from user.views import (
    MobileInitialStepView, MobileVerificationView, MobileSignupView, EmailInitialStepView, EmailVerificationView,
    EmailSignupView, ProfileView, BeginPasswordResetView, SendPasswordResetView, ConfirmPasswordResetCodeView,
    PerformPasswordResetView, LoginView, MobileManagerView, EmailManagerView
)

urlpatterns = [
    path('profile/', ProfileView.as_view(), name='profile'),
    path('profile/contact/mobile/', MobileManagerView.as_view(), name='profile-contact-mobile'),
    path('profile/contact/email/', EmailManagerView.as_view(), name='profile-contact-email'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),

    path('signup/mobile/step/1/', MobileInitialStepView.as_view(), name='signup-mobile-1'),
    path('signup/mobile/step/2/', MobileVerificationView.as_view(), name='signup-mobile-2'),
    path('signup/mobile/step/3/', MobileSignupView.as_view(), name='signup-mobile-3'),

    path('signup/email/step/1/', EmailInitialStepView.as_view(), name='signup-email-1'),
    path('signup/email/step/2/', EmailVerificationView.as_view(), name='signup-email-2'),
    path('signup/email/step/3/', EmailSignupView.as_view(), name='signup-email-3'),

    path('password_reset/begin/', BeginPasswordResetView.as_view(), name='password-reset-begin'),
    path('password_reset/send/', SendPasswordResetView.as_view(), name='password-reset-send'),
    path('password_reset/confirm-code/', ConfirmPasswordResetCodeView.as_view(), name='password-reset-confirm-code'),
    path('password_reset/perform/', PerformPasswordResetView.as_view(), name='password-reset-perform'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
]
