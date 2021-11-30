from django.urls import path

from .views import PingPong


urlpatterns = [
    path('/pong', PingPong.as_view())
]