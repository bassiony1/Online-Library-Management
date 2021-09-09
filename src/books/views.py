from books.forms import Borrow
from django.shortcuts import render , redirect
from .models import book
from django.contrib.auth.decorators import login_required
# Create your views here.
@login_required
def all_books(request):
    books = book.objects.filter(borrowed=False)

    return render(request, 'books/home.html' , {'books' : books})

def bookdetail(request,id):
    d_book = book.objects.get(id=id)
    if request.method == 'POST':
        borrowform= Borrow(request.POST , instance=d_book)
        if borrowform.is_valid() :
            is_borrowed = borrowform.cleaned_data['borrowed']
            if d_book.owner != request.user :
                my_form = borrowform.save(commit=False)
                my_form.borrowed_by = request.user
                my_form.save()
            elif d_book.owner == request.user and is_borrowed==False:
                borrowform.save()
            
        return redirect('all-books')
    else :
            
        return render(request , 'books/book.html', {'book':d_book , 'form':Borrow(instance=d_book)})
    