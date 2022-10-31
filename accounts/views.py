from django import views
from accounts.permissions import IsAdmin, IsDeveloper, IsInvestor, IsTrader
from accounts.serializers import UserSerializer
from rest_framework import viewsets
from django.contrib.auth import get_user_model
from rest_framework import generics, views
from django.utils.encoding import force_text
from django.utils.http import urlsafe_base64_decode
from accounts.tokens import account_activation_token
from rest_framework.response import Response
from django.contrib.auth import login

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
        serializer = UserSerializer(
            data=request.data, contest={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        # GENERATE API KEY


class ActivateView(views.APIView):
    authentication_classes = ()
    permission_classes = ()

    def get(self, request, uidb64, token):
        try:
            uid = force_text(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except(TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None
        if user is not None and account_activation_token.check_token(user, token):
            user.is_active = True
            user.save()
            login(request, user)
            return Response({"user is active: ": user.is_active})
        else:
            return Response({'detail': "Error"})
