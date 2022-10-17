from rest_framework import serializers
from stocks_v1.models import Stock, StockTracker
from django.contrib.auth import get_user_model


User = get_user_model()


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password', 'role']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User(email=validated_data['email'],
                    username=validated_data['username'], role=validated_data['role'])
        user.set_password(validated_data['password'])
        user.save()
        return user


class StockSerializer(serializers.HyperlinkedModelSerializer):
    id = serializers.SerializerMethodField()

    class Meta:
        model = Stock
        fields = [
            'id',
            'category',
            'name',
            'ticker',
            'volume',
            'price',
            'prev_price',
            'open_price',
            'percentage_change',
            'max_price',
            'min_price',
            'updated_at',
        ]

    def get_id(self, obj):
        return obj.pk


class TrackerSerializer(serializers.ModelSerializer):
    stock = serializers.StringRelatedField()

    class Meta:
        model = StockTracker
        fields = [
            "id",
            "stock",
            "quote_price",
            "at_tracking",
            "matched",
            "start_date",
            "last_updated",
            "matched_date"
        ]

    def get_stock(self, obj):
        return obj.ticker
