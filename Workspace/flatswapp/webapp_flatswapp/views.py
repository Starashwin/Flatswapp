from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.urls import reverse
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.db.models import Q
from django.http import *
from .models import *
from webapp_flatswapp.forms import *
from .filters import PropertyFilter
import requests

# Create your views here.

def index(request):
    return render(request, 'webapp_flatswapp/index.html')

def myaccount(request):
    return render(request, 'webapp_flatswapp/myaccount.html')
    
def about(request):
    response = render(request, 'webapp_flatswapp/about.html')
    return response

def show_category(request, category_name_slug):

    context_dict = {}
    try:
        category = Category.objects.get(slug=category_name_slug)
        pages = Page.objects.filter(category=category)
        context_dict['pages'] = pages
        context_dict['category'] = category
    except Category.DoesNotExist:
        context_dict['category'] = None
        context_dict['pages'] = None
    return render(request, 'webapp_flatswapp/category.html', context=context_dict)

@login_required
# def add_property(request):
    # if request.method == 'POST':
        # form = PropertyForm(request.POST, request.FILES)

        # if form.is_valid():
            # #form.save()
            # form.save(commit=False)
            # for field in request.FILES.keys():
                # for formfile in request.FILES.getlist(field):
                    # img = Property(picture = formfile)
                    # img.save()
            # form.save()
            # return redirect('/flatswapp/success')
    # else:
        # form = PropertyForm()
    # return render(request, 'webapp_flatswapp/add_property.html', {'form' : form})

def success(request):
    return HttpResponse('Property added successfully')

@login_required
def display_property_view(request):
    if request.method == 'GET':
        prop = Property.objects.all()
        return render(request, 'webapp_flatswapp/show_property.html', {'home_images' : prop})

@login_required
def add_property(request):
    form = PropertyForm()
    if request.method == 'POST':
        form = PropertyForm(request.POST,request.FILES)
        # # Have we been provided with a valid form?
        if form.is_valid():
            print(form['postcode'].value())
            url = 'http://api.postcodes.io/postcodes/%s'%(form['postcode'].value())
            data = requests.get(url).json()
            print(data['status'])
            if data['status']==200:
                print("Working2")
                data=data['result']
                print(data['longitude'])
                form.longitude = data['longitude']
                form.latitude = data['latitude']
            # if 'picture' in request.FILES:
                # form.picture = request.FILES['picture']
            form.save(commit=True)
            # Save the new category to the database.

            # Now that the category is saved, we could confirm this.
            # For now, just redirect the user back to the index view.
            return redirect('/flatswapp/')
        else:
            # The supplied form contained errors -
            # just print them to the terminal.
            print(form.errors)
    # Will handle the bad form, new form, or no form supplied cases.
    # Render the form with error messages (if any).
    return render(request, 'webapp_flatswapp/add_property.html', {'form': form})

@login_required    
def add_page(request, category_name_slug):
    try:
        category = Category.objects.get(slug=category_name_slug)
    except Category.DoesNotExist:
        category = None
    # You cannot add a page to a Category that does not exist...
    if category is None:
        return redirect('/webapp_flatswapp/')
        
    form = PageForm()

    if request.method == 'POST':
        form = PageForm(request.POST)

        if form.is_valid():
            if category:
                page = form.save(commit=False)
                page.category = category
                page.views = 0
                page.save()
                
                return redirect(reverse('webapp_flatswapp:show_category',kwargs={'category_name_slug':category_name_slug}))
        else:
            print(form.errors)
            
    context_dict = {'form': form, 'category': category}
    return render(request, 'webapp_flatswapp/add_page.html', context=context_dict)
    
def register(request):
    registered = False
    if request.method == 'POST':
        user_form = UserForm(request.POST)
        profile_form = UserProfileForm(request.POST)
        #address_form = AddressForm(request.POST)
        
        if user_form.is_valid() and profile_form.is_valid(): #and Api.is_postcode_valid(self, address_form.postcode):
            user = user_form.save()
            user.set_password(user.password)
            user.save()
            profile = profile_form.save(commit=False)
            profile.user = user
            #address = address_form.save(commit=False)
            #profile.address = adress

            if 'picture' in request.FILES:
                profile.picture = request.FILES['picture']
            profile.save()
            registered = True
        else:
            print(user_form.errors, profile_form.errors)
    else:
        user_form = UserForm()
        profile_form = UserProfileForm()
    return render(request, 'webapp_flatswapp/register.html', context = {'user_form': user_form,  'profile_form': profile_form, 'registered': registered})

def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(request, user)
                return redirect(reverse('webapp_flatswapp:myaccount'))
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

# def search(request):
    # if request.method== 'POST':
        # search_string = request.POST['search_string']
        # if search_string:
            # match = Property.objects.filter(Q(name__icontains=search_string))
            # if match:
                # return render(request, 'webapp_flatswapp/search.html', {'sr':match})
        # else:
            # return redirect(reverse('webapp_flatswapp:search'))
    # return render(request, 'webapp_flatswapp/search.html')

def search(request):
    property_list = Property.objects.all()
    property_filter = PropertyFilter(request.GET, queryset=property_list)
    return render(request, 'webapp_flatswapp/search.html', {'filter': property_filter})
