from django.urls import path

from .views import CreateAccountBookView


urlpatterns = [
    path('', CreateAccountBookView.as_view()),
]