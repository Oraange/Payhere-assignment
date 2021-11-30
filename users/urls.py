from django.urls import path

from .views import SignInView, SignUpView, LogOutView


urlpatterns = [
    path('/sign-up', SignUpView.as_view()),
    path('/sign-in', SignInView.as_view()),
    path('/log-out', LogOutView.as_view()),
]