from rest_framework.routers import DefaultRouter
from django.urls import include, path
from accounts.views import ActivateEmailView, LoginView, SignupView


urlpatterns = [
    path('register/', SignupView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path(
        'activate/(<uidb64>[0-9A-Za-z_\-]+)/(<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/', ActivateEmailView.as_view(), name='activate'),
]
