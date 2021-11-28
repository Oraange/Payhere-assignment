from django.urls import path

from .views import AccountBookView, AccountBookDetailView


urlpatterns = [
    path('', AccountBookView.as_view()),
    path('/<int:book_id>', AccountBookDetailView.as_view()),
]