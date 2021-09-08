from django.contrib.auth.models import User
from user.forms import AdminForm, ProfileUpdateForm, UserUpdateForm , UserCreationForm , UserRegisterForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import render , redirect , reverse
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
from .models import Profile


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
        return render(request , 'user/profile.html', {'profile': profile , 'admin_form': admin_form})
@login_required
def u_profile(request , id):
    profile = Profile.objects.get(id=id)
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
        return render(request , 'user/profile.html', {'profile': profile , 'admin_form': admin_form})
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