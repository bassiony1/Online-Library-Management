from django.shortcuts import render
from .models import book
from django.contrib.auth.decorators import login_required
# Create your views here.
@login_required
def all_books(request):
    books = book.objects.filter(borrowed=False)

    return render(request, 'books/home.html' , {'books' : books})
