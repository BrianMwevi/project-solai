from django.urls import path
from tracker.views import TrackerViewSet
from rest_framework.routers import DefaultRouter


routers = DefaultRouter()

routers.register('', TrackerViewSet, 'tracker')

urlpatterns = [
    # path("track/", TrackerViewSet, name="tracker")
]
urlpatterns += routers.urls
