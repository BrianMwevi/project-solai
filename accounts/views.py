from accounts.permissions import IsAdmin, IsDeveloper, IsInvestor, IsTrader
from accounts.serializers import DeveloperSerializer
from django.contrib.auth import get_user_model
from rest_framework import generics, views, status
from rest_framework.permissions import IsAuthenticated
from django.utils.encoding import force_text
from django.utils.http import urlsafe_base64_decode
from accounts.tokens import account_activation_token
from rest_framework.response import Response
from django.contrib.auth import login
from accounts.api_keys import NewKey

User = get_user_model()


class DeveloperSignupView(generics.CreateAPIView):
    """
    Handles user account creation
    """
    serializer_class = DeveloperSerializer
    permission_classes = ()
    authentication_classes = ()


class GenerateApiKeyView(views.APIView):
    permission_classes = [IsAuthenticated, IsDeveloper]

    def post(self, request):
        api_key, expiry_date = NewKey.generate(request.user.id)
        content = {'apiKey': api_key, 'expiry': expiry_date}
        return Response(content, status=status.HTTP_200_OK)


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
            user.is_active = True
            user.save()
            login(request, user)
            content = {"data": "Account activated succuessfully!"}
            return Response(content, status=status.HTTP_200_OK)
        else:
            content = {'data': "Invalid activation link"}
            return Response(content, status=status.HTTP_400_BAD_REQUEST)
