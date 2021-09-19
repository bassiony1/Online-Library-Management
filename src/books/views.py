from django.core.paginator import Paginator
from django.db.models.deletion import SET_NULL
from books.forms import Borrow
from django.shortcuts import render , redirect
from .models import book
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.mixins import LoginRequiredMixin , UserPassesTestMixin
from django.views.generic import (  CreateView , UpdateView , DeleteView)
from .filters import BookFilter
from datetime import datetime
from django.utils import timezone
from blog.models import post
# Create your views here.
@login_required
def home (request):
    borrowed_books = book.objects.filter(borrowed=True)
    for bookie in borrowed_books :
        if bookie.return_date <= timezone.now() :
            bookie.borrowed = False
            bookie.borrowed_by = None
            bookie.borrowed_date = None
            bookie.save()
    books = book.objects.filter(borrowed=False).order_by('-upload_date')[:6]
    posts = post.objects.all().order_by('-date')[:3]
    
    return render(request, 'books/home.html' , {'books' : books , 'posts':posts })






@login_required
def all_books(request):
    borrowed_books = book.objects.filter(borrowed=True)
    for bookie in borrowed_books :
        if bookie.return_date <= timezone.now() :
            bookie.borrowed = False
            bookie.borrowed_by = None
            bookie.borrowed_date = None
            bookie.save()
    books = book.objects.filter(borrowed=False).order_by('-upload_date')
   
    myfilter = BookFilter(request.GET , queryset=books)
    books = myfilter.qs
    paginator = Paginator(books , 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'books/all_books.html' , {'books' : page_obj , 'myfilter':myfilter})
    
@login_required
def bookdetail(request,id):
    d_book = book.objects.get(id=id)
    u_books = book.objects.filter(owner= d_book.owner , borrowed = False).order_by('-upload_date').exclude(id=id)[:3]
    c_books = book.objects.filter(category__in= d_book.category.all() , borrowed = False).distinct().order_by('-upload_date').exclude(id=id)[:3]
    if request.method == 'POST':
        borrowform= Borrow(request.POST , instance=d_book)
        if borrowform.is_valid() :
            is_borrowed = borrowform.cleaned_data['borrowed']
            if d_book.owner != request.user and is_borrowed :
                my_form = borrowform.save(commit=False)
                my_form.borrowed_by = request.user
                d_book.borrowed_date = timezone.now()
                d_book.save()
                my_form.save()
            elif d_book.owner == request.user and is_borrowed==False:
                my_form = borrowform.save(commit=False)
                my_form.borrowed_by = None
                d_book.borrowed_date = None
                my_form.save()
            elif d_book.owner != request.user and is_borrowed==False:
                my_form = borrowform.save(commit=False)
                my_form.borrowed_by = None
                d_book.borrowed_date = None
                my_form.save()
            
        return redirect('all-books')
    else :
            
        return render(request , 'books/book.html', {'book':d_book , 'form':Borrow(instance=d_book) , 
       'u_books' : u_books , 'c_books' : c_books})


@user_passes_test(lambda u: u.is_superuser)
@login_required
def borrowed_books(request):
    books = book.objects.filter(borrowed=True)
    for bookie in books :
        if bookie.return_date <= timezone.now() :
            bookie.borrowed = False
            bookie.borrowed_by = None
            bookie.borrowed_date = None
            bookie.save()
    books.order_by('upload_date')
    myfilter = BookFilter(request.GET , queryset=books)
    books = myfilter.qs
    return render(request, 'books/borrowed_books.html', {'books':books , 'myfilter':myfilter})



class AddBookView(LoginRequiredMixin , CreateView):

    model = book
    fields = ['name' , 'description' , 'cover' , 'borrowing_duration']
    def form_valid(self, form):
        form.instance.owner = self.request.user

        return super().form_valid(form)


class UpdateBookView(LoginRequiredMixin ,UserPassesTestMixin, UpdateView):
    model = book
    fields = ['name' , 'description' , 'cover' , 'borrowing_duration']
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