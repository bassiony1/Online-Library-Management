from django.db.models.deletion import SET_NULL
from books.forms import Borrow
from django.shortcuts import render , redirect
from .models import book
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.mixins import LoginRequiredMixin , UserPassesTestMixin
from django.views.generic import (  CreateView , UpdateView , DeleteView)

# Create your views here.
@login_required
def all_books(request):
    books = book.objects.filter(borrowed=False).order_by('-upload_date')
    
    return render(request, 'books/home.html' , {'books' : books})
    
@login_required
def bookdetail(request,id):
    d_book = book.objects.get(id=id)
    if request.method == 'POST':
        borrowform= Borrow(request.POST , instance=d_book)
        if borrowform.is_valid() :
            is_borrowed = borrowform.cleaned_data['borrowed']
            if d_book.owner != request.user and is_borrowed :
                my_form = borrowform.save(commit=False)
                my_form.borrowed_by = request.user
                my_form.save()
            elif d_book.owner == request.user and is_borrowed==False:
                my_form = borrowform.save(commit=False)
                my_form.borrowed_by = None
                my_form.save()
            elif d_book.owner != request.user and is_borrowed==False:
                print('We Got Here')
                my_form = borrowform.save(commit=False)
                my_form.borrowed_by = None
                my_form.save()
            
        return redirect('all-books')
    else :
            
        return render(request , 'books/book.html', {'book':d_book , 'form':Borrow(instance=d_book)})


@user_passes_test(lambda u: u.is_superuser)
@login_required
def borrowed_books(request):
    books = book.objects.filter(borrowed=True).order_by('upload_date')

    return render(request, 'books/borrowed_books.html', {'books':books})



class AddBookView(LoginRequiredMixin , CreateView):

    model = book
    fields = ['name' , 'description' , 'cover']
    def form_valid(self, form):
        form.instance.owner = self.request.user

        return super().form_valid(form)


class UpdateBookView(LoginRequiredMixin ,UserPassesTestMixin, UpdateView):
    model = book
    fields = ['name' , 'description' , 'cover']
    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)
    def test_func(self):
        book = self.get_object()
        if book.owner == self.request.user and self.request.user.is_superuser :
            return True
        return False
    
class DeleteBookView(LoginRequiredMixin , UserPassesTestMixin , DeleteView):
    model = book
    success_url = '/'
    def test_func(self):
        if self.request.user.is_superuser :
            return True
        return False