from django.urls import path

from app_main import views

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('product/<int:pk>/', views.ProductDetailsView.as_view(), name='product-details'),
    path('catalog/', views.CatalogView.as_view(), name='catalog'),
    path('contact/', views.ContactView.as_view(), name='contact'),
    path('cart/', views.CartView.as_view(), name='cart'),
    path('subscribe/', views.subscribe, name='subscribe'),
    path('unsubscribe/<uidb64>/', views.unsubscribe, name='unsubscribe'),
    path('api/product/list/', views.product_list_api, name='api-list-product'),
]
