from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('delete-task/<str:pk>', views.delete_task, name='delete-task'),
    path('edit-task/<str:pk>', views.edit_task, name='edit-task'),
    path('login/', views.loginPage, name='login'),
    path('logout/', views.logoutUser , name='logout'),
    path('signup/', views.signup , name='signup'),
    path('toggle-task/<str:id>', views.toggle_task , name='toggle-task'),
]

