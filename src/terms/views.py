from django.db.models import fields
from django.forms.models import ALL_FIELDS
from django.shortcuts import render
from django.views.generic.detail import DetailView
from .models import terms
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.shortcuts import render , redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.mixins import LoginRequiredMixin , UserPassesTestMixin
from django.views.generic import (  CreateView , UpdateView , DeleteView , DetailView)
# Create your views here.



def allterms(request):
    all_terms = terms.objects.all().order_by('number')
    paginator = Paginator(all_terms , 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request , 'terms/terms.html' , {'all_terms':page_obj})

class TermCreateView(LoginRequiredMixin,UserPassesTestMixin ,CreateView):
    model = terms
    fields = ALL_FIELDS
    def test_func(self):
        if self.request.user.is_superuser :
            return True
        return False
class TermDetailView(LoginRequiredMixin,UserPassesTestMixin , DetailView):
    model = terms
    context_object_name = 'term'
    def form_valid(self, form):
        form.instance.writer = self.request.user

        return super().form_valid(form)
    def test_func(self):
        if self.request.user.is_superuser :
            return True
        return False

class TermUpdateView(LoginRequiredMixin ,UserPassesTestMixin,UpdateView):
    model = terms
    fields = ['title', 'description' , 'number' ]
    def form_valid(self, form):
        form.instance.writer = self.request.user
        return super().form_valid(form)
    def test_func(self):
        term = self.get_object()
        if term.writer == self.request.user and self.request.user.is_superuser :
            return True
        return False
class TermDeleteView(LoginRequiredMixin ,UserPassesTestMixin,DeleteView):
    model = terms
    success_url = '/terms'
    def test_func(self):
        if self.request.user.is_superuser :
            return True
        return False
