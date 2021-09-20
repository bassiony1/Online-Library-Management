from .models import testimonial
from django.shortcuts import redirect, render , reverse
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin , UserPassesTestMixin
from django.views.generic import (ListView , DetailView , CreateView , UpdateView , DeleteView)
from django.core.paginator import Paginator
from .forms import FavForm
# Create your views here.

def testimonail_list(request):
    testimonials = testimonial.objects.all().order_by('-fav' , 'date')
    paginator = Paginator(testimonials , 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request , 'testimonials/testimonials.html', {'testimonials':page_obj })


def testimonial_detail(request , id):
    d_testimonial = testimonial.objects.get(id=id)
    if request.method == 'POST':
        fav_form = FavForm(request.POST , instance=d_testimonial)
        if fav_form.is_valid():
            is_fav = fav_form.cleaned_data['fav']
            if is_fav :
                testimonial.fav = True
            else:
                testimonial.fav = False
            fav_form.save()
        return redirect('testimonials')
    else:
        fav_form = FavForm(instance=d_testimonial)
        return render(request , 'testimonials/testimonial_detail.html',
         {'testimonial': d_testimonial , 'fav_form': fav_form })

class TestimonialCreateView(LoginRequiredMixin ,CreateView):
    model = testimonial
    fields = ['content']
    def form_valid(self , form):
        form.instance.writer = self.request.user
        return super().form_valid(form)


class TestimonialUpdateView(LoginRequiredMixin ,UserPassesTestMixin, UpdateView):
    model = testimonial
    fields = ['content']
    def form_valid(self , form):
        form.instance.writer = self.request.user
        return super().form_valid(form)
    def test_func(self):
        testimonial = self.get_object()
        if testimonial.writer == self.request.user :
            return True
        return False

class TestimonialDeleteView(LoginRequiredMixin , UserPassesTestMixin , DeleteView):
    model = testimonial
    success_url = '/testimonails'
    def test_func(self):
        testimonial = self.get_object()
        if testimonial.writer == self.request.user or self.request.user.is_superuser :
            return True
        return False