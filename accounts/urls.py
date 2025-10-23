from django.urls import path
from django.http import HttpResponse

def placeholder_view(request):
    return HttpResponse("Accounts placeholder")

urlpatterns = [
    path("", placeholder_view, name="accounts-home"),
]
