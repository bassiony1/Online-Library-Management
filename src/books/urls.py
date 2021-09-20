from django.urls import path
from . import views as book_views

urlpatterns = [
    path('', book_views.home , name='home'),
    path('all_books/', book_views.all_books , name='all-books'),
    path('borrowed/', book_views.borrowed_books , name='borrowed-books'),
    path('<int:id>/', book_views.bookdetail, name='book-detail'),
    path('<int:id>/books', book_views.owner_books, name='owner-books'),
    path('terms/', book_views.terms, name='terms'),
    path('contact/', book_views.contact_us, name='contact-us'),
    path('about/', book_views.about_us, name='about-us'),
    path('<int:pk>/update', book_views.UpdateBookView.as_view(), name='book-update'),
    path('<int:pk>/delete', book_views.DeleteBookView.as_view(), name='book-delete'),
    path('create/',book_views.AddBookView.as_view(), name='book-add') ,


]