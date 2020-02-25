from django.shortcuts import render
from django.http import HttpResponse
from django.urls import reverse

# Create your views here.

def index(request):
    return render(request, 'webapp_flatswapp/index.html')

def about(request):
    response = render(request, 'webapp_flatswapp/about.html')
    return response