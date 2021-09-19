from django.urls import path 
from django.conf import settings
from . import views as blog_views


urlpatterns = [
    path('blog/', blog_views.post_list,name='blog-home') ,
    path('blog/<int:pk>/', blog_views.PostDetailView.as_view() , name= 'post-detail'),
    path('blog/create/', blog_views.PostCreateView.as_view() , name='post-create'),
    path('blog/<int:pk>/update/', blog_views.PostUpdateView.as_view() , name='post-update'),
    path('blog/<int:pk>/delete/', blog_views.PostDeleteView.as_view() , name='post-delete'),
]