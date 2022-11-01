from rest_framework.permissions import IsAuthenticated
from rest_framework import generics, views, status
from rest_framework.response import Response

from django.contrib.auth import get_user_model
from django.utils.encoding import force_text
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth import login

from drf_yasg.utils import swagger_auto_schema

from accounts.permissions import CanGenerate, CanReset, IsDeveloper
from accounts.serializers import DeveloperSerializer
from accounts.tokens import account_activation_token
from accounts.api_keys import NewKey

User = get_user_model()


class DeveloperSignupView(generics.CreateAPIView):
    """Creates a developer account using the provided account details"""
    serializer_class = DeveloperSerializer
    permission_classes = ()
    authentication_classes = ()


class GenerateApiKeyView(views.APIView):
    """Generates an api key for authenticated developers who have no record of generating any in the past"""
    permission_classes = [IsAuthenticated, IsDeveloper, CanGenerate]

    def post(self, request):
        api_key, key = NewKey.generate(request.user.id)
        content = {'apiKey': key}
        return Response(content, status=status.HTTP_200_OK)


class ResetApiKeyView(views.APIView):
    """Revokes old and generates new api key for authenticated developers"""
    permission_classes = [IsAuthenticated, IsDeveloper, CanReset]

    def post(self, request):
        api_key, key = NewKey.reset(request.user.id)
        content = {'apiKey': key}
        return Response(content, status=status.HTTP_200_OK)

class ActivateEmailView(views.APIView):
    """Sends email activation link to the provided email during signup"""
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
            content = {"message": "Account activated succuessfully!"}
            return Response(content, status=status.HTTP_200_OK)
        else:
            content = {'detail': "Invalid activation link"}
            return Response(content, status=status.HTTP_400_BAD_REQUEST)
