from django import views
from accounts.permissions import IsAdmin, IsDeveloper, IsInvestor, IsTrader
from accounts.serializers import UserSerializer
from rest_framework import viewsets
from django.contrib.auth import get_user_model
from rest_framework import generics, views, status
from django.utils.encoding import force_text
from django.utils.http import urlsafe_base64_decode
from accounts.tokens import account_activation_token
from rest_framework.response import Response
from django.contrib.auth import login, authenticate
from accounts.api_keys import NewKey

User = get_user_model()


class SignupView(generics.CreateAPIView):
    """
    Handles user account creation
    """
    serializer_class = UserSerializer
    permission_classes = ()
    authentication_classes = ()


class LoginView(views.APIView):
    serializer_class = UserSerializer
    permission_classes = ()
    authentication_classes = ()

    def post(self, request, *args, **kwargs):
        email = request.data.get('email')
        password = request.data.get('password')
        user = User.get_user_by_email(email)
        if user is not None and user.is_active:
            user = authenticate(email, password)
            if user.is_authenticatated:
                login(request, user)
                key = NewKey.generate(user.id)
                return Response(data={"api_key": key}, status=status.HTTP_200_OK)
        elif user is not None and user.is_active:
            return Response(data={"email": "Please confirm your email address"})
        print(user)
        return Response(data={"credentials": "Invalid credentials"}, status=status.HTTP_400_BAD_REQUEST)


class ActivateEmailView(views.APIView):
    authentication_classes = ()
    permission_classes = ()

    def get(self, request, uidb64, token):
        try:
            uid = force_text(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except(TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None
        if user is not None and account_activation_token.check_token(user, token):
            key = NewKey.generate(user.id)
            user.is_active = True
            user.save()
            login(request, user)
            return Response(data={"api_key": key}, status=status.HTTP_200_OK)
        else:
            return Response(data={'error': "Invalid activation link"}, status=status.HTTP_400_BAD_REQUEST)
