from rest_framework import serializers
from stocks_v1.models import Stock


class StockSerializer(serializers.ModelSerializer):

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
