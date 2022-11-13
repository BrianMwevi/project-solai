from rest_framework.permissions import IsAuthenticated
from rest_framework import generics, views, status
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenRefreshSerializer

from django.contrib.auth import get_user_model
from django.utils.encoding import force_text
from django.utils.http import urlsafe_base64_decode
from django.utils.decorators import method_decorator

from drf_yasg.utils import swagger_auto_schema
from drf_yasg.openapi import Schema, TYPE_OBJECT, TYPE_STRING

from accounts.permissions import CanGenerateKey, IsDeveloper
from accounts.serializers import UserSerializer, LoginSerializer, ChangePasswordSerializer
from accounts.tokens import account_activation_token
from accounts.api_keys import NewKey
from core.tasks import LongTasks
from clock import scheduler

User = get_user_model()


@method_decorator(name='post', decorator=swagger_auto_schema(
    operation_summary="Signup User",
    operation_description="Creates a user account using the provided account details",
    tags=["User Authentication"],
))
class SignupView(generics.CreateAPIView):
    serializer_class = UserSerializer
    permission_classes = ()
    authentication_classes = ()


@method_decorator(name='post', decorator=swagger_auto_schema(
    operation_summary='Login User',
    operation_description='Takes users email and password, authenticates and generates access token',
    tags=['User Authentication'],
    responses={status.HTTP_200_OK:  TokenRefreshSerializer},
))
class LoginView(TokenObtainPairView):

    authentication_classes = ()
    permission_classes = ()
    serializer_class = LoginSerializer


@method_decorator(name='post', decorator=swagger_auto_schema(
    operation_summary="Logout Current Session",
    operation_description="Logs out the requesting user and blacklists the refresh_token sent in the body",
    tags=["User Authentication"],
    request_body=TokenRefreshSerializer,
    responses={status.HTTP_200_OK: '', status.HTTP_400_BAD_REQUEST: ''},
))
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


@method_decorator(name='post', decorator=swagger_auto_schema(
    operation_summary="Logout everywhere",
    operation_description="Logs out the user and blacklists all the refresh tokens linked to the user",
    tags=["User Authentication"],
    request_body=TokenRefreshSerializer,
    responses={status.HTTP_200_OK: '', status.HTTP_400_BAD_REQUEST: ''}
))
class LogoutAllView(views.APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        scheduler.add_job(LongTasks.blacklist_user_tokens,
                          args=[request.user.id])
        return Response(status=status.HTTP_205_RESET_CONTENT)


@method_decorator(name='post', decorator=swagger_auto_schema(
    operation_summary="Generate New ApiKey",
    operation_description="Generates an api key for an authenticated user who have no record of generating any in the past",
    tags=['ApiKeys'],
    responses={status.HTTP_201_CREATED: Schema(
        type=TYPE_OBJECT,
        properties={
            'api_key': Schema(
               type=TYPE_STRING
               )
        }
    )
    },
))
class GenerateApiKeyView(views.APIView):
    permission_classes = [IsAuthenticated, IsDeveloper, CanGenerateKey]

    def post(self, request):
        _, key = NewKey.generate(request.user.id)
        content = {'api_key': key}
        return Response(content, status=status.HTTP_200_OK)


@method_decorator(name='post', decorator=swagger_auto_schema(
    operation_summary="Replace Existing ApiKey",
    operation_description="Revokes old and generates new ApiKey for authenticated developers",
    tags=['ApiKeys'],
    responses={status.HTTP_201_CREATED: Schema(
        type=TYPE_OBJECT,
        properties={
            'api_key': Schema(
                type=TYPE_STRING
            )
        }
    )
    },
))
class ResetApiKeyView(views.APIView):
    permission_classes = [IsAuthenticated, ~CanGenerateKey]

    def post(self, request):
        _, key = NewKey.reset(request.user.id)
        content = {'api_key': key}
        return Response(content, status=status.HTTP_200_OK)


@method_decorator(name='get', decorator=swagger_auto_schema(
    operation_summary="Email user",
    operation_description="Sends a confirmation email to the requested user in the background",
    tags=["Email"],
    responses={status.HTTP_200_OK: TokenRefreshSerializer,
               status.HTTP_404_NOT_FOUND: ""},
))
class EmailUserView(views.APIView):
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
        content = {'message': 'Invalid confirmation link'}
        return Response(content, status=status.HTTP_400_BAD_REQUEST)


@method_decorator(name='post', decorator=swagger_auto_schema(
    operation_summary="Forgot password",
    operation_description="Takes user's email address and sends a password reset confirmation email if a user with that email exists",
    tags=["User Authentication"],
    request_body=Schema(
        type=TYPE_OBJECT,
        properties={
            'email': Schema(type=TYPE_STRING, description='string'),
        },
        required=['email'],
    ),
    responses={status.HTTP_200_OK: ""}
))
class ForgotPasswordView(views.APIView):
    permission_classes = ()
    authentication_classes = ()

    def post(self, request):
        try:
            user = User.get_user_by_email(request.data['email'])
            mail_subject = "Solai Account Password Reset"
            template = 'accounts/password_reset.html'
            scheduler.add_job(LongTasks.send_email, args=[
                request, user, mail_subject, template])
        except (KeyError, User.DoesNotExist):
            pass
        return Response(status=status.HTTP_200_OK)


@method_decorator(name='put', decorator=swagger_auto_schema(
    operation_summary="Change User Password",
    operation_description="Sets new password for a user and blacklists all associated refresh tokens",
    tags=["User Authentication"],
    request_body=ChangePasswordSerializer,
    responses={status.HTTP_200_OK: ""}
))
@method_decorator(name='patch', decorator=swagger_auto_schema(
    operation_summary="Change User Password",
    operation_description="Sets new password for a user and blacklists all associated refresh tokens",
    tags=["User Authentication"],
    auto_schema=None,
    request_body=ChangePasswordSerializer,
    responses={status.HTTP_200_OK: ""}
))
class ChangePasswordView(generics.UpdateAPIView):
    serializer_class = ChangePasswordSerializer
    permission_classes = [IsAuthenticated]

    def put(self, request, *args, **kwargs):
        user = self.request.user
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            old_password = serializer.data.get('old_password')
            if not user.check_password(old_password):
                content = {'old_password': 'Wrong password'}
                return Response(content, status=status.HTTP_400_BAD_REQUEST)
            new_password = serializer.data.get('new_password')
            user.set_password(new_password)
            user.save()

            response = {
                'status': 'success',
                'code': status.HTTP_200_OK,
            }
            return Response(response)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
