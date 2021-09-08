from django.urls import path
from . import views as book_views

urlpatterns = [
    path('', book_views.all_books , name='all-books'),
]