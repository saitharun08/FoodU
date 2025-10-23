from django.urls import path
from django.http import HttpResponse

def placeholder_view(request):
    return HttpResponse("Chat placeholder")

urlpatterns = [
    path("", placeholder_view, name="chat-home"),
]
