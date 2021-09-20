from django.urls import path
from . import views as test_views


urlpatterns = [

    path('testimonails/', test_views.testimonail_list, name='testimonials'),
    path('testimonails/<int:id>/', test_views.testimonial_detail, name='testimonials-detail'),
    path('testimonails/create/', test_views.TestimonialCreateView.as_view(),name='testimonials-create'),
    path('testimonails/<int:pk>/update', test_views.TestimonialUpdateView.as_view(), name='testimonials-update'),
    path('testimonails/<int:pk>/delete', test_views.TestimonialDeleteView.as_view(), name='testimonials-delete'),

]
