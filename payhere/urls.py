from django.urls import path, include

urlpatterns = [
    path('users', include('users.urls')),
    path('account-books', include('account_books.urls')),
]
