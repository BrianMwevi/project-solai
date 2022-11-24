from rest_framework import serializers
from stocks_v1.models import Stock, Tracker


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


class TrackerSerializer(serializers.ModelSerializer):
    stock = serializers.StringRelatedField()

    class Meta:
        model = Tracker
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
