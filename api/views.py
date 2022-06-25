from api.serializers import StockSerializer
from rest_framework import generics
from stocks_v1.models import Stock


class StockList(generics.ListAPIView):
    serializer_class = StockSerializer
    queryset = Stock.objects.all()
