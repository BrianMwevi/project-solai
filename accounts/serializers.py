from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers

from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group

from core.tasks import LongTasks
from clock import scheduler


class UserSerializer(serializers.ModelSerializer):
    password1 = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)

    def validate(self, data):
        if data['password1'] != data['password2']:
            raise serializers.ValidationError('Passwords must match.')
        if data['role'] not in get_user_model().Roles:
            raise serializers.ValidationError('Invalid user role')
        return data

    def create(self, validated_data):
        group, _ = Group.objects.get_or_create(name=validated_data['role'])
        data = {
            key: value for key, value in validated_data.items() if key not in ('password1', 'password2')
        }
        data['password'] = validated_data['password1']
        user = self.Meta.model.objects.create_user(**data)
        user.groups.add(group)
        user.save()
        mail_subject = "Solai Account Activation"
        template = 'accounts/account_activation_email.html'
        scheduler.add_job(LongTasks.send_email, args=[
                          self.context["request"], user, mail_subject, template])
        return user

    class Meta:
        model = get_user_model()
        fields = (
            'id', 'email', 'first_name', 'last_name', 'password1', 'password2', 'usage', 'role',
        )
        read_only_fields = ('id',)


class LoginSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        user_data = UserSerializer(user).data

        for key, value in user_data.items():
            if key != 'id':
                token[key] = value
        return token
