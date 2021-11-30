from django.views import View
from django.http import HttpResponse


class PingPong(View):
    def get(self, request):
        return HttpResponse("pong")