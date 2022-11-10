from rest_framework import serializers
from stocks.models import Stock


class StockSerializer(serializers.ModelSerializer):
    id = serializers.SerializerMethodField()

    class Meta:
        model = Stock
        fields = "__all__"

    def get_id(self, obj):
        return obj.pk
