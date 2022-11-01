from rest_framework.routers import DefaultRouter
from django.urls import include, path
from accounts.views import ActivateEmailView, GenerateApiKeyView, DeveloperSignupView, ResetApiKeyView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView


urlpatterns = [
    path('signup/developer/', DeveloperSignupView.as_view(), name='signup_dev'),
    path('apikey/generate/', GenerateApiKeyView.as_view(), name='new_apikey'),
    path('apikey/reset/', ResetApiKeyView.as_view(), name='reset_key'),
    path('login/', TokenObtainPairView.as_view(), name='new_token'),
    path('token/refresh/', TokenRefreshView.as_view(), name='refresh_token'),
    path(
        'activate/(<uidb64>[0-9A-Za-z_\-]+)/(<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/', ActivateEmailView.as_view(), name='activate'),
]
