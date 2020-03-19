from django.urls import path
from django.conf import settings
from django.urls import include

from webapp_flatswapp import views

app_name = 'webapp_flatswapp'

urlpatterns = [

    path('', views.index, name='index'),
    path('about/', views.about, name='about'),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('search/', views.search, name = 'search'),
]