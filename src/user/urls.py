from django.contrib.auth.forms import PasswordChangeForm
from django.http import request
from django.urls import path ,include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import logout as auth_logout
from django.urls import reverse_lazy
from . import views as user_views
from django.contrib.auth import logout, views as auth_views


urlpatterns = [
    path('register/' , user_views.userRegisterForm , name='register'),
    path('login/',auth_views.LoginView.as_view(template_name='user/login.html' ,redirect_authenticated_user = True),name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='user/logout.html'), name='logout'),
    path('profile/<int:id>' , user_views.u_profile , name='u-profile'),
    path('profile/' , user_views.profile , name='profile'),
    path('profile/passwordchange/done',auth_views.PasswordChangeDoneView.as_view(template_name='user/password_change_done.html'),name='password-change-done'),
    path('profile/passwordchange/',auth_views.PasswordChangeView.as_view(template_name='user/password_change.html',success_url = reverse_lazy('password-change-done')),name='password-change'),
    path('profileupdate/', user_views.profile_update,name='profile-update'),
]
