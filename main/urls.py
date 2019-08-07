from django.contrib import admin
from django.views.generic import TemplateView
from django.urls import path, include
from main import views



urlpatterns = [
    path('product/<uuid:uuid_url>/', views.ProductDetailView.as_view(), name='product'),
    path('products/<slug:tag>/', views.ProductListView.as_view(), name='products'),
    path('', TemplateView.as_view(template_name="main/home.html"), name='home'),
]