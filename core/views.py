from django.shortcuts import redirect
from django.urls import reverse


def error_404_view(request, exception):
    return redirect(reverse("schema-redoc"))
