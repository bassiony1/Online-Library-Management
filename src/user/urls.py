from django.urls import path ,include
from django.conf import settings
from django.conf.urls.static import static
from . import views as user_views
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('register/' , user_views.userRegisterForm , name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='user/login.html'),name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='user/logout.html'), name='logout'),
    path('profile/<int:id>' , user_views.profile , name='profile'),
    path('profileupdate/', user_views.profile_update,name='profile-update'),
]
