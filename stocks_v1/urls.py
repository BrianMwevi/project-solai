from django.urls import path
from stocks_v1.views import AdminApiView, HistoryView

urlpatterns = [
    path('realtime/', AdminApiView.as_view(), name='realtime'),
    path('history/', HistoryView.as_view(), name='history'),
]
