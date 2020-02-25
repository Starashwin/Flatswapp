from django.urls import path
from webapp_flatswapp import views

app_name = 'webapp_flatswapp'

urlpatterns = [
    path('', views.index, name='index'),
    path('about/', views.about, name='about'),
]