from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('home/<int:id>', views.home, name='home'),
    path('login/', views.login, name='login'),
]
