from django.urls import path, include
from api import views



urlpatterns = [
    path('favorite/product/create/', views.FavoriteProductCreateAjaxView.as_view(), name='api-favorite-product-create'),
    path('favorite/product/delete/', views.FavoriteProductDeleteAjaxView.as_view(), name='api-favorite-product-delete'),
    path('favorite/user/create/', views.FavoriteUserCreateAjaxView.as_view(), name='api-favorite-user-create'),
    path('favorite/user/delete/', views.FavoriteUserDeleteAjaxView.as_view(), name='api-favorite-user-delete'),
]