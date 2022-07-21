from api.serializers import StockSerializer
from rest_framework import generics, viewsets
from stocks_v1.models import Stock
from rest_framework import serializers, status
from rest_framework.response import Response


class StockViewset(viewsets.ModelViewSet):
    serializer_class = StockSerializer
    queryset = Stock.objects.all()
