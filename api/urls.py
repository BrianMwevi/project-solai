from django.urls import path, re_path

from rest_framework.routers import DefaultRouter
from rest_framework import permissions

from api.views import AdminApiView, HistoricalStocks, RealTimeStocks
from drf_yasg.views import get_schema_view
from drf_yasg import openapi


schema_view = get_schema_view(
    openapi.Info(
        title="Kenya Stocks API",
        default_version='v1',
        description="Free and open stocks API that is populated with publicly available data",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="mwevibrian@gmail.com"),
        license=openapi.License(name="MIT"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)


routes = DefaultRouter()
urlpatterns = [
    path('realtime/', RealTimeStocks.as_view(), name="realtime_stocks"),
    path('realtime/admin/', AdminApiView.as_view(), name="admin"),
    path('history/', HistoricalStocks.as_view(), name="history_stocks"),
    re_path(r'^swagger(?P<format>\.json|\.yaml)$',
            schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('', schema_view.with_ui('swagger',
            cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc',
                                 cache_timeout=0), name='schema-redoc'),
]
urlpatterns += routes.urls
