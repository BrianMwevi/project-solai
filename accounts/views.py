from rest_framework.permissions import IsAuthenticated
from rest_framework import generics, views, status
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken, OutstandingToken, BlacklistedToken

from django.contrib.auth import get_user_model
from django.utils.encoding import force_text
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth import login

from drf_yasg.utils import swagger_auto_schema

from accounts.permissions import CanGenerate, IsDeveloper
from accounts.serializers import DeveloperSerializer
from accounts.tokens import account_activation_token
from accounts.api_keys import NewKey
from emailer.confirmation_email import EmailConfirmation
from clock import scheduler

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
        _, key = NewKey.generate(request.user.id)
        content = {'apiKey': key}
        return Response(content, status=status.HTTP_200_OK)


class ResetApiKeyView(views.APIView):
    """Revokes old and generates new api key for authenticated developers"""
    permission_classes = [IsAuthenticated, IsDeveloper, ~CanGenerate]

    def post(self, request):
        _, key = NewKey.reset(request.user.id)
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
            refresh = RefreshToken.for_user(user)
            content = {"refresh": str(refresh),
                       "access": str(refresh.access_token)}
            return Response(content, status=status.HTTP_200_OK)

        return Response(status=status.HTTP_400_BAD_REQUEST)


class ResetPasswordView(views.APIView):
    permission_classes = ()
    authentication_classes = ()

    def post(self, request):
        if request.data.get('email', None):
            user = User.get_user_by_email(request.data['email'])
            mail_subject = "Solai Account Password Reset"
            template = 'accounts/password_reset.html'
            scheduler.add_job(EmailConfirmation.email_user, args=[
                request, user, mail_subject, template])
        return Response(status=status.HTTP_200_OK)


class SetNewPasswordView(views.APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        request.user.set_password(request.data['password'])
        request.user.save()
        return Response(status=status.HTTP_201_CREATED)


class LogoutView(views.APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.data["refresh_token"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class LogoutAllView(views.APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        tokens = OutstandingToken.objects.filter(user_id=request.user.id)
        [BlacklistedToken.objects.get_or_create(token=token)
         for token in tokens]
        return Response(status=status.HTTP_205_RESET_CONTENT)
