from django.urls import path
from . import views as book_views

urlpatterns = [
    path('', book_views.home , name='home'),
    path('all_books/', book_views.all_books , name='all-books'),
    path('borrowed/', book_views.borrowed_books , name='borrowed-books'),
    path('<int:id>/', book_views.bookdetail, name='book-detail'),
    path('<int:pk>/update', book_views.UpdateBookView.as_view(), name='book-update'),
    path('<int:pk>/delete', book_views.DeleteBookView.as_view(), name='book-delete'),
    path('create/',book_views.AddBookView.as_view(), name='book-add') ,

]