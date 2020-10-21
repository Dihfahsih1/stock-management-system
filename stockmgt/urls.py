from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('items-list', views.list_items, name='list_items'),
    path('add-item', views.add_item, name='add_item'),
    path('add-item/<str:pk>/', views.update_items, name='update_items'),
]