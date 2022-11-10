from rest_framework import views, status
from rest_framework.response import Response
from simple_history.utils import update_change_reason
from rest_framework_api_key.permissions import HasAPIKey

from stocks.models import Stock
from stocks.serializers import StockSerializer
from accounts.permissions import IsStockAdmin


class HistoryView(views.APIView):
    permission_classes = [HasAPIKey]

    def get(self, request):
        ticker = request.data.get('ticker')
        start_date = request.data.get('startDate')
        end_date = request.data.get('endDate')

        if ticker and start_date:
            ticker = ticker.upper()
            serializer = StockSerializer(Stock.get_history(
                ticker, start_date, end_date), many=True)
            content = {"data": serializer.data}
            return Response(content, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_404_NOT_FOUND)


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
                print("Data ready to be saved!")
                updated_stock = serializer.save()
                updated_stocks['stocks'].append(serializer.data)
                update_change_reason(updated_stock, "Update")
        return Response(updated_stocks)
