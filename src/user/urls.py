from django.urls import path ,include
from django.conf import settings
from django.conf.urls.static import static
from . import views as user_views

urlpatterns = [
    path('profile/<int:id>' , user_views.profile , name='profile'),
    path('profileupdate/', user_views.profile_update,name='profile-update'),
]
