from django.urls import path

from rest_framework.routers import DefaultRouter

from api.views import AdminApiView, HistoricalStocks, RealTimeStocks


routes = DefaultRouter()
urlpatterns = [
    path('realtime/', RealTimeStocks.as_view(), name="realtime_stocks"),
    path('realtime/admin/', AdminApiView.as_view(), name="admin"),
    path('history/', HistoricalStocks.as_view(), name="history_stocks"),
]
urlpatterns += routes.urls
