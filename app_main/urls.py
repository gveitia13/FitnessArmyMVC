from django.urls import path

from app_main import views

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('product/<int:pk>/', views.ProductDetailsView.as_view(), name='product-details'),
    path('catalog/', views.CatalogView.as_view(), name='catalog'),
]
