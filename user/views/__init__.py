from .profile import ProfileView, MobileManagerView, EmailManagerView
from .signup import MobileInitialStepView, MobileVerificationView, MobileSignupView, EmailInitialStepView, \
    EmailVerificationView, EmailSignupView
from .password_reset import BeginPasswordResetView, SendPasswordResetView, ConfirmPasswordResetCodeView, \
    PerformPasswordResetView
from .login import LoginView
