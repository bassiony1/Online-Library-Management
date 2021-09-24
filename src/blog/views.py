from django.shortcuts import redirect, render , reverse
from django.contrib.auth.models import User
from .models import post
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin , UserPassesTestMixin
from django.views.generic import (ListView , DetailView , CreateView , UpdateView , DeleteView)
from .filters import PostFilter
from django.core.paginator import Paginator
# Create your views here.
@login_required
def post_list(request):
    images = ['books/images/blog-1-720x480.jpg',
               'books/images/blog-2-720x480.jpg',
               'books/images/blog-3-720x480.jpg',
               'books/images/blog-4-720x480.jpg',
               'books/images/blog-5-720x480.jpg',
               'books/images/blog-6-720x480.jpg']
    posts = post.objects.all().order_by('-date')
    myfilter = PostFilter(request.GET , queryset=posts)
    posts = myfilter.qs
    paginator = Paginator(posts , 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request , 'blog/home.html', {'posts':page_obj , 'myfilter':myfilter ,'images' : images})


class PostDetailView(LoginRequiredMixin,DetailView):
    model = post
    context_object_name = 'post'

class PostCreateView(LoginRequiredMixin ,CreateView):
    model = post
    fields = ['title' , 'content' , 'image', 'spoiled']
    def form_valid(self , form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin ,UserPassesTestMixin, UpdateView):
    model = post
    fields = ['title' , 'content' , 'image']
    def form_valid(self , form):
        form.instance.author = self.request.user
        return super().form_valid(form)
    def test_func(self):
        post = self.get_object()
        if post.author == self.request.user :
            return True
        return False

class PostDeleteView(LoginRequiredMixin , UserPassesTestMixin , DeleteView):
    model = post
    success_url = '/blog'
    def test_func(self):
        post = self.get_object()
        if post.author == self.request.user or self.request.user.is_superuser :
            return True
        return False