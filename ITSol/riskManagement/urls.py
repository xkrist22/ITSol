from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.login, name='login'),
    path('home/<str:msg>', views.home, name='home'),
    path('users/', views.users, name='users'),
    path('users/editUser/<int:id>', views.editUser, name='editUser'),
    path('users/editUser/saveEditUser/<int:id>', views.saveEditUser, name='saveEditUser'),
    path('users/addUser/', views.addUser, name='addUser'),
    path('users/addUser/saveNewUser/', views.saveNewUser, name='saveNewUser'),
    path('users/removeUser/<int:id>', views.removeUser, name='removeUser'),
]