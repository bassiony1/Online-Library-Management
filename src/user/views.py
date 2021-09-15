from django.contrib.auth.models import User
from user.forms import AdminForm, ProfileUpdateForm, UserUpdateForm , UserCreationForm , UserRegisterForm
from django.contrib.auth.decorators import login_required , user_passes_test
from django.shortcuts import render , redirect , reverse
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
from .models import Profile
from books.models import book
from django.contrib.auth.mixins import LoginRequiredMixin , UserPassesTestMixin
from django.views.generic import (DeleteView)
from .filters import ProfilesFilter


# Create your views here.
def userRegisterForm(request):
    logout(request)
    if request.method == 'POST':
        r_form = UserRegisterForm(request.POST)
        if r_form.is_valid():
            r_form.save()
            username = r_form.cleaned_data['username']
            password = r_form.cleaned_data['password1']
            user = authenticate(username=username, password=password)
            login(request,user)
        return redirect('profile')
    else:
        r_form = UserRegisterForm()
        return render(request,'user/register.html',{'r_form':r_form})
@login_required
def profile(request):
    borrowed_books = book.objects.filter(borrowed_by=request.user)
    owned_by = book.objects.filter(owner=request.user)
    profile = request.user.profile
    if request.method == 'POST':
        admin_form = AdminForm(request.POST , instance=profile)
        if admin_form.is_valid():
            is_admin = admin_form.cleaned_data['is_admin']
            if is_admin :
                profile.user.is_staff = True
                profile.user.is_admin = True
                profile.user.is_superuser= True
                profile.user.save()
            else:
                profile.user.is_superuser= False
                profile.user.is_staff = False
                profile.user.is_admin = False
                profile.user.save()
            admin_form.save()
        return redirect('profile')
    else:
        admin_form = AdminForm(instance=profile)
        return render(request , 'user/profile.html',
         {'profile': profile , 'admin_form': admin_form ,
          'borrowed_books':borrowed_books ,
          'owned_by':owned_by })
@login_required
def u_profile(request , id):
    profile = Profile.objects.get(id=id)
    user= User.objects.get(profile= profile)
    borrowed_books = book.objects.filter(borrowed_by=user)
    owned_by = book.objects.filter(owner=user)
    if request.method == 'POST':
        admin_form = AdminForm(request.POST , instance=profile)
        if admin_form.is_valid():
            is_admin = admin_form.cleaned_data['is_admin']
            if is_admin :
                profile.user.is_staff = True
                profile.user.is_admin = True
                profile.user.is_superuser= True
                profile.user.save()
            else:
                profile.user.is_superuser= False
                profile.user.is_staff = False
                profile.user.is_admin = False
                profile.user.save()
            admin_form.save()
        return redirect('u-profile', id=id)
    else:
        admin_form = AdminForm(instance=profile)
        return render(request , 'user/profile.html',
         {'profile': profile , 'admin_form': admin_form ,
          'borrowed_books':borrowed_books ,
          'owned_by':owned_by })
@login_required
def profile_update(request):

    if request.method == 'POST':
        u_form = UserUpdateForm( request.POST ,instance=request.user)
        p_form = ProfileUpdateForm(request.POST ,  request.FILES , instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            rprofile = p_form.save(commit=False)
            rprofile.user = request.user
            rprofile.save()
        return redirect('profile')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)
        return render(request , 'user/profile_update.html' , {'u_form' : u_form , 'p_form' : p_form})
@user_passes_test(lambda u: u.is_superuser)
def profile_delete(request , id):
    profile = Profile.objects.get(id=id)
    user = User.objects.get(profile=profile)
    if request.method == 'POST':
        user.delete()
        return redirect('all-books')
    else :
        return render(request , 'user/delete_confirm.html' , {'user': user})
@user_passes_test(lambda u: u.is_superuser)
def profiles(request):
    users = User.objects.all().order_by('-is_superuser')
    myfilter = ProfilesFilter(request.GET , queryset=users)
    users = myfilter.qs
    return render(request, 'user/profiles.html' , {'users':users , 'myfilter':myfilter })