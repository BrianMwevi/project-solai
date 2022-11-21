from rest_framework import serializers
from stocks_v1.models import Stock


class StockSerializer(serializers.ModelSerializer):
    id = serializers.SerializerMethodField()

    class Meta:
        model = Stock
        fields = "__all__"

    def get_id(self, obj):
        return obj.pk


class HistorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Stock
        fields = ['price', 'updated_at']
