from django.urls import path

from app_main import views

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
]
