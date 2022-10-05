from curses import raw
from simple_history.utils import update_change_reason
from api.serializers import StockSerializer, TrackerSerializer
from rest_framework import views, generics, viewsets
from stocks_v1.models import Stock, Tracker
from rest_framework import status
from rest_framework.response import Response
from updater.notifications import Notification


class RealTimeStocks(generics.ListAPIView):
    queryset = Stock.objects.all()
    serializer_class = StockSerializer


class HistoricalStocks(generics.ListAPIView):
    queryset = Stock.history.all()
    serializer_class = StockSerializer

    def get_queryset(self):
        return self.queryset.filter(ticker=self.request.GET.get('ticker'))


class AdminApiView(views.APIView):

    def post(self, request):
        stocks = request.data['stocks']
        created_stocks = {"stocks": []}
        for stock in stocks:
            serializer = StockSerializer(data=stock)
            if serializer.is_valid():
                created_stock = serializer.save()
                created_stocks['stocks'].append(serializer.data)
                update_change_reason(created_stock, "Genesis Stock")

        return Response(created_stocks, status=status.HTTP_201_CREATED)

    def put(self, request, format=None):
        stocks = request.data['stocks']
        updated_stocks = {"stocks": []}
        queryset = Stock.objects.all()
        for stock in stocks:
            instance = queryset.get(ticker=stock['ticker'])
            serializer = StockSerializer(
                instance, data=stock, context={'request': request})
            if stock['percentage_change'] != float(instance.percentage_change) and serializer.is_valid():
                updated_stock = serializer.save()
                updated_stocks['stocks'].append(serializer.data)
                update_change_reason(updated_stock, "Update")
        return Response(updated_stocks)


class TrackerViewSet(viewsets.ModelViewSet):
    queryset = Tracker.objects.all()
    serializer_class = TrackerSerializer

    def get_queryset(self):
        return self.queryset.filter(investors=self.request.user)

    def perform_create(self, serializer):
        ticker = self.request.data['stock']
        quote_price = float(self.request.data['quote_price'])
        stock = Tracker.check_stock(ticker, quote_price)

        if not stock:
            stock = serializer.save()
        stock.investors.add(self.request.user)
