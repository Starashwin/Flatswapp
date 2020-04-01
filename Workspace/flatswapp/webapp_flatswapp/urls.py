#This file contains the URLs for the Flatswapp,webapp_flatswapp 

from django.urls import path
from django.conf import settings
from django.urls import include


from webapp_flatswapp import views 

app_name = 'webapp_flatswapp'

#All these URLs are extension after "/flatswapp/" in URL
urlpatterns = [

    path('', views.index, name='index'),
    path('about/', views.about, name='about'),
    path('register/', views.register, name='register'),
    path('register1/', views.after_register, name='register1'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('myaccount/', views.myaccount, name = 'myaccount'),
    path('property/<slug:id_slug>/add_shortlist/', views.add_shortlist, name = 'add_shortlist'),
    path('property/<slug:id_slug>/remove_shortlist/', views.remove_shortlist, name = 'remove_shortlist'),
    path('change_password/',views.change_password, name='change_password'),
    path('search/', views.search, name='search'),
    
    path('property/<slug:id_slug>/add_facility/',views.add_facility, name='add_facility'),
    path('property/<slug:id_slug>/',views.show_property, name='show_property'),
    path('add_property/', views.add_property, name = 'add_property'),
]