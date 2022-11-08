from rest_framework import generics, views, status
from rest_framework.response import Response
from simple_history.utils import update_change_reason
from rest_framework_api_key.permissions import HasAPIKey

from stocks.models import Stock
from stocks.serializers import StockSerializer
from accounts.permissions import IsStockAdmin


class RealTimeStocks(generics.ListAPIView):
    queryset = Stock.objects.all()
    serializer_class = StockSerializer
    # permission_classes = [HasAPIKey, IsAdmin |IsInvestor | IsTrader | IsDeveloper]

    # def get_throttles(self):
    #     throttle_classes = []
    #     if self.request.user.role == "DEVELOPER":
    #         throttle_classes = [DeveloperThrottle]
    #     elif self.request.user.role == "INVESTOR":
    #         throttle_classes = [InvestorThrottle]
    #     elif self.request.user.role == "TRADER":
    #         throttle_classes = [TraderThrottle]
    #     return [throttle() for throttle in throttle_classes]


class HistoryView(generics.ListAPIView):
    queryset = Stock.history.all()
    serializer_class = StockSerializer
    # permission_classes = [IsAuthenticated, IsAdmin |
    #                       IsInvestor | IsTrader | IsDeveloper]

    # def get_throttles(self):
    #     throttle_classes = []
    #     if self.request.user.role == "DEVELOPER":
    #         throttle_classes = [DeveloperThrottle]
    #     elif self.request.user.role == "INVESTOR":
    #         throttle_classes = [InvestorThrottle]
    #     elif self.request.user.role == "TRADER":
    #         throttle_classes = [TraderThrottle]
    #     return [throttle() for throttle in throttle_classes]

    def get_queryset(self):
        return self.queryset.filter(ticker=self.request.GET.get('ticker'))[:30]


class AdminApiView(views.APIView):
    permission_classes = [HasAPIKey, IsStockAdmin]

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
            if stock['change'] != float(instance.change) and serializer.is_valid():
                updated_stock = serializer.save()
                updated_stocks['stocks'].append(serializer.data)
                update_change_reason(updated_stock, "Update")
        return Response(updated_stocks)
