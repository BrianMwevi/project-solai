from rest_framework import serializers
from django.contrib.auth import get_user_model
from accounts.models import Developer, Trader, Investor, Admin


User = get_user_model()


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        username = validated_data['username']
        email = validated_data['email']
        password = validated_data['password']
        usage = validated_data['usage']

        user = User(email=email, username=username, usage=usage)
        user.set_password(password)
        user.save()
        return user

