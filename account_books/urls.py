from django.urls import path

from .views import (
    AccountBookDetailView,
    AccountBookView, 
    TrashedBookView
)

urlpatterns = [
    path('', AccountBookView.as_view()),
    path('/<int:book_id>', AccountBookDetailView.as_view()),
    path('/trash/restore/<int:book_id>', TrashedBookView.as_view()),
    path('/trash', TrashedBookView.as_view()),
]