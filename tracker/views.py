from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from tracker.serializers import TrackerSerializer
from tracker.models import Tracker


class TrackerViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Tracker.objects.all()
    serializer_class = TrackerSerializer

    def get_queryset(self):
        return self.queryset.filter(investors=self.request.user)

    def perform_create(self, serializer):
        id = self.request.data['stock']
        quote_price = float(self.request.data['quote_price'])
        stock = Tracker.check_match(id, quote_price)
        if not stock:
            stock = serializer.save()
        stock.investors.add(self.request.user)
