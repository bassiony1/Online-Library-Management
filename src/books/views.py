import os
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.db.models.deletion import SET_NULL
from django.http.response import HttpResponse
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
from random import choice
from testimonials.models import testimonial
from django.core.mail import send_mail
from django.conf import settings
# Create your views here.
@login_required
def home (request):
    quotes = ['Only Those Who Risk Going Too Far Can Possibly Find out How Far one Can Go !',
                   'Life is But A Dream ' , 
                   "No matter Who You Think you are , you don't Really Know What kindna Man you've Become Until You Reach The very End , One realizes one's True Nature At The Time of Death" ,
                    "It Takes Great Talent And Skill To Conceal one's Talent And Skill " , 
                    "Te beauty of The First Snow of Winter and All The Sadness of Dead Flowers on A grave" ,
                    "When your Mind is Lost You Can't Meet Your Potentials" , 
                    "If we were  all on Trial for our thoughts , We would All be Hanged" ,
                    "When we're on The edge and have nowhere to go , The only thing that can support us is The Pride we Have " ,
                    "Strength Is nothing but Tolerance " ,
                    "EverythingShip" ,
                    "For Some Reason Recalling The Past always takes a strangely dark turn",
                    "Sometimes The Things You fall into by Chance turn out to be The most important once of all as long as you go into it with a tiny bit of wonder",
                    "if you spend too much time staring at the top , you'll have the rug pulled out from under you" ]

    quote = choice(quotes)
    borrowed_books = book.objects.filter(borrowed=True)
    for bookie in borrowed_books :
        if bookie.return_date <= timezone.now() :
            bookie.borrowed = False
            bookie.borrowed_by = None
            bookie.borrowed_date = None
            bookie.save()
    books = book.objects.filter(borrowed=False).order_by('-upload_date')[:6]
    posts = post.objects.all().order_by('-date')[:3]
    testimonials = testimonial.objects.filter(fav=True)[:2]
    
    return render(request, 'books/home.html' , {'books' : books , 'posts':posts  , 'quote': quote , 'testimonials':testimonials})






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
def owner_books(request , id):
    owner = User.objects.get(id=id)
    o_books = book.objects.filter(owner=owner,borrowed=False).order_by('-upload_date')
    paginator = Paginator(o_books , 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request , 'books/owner_books.html' ,  {'o_books':page_obj , 'owner':owner})

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
        paginator = Paginator(u_books , 3)
        page_number = request.GET.get('page')
        U_page_obj = paginator.get_page(page_number)  
        return render(request , 'books/book.html', {'book':d_book , 'form':Borrow(instance=d_book) , 
       'u_books' : U_page_obj , 'c_books' : c_books})


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
    paginator = Paginator(books , 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'books/borrowed_books.html', {'books':page_obj , 'myfilter':myfilter})




def contact_us(request):

    if request.method == 'POST':
        user_name = request.user.username
        subject = user_name + ' ' +',Thanks For Communcating With Us'
        message = 'We have Received Your Note And We wil Look into it '
        email = request.user.email
        print(email)
        send_mail(
            subject,
            message,
            settings.EMAIL_HOST_USER,
            recipient_list=[email],

        )

    return render(request , 'books/contact_us.html')


def about_us(request):

    return render(request , 'books/about_us.html')

class AddBookView(LoginRequiredMixin , CreateView):

    model = book
    fields = ['name' , 'description' , 'cover' , 'category' ,'borrowing_duration']
    def form_valid(self, form):
        form.instance.owner = self.request.user

        return super().form_valid(form)


class UpdateBookView(LoginRequiredMixin ,UserPassesTestMixin, UpdateView):
    model = book
    fields = ['name' , 'description' , 'cover' ,'category', 'borrowing_duration']
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