from django.urls import path

from rest_framework.routers import DefaultRouter

from api.views import StockViewset

routes = DefaultRouter()

routes.register('stocks', StockViewset, basename='stock')
urlpatterns = [
    # path('stocks/', StockList.as_view(), name='stock-list'),
    # path('stocks/<int:id>/', StockDetail.as_view(), name='stock-detail'),
]

urlpatterns += routes.urls
