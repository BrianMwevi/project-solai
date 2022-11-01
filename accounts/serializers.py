from rest_framework import serializers
from django.contrib.auth import get_user_model
from emailer.confirmation_email import EmailConfirmation
from accounts.models import Developer, Trader, Investor, Admin
from asgiref.sync import async_to_sync
from rest_framework_api_key.models import APIKey
User = get_user_model()


class DeveloperSerializer(serializers.ModelSerializer):

    class Meta:
        model = Developer
        fields = ['id', 'username', 'email', 'password', 'usage', 'role']
        extra_kwargs = {'password': {'write_only': True},
                        }

    def create(self, validated_data):
        username = validated_data['username']
        email = validated_data['email']
        password = validated_data['password']
        usage = validated_data['usage']
        role = validated_data['role']

        user = User(email=email, username=username, usage=usage, role=role)
        user.set_password(password)
        user.save()
        sent_email = async_to_sync(
            EmailConfirmation.signup)(self.context['request'], user)
        return user
