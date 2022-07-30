from simple_history.utils import update_change_reason
from api.serializers import StockSerializer
from rest_framework import viewsets, views
from stocks_v1.models import Stock
from rest_framework import status
from rest_framework.response import Response


class StockViewset(viewsets.ModelViewSet):
    serializer_class = StockSerializer
    queryset = Stock.objects.all()


class StockUpdateView(views.APIView):

    def post(self, request):
        for stock in request.data['stocks']:
            serializer = StockSerializer(data=stock)
            if serializer.is_valid():
                created_stock = serializer.save()
                update_change_reason(created_stock, "Genesis Stock")
        return Response(status=status.HTTP_201_CREATED)

    def put(self, request, format=None):

        for stock in request.data['stocks']:
            obj = Stock.objects.get(ticker=stock['ticker'])
            serializer = StockSerializer(
                obj, data=stock, context={'request': request})
            if serializer.is_valid():
                updated_stock = serializer.save()
                update_change_reason(updated_stock, "Update")
        return Response(serializer.data)
