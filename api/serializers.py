from rest_framework import serializers
from stocks_v1.models import Stock, Tracker


class StockSerializer(serializers.HyperlinkedModelSerializer):
    # url = serializers.HyperlinkedIdentityField(view_name='admin-detail')

    class Meta:
        model = Stock
        fields = [
            # 'url',
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

    def get_stock(self,obj):
        return obj.ticker