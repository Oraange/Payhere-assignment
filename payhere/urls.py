from django.urls import path, include

urlpatterns = [
    path('ping', include('core.urls')),
    path('users', include('users.urls')),
    path('account-books', include('account_books.urls')),
]
