from django.urls import path

from rest_framework.routers import DefaultRouter

from api.views import StockUpdateView, StockViewset

routes = DefaultRouter()

routes.register('stocks', StockViewset, basename='stock')
urlpatterns = [
    path('stocks/crud/', StockUpdateView.as_view()),
]

urlpatterns += routes.urls
