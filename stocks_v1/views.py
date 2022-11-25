from rest_framework import views, status, generics
from rest_framework.response import Response
from rest_framework_api_key.permissions import HasAPIKey

from django.utils.decorators import method_decorator

from drf_yasg.utils import swagger_auto_schema

from simple_history.utils import update_change_reason

from stocks_v1.models import Stock
from stocks_v1.serializers import StockSerializer, HistorySerializer
from accounts.permissions import IsStockAdmin


@method_decorator(name='get', decorator=swagger_auto_schema(
    operation_summary="Stock History",
    operation_description="Fetches the history of specific stock using a ticker symbol, start and end date. Returns 404 if wrong ticker is passed",
    tags=['Stocks'],

    # responses={status.HTTP_200_OK: HistorySerializer(many=True)},
))
class HistoryView(generics.ListAPIView):
    permission_classes = [HasAPIKey]
    serializer_class = HistorySerializer

    def get(self, request, *args, **kwargs):
        ticker = request.data.get('ticker').upper()
        start_date = request.data.get('startDate')
        end_date = request.data.get('endDate')

        if ticker and start_date:
            ticker = ticker.upper()
            serializer = HistorySerializer(Stock.get_history(
                ticker, start_date, end_date), many=True)
            content = {"data": serializer.data}
            return Response(content, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_404_NOT_FOUND)


@method_decorator(name='post', decorator=swagger_auto_schema(
    operation_summary="Stock Creation",
    operation_description="Takes a list of stocks to be created and returns the created stocks",
    tags=['Stocks'],
    query_serializer=StockSerializer,
    auto_schema=None,
))
@method_decorator(name='put', decorator=swagger_auto_schema(
    operation_summary="Stock Update",
    operation_description="Takes a list of stocks to be updated and returns the updated stocks",
    tags=['Stocks'],
    query_serializer=StockSerializer,
    auto_schema=None,
))
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
