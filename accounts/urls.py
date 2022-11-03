from rest_framework.routers import DefaultRouter
from django.urls import include, path
from accounts.views import EmailUserView, GenerateApiKeyView, SignupView, ResetApiKeyView, ForgetPasswordView, ChangePassword, LogoutView, LogoutAllView, TestView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView


urlpatterns = [
    path('test/', TestView.as_view(), name='tester'),
    path('signup/', SignupView.as_view(), name='signup'),
    path('login/', TokenObtainPairView.as_view(), name='login'),
    path('logoutall/', LogoutAllView.as_view(), name='logout_all'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('token/refresh/', TokenRefreshView.as_view(), name='refresh_token'),
    path('password/reset/', ForgetPasswordView.as_view(), name='reset_password'),
    path('password/change/', ChangePassword.as_view(), name='new_password'),
    path('apikey/reset/', ResetApiKeyView.as_view(), name='reset_key'),
    path('apikey/generate/', GenerateApiKeyView.as_view(), name='new_apikey'),
    path(
        'confirm/(<uidb64>[0-9A-Za-z_\-]+)/(<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/', EmailUserView.as_view(), name='activate'),
]
