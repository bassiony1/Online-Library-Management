from django.urls import path
from . import views as terms_views


urlpatterns = [

    path('terms/', terms_views.allterms, name='terms'),
    path('terms/create/', terms_views.TermCreateView.as_view(),name='term-create'),
    path('terms/<int:pk>/', terms_views.TermDetailView.as_view(), name='term-detail'),
    path('terms/<int:pk>/update', terms_views.TermUpdateView.as_view(), name='term-update'),
    path('terms/<int:pk>/delete', terms_views.TermDeleteView.as_view(), name='term-delete'),

]
