from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('home/<str:hash>', views.home, name='home'),
    path('login/', views.login, name='login'),
    path('users/<str:hash>', views.users, name='users'),
    path('users/editUser/<int:id>&<str:hash>', views.editUser, name='editUser'),
    path('users/removeUser/<int:id>&<str:hash>', views.removeUser, name='removeUser'),
    path('users/addUser/<str:hash>', views.addUser, name='addUser'),
]
