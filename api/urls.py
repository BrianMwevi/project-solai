from django.urls import path, include

from api.views import StockDetail, StockList


urlpatterns = [
    path('stocks/', StockList.as_view(), name='stock-list'),
]
