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
    path('myaccount/', views.myaccount, name = 'myaccount'),
    
    #path('category/<slug:category_name_slug>/add_page/',views.add_page, name='add_page'),
    path('category/<slug:category_name_slug>/',views.show_category, name='show_category'),
    #path('add_category/', views.add_category, name='add_category'),
    path('add_property/', views.add_property_view, name = 'add_property'),
    path('success/', views.success, name = 'success'),
    path('property_images/', views.display_property_view, name = 'property_images'),
]