from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.urls import reverse
from django.shortcuts import redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.db.models import Q
from .models import *
import postcodes_io_api 

from webapp_flatswapp.forms import UserForm, UserProfileForm

# Create your views here.

def index(request):
    return render(request, 'webapp_flatswapp/index.html')

def about(request):
    response = render(request, 'webapp_flatswapp/about.html')
    return response

def register(request):
    registered = False
    if request.method == 'POST':
        user_form = UserForm(request.POST)
        profile_form = UserProfileForm(request.POST)
        address_form = Address(request.POST)
        
        if user_form.is_valid() and profile_form.is_valid() and Api.is_postcode_valid(self, address_form.postcode):
            user = user_form.save()
            user.set_password(user.password)
            user.save()
            profile = profile_form.save(commit=False)
            profile.user = user
            address = address_form.save(commit=False)

            if 'picture' in request.FILES:
                profile.picture = request.FILES['picture']
            profile.save()
            registered = True
        else:
            print(user_form.errors, profile_form.errors)
    else:
        user_form = UserForm()
        profile_form = UserProfileForm()
        adrress_form = Address()
    return render(request, 'webapp_flatswapp/register.html', context = {'user_form': user_form, 'profile_form': profile_form, 'registered': registered})

def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(request, user)
                return redirect(reverse('webapp_flatswapp:index'))
            else:
                return HttpResponse("Your Flatswapp account is disabled.")
        else:
            print("Invalid login details: {username}, {password}")
            return HttpResponse("Invalid login details supplied.")
    else:
        return render(request, 'webapp_flatswapp/login.html')

@login_required
def user_logout(request):
    logout(request)
    return redirect(reverse('webapp_flatswapp:index'))

def search(request):
    if request.method== 'POST':
        srch = request.POST['search_string']
        if srch:
            match = UserProfile.objects.filter(Q(mobile__icontains=srch) | Q(location_icontains=srch))
            if match:
                return render(request, 'webapp_flatswapp/search.html', {'sr':match})
            else:
                messages.error(request, 'no result found')
        else:
            return HttpResponseRedirect('/search/')
    return render(request, 'webapp_flatswapp/search.html')
