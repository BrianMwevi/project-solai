from django.urls import path
from accounts.views import EmailUserView, GenerateApiKeyView, SignupView, LoginView, ResetApiKeyView, ForgotPasswordView, ChangePasswordView, LogoutView, LogoutAllView
from rest_framework_simplejwt.views import TokenRefreshView



urlpatterns = [
    path('signup/', SignupView.as_view(), name='signup'),
    path('login/', LoginView.as_view(), name='login'),
    path('logoutall/', LogoutAllView.as_view(), name='logout_all'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('token/refresh/', TokenRefreshView.as_view(), name='refresh_token'),
    path('password/reset/', ForgotPasswordView.as_view(), name='reset_password'),
    path('password/change/', ChangePasswordView.as_view(), name='change_password'),
    path('apikey/reset/', ResetApiKeyView.as_view(), name='reset_key'),
    path('apikey/generate/', GenerateApiKeyView.as_view(), name='new_apikey'),
    path(
        'confirm/(<uidb64>[0-9A-Za-z_\-]+)/(<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/', EmailUserView.as_view(), name='activate'),
]
