from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('admin/', admin.site.urls),
    # path('api/v1/', include('api.urls')),
    # path('', include('api.urls')),
]
handler404 = 'core.views.error_404_view'
