from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.login, name='login'),
    path('home/', views.home, name='home'),
    path('users/', views.users, name='users'),
    path('users/editUser/<int:id>', views.editUser, name='editUser'),
    path('users/removeUser/<int:id>', views.removeUser, name='removeUser'),
    path('users/addUser/', views.addUser, name='addUser'),
]
