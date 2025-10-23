from django.urls import path
from django.http import HttpResponse

def placeholder_view(request):
    return HttpResponse("Orders placeholder")

urlpatterns = [
    path("", placeholder_view, name="orders-home"),
]
