from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
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
    prop_slider=Property.objects.order_by('-views')[:3]
    context_dict = {}
    context_dict['properties'] = prop_slider
    return render(request, 'webapp_flatswapp/index.html',context=context_dict)

def myaccount(request):
    context_dict = {}
    context_dict['shortlist'] = Shortlist.objects.filter(user=request.user)
    return render(request, 'webapp_flatswapp/myaccount.html',context=context_dict)
    
def about(request):
    response = render(request, 'webapp_flatswapp/about.html')
    return response

# def shortlist(request)
    # return render(request, 'webapp_flatswapp/shortlist.html')

def show_property(request, id_slug):

    context_dict = {}
    try:
        property = Property.objects.get(slug=id_slug)
        property.views+=1
        property.save()
        #pages = Page.objects.filter(property=property)
        #context_dict['pages'] = pages
        context_dict['property'] = property
    except property.DoesNotExist:
        context_dict['property'] = None
        #context_dict['pages'] = None
    return render(request, 'webapp_flatswapp/property.html', context=context_dict)

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
def add_shortlist(request,id_slug):
    if request.method == 'GET':
        shortlisted = False
        us=User.objects.get(username=request.user.username)
        pr=Property.objects.get(slug=id_slug)
        context_dict = {}
        context_dict['property'] = pr
        sl = Shortlist.objects.create(user=us,property_id=pr)
        sl.save()
        # shortlisting=User.objects.get(username=request.user.username),shortlisted=Property.objects.get(slug=id_slug))
        shortlisted = True
        return render(request,'webapp_flatswapp/property.html',context={'property': pr,  'shortlisted': shortlisted})
        
@login_required
def add_property(request):
    form = PropertyForm()
    if request.method == 'POST':
        form = PropertyForm(request.POST,request.FILES,request.user)
        # print(request.user)
        
        
        # # Have we been provided with a valid form?
        if form.is_valid():
            fs=form.save(commit=False)
            fs.user=User.objects.get(username=request.user.username)
            fs.save()
            
            # form.user=request.user
            
            # print(form['postcode'].value())
            # url = 'http://api.postcodes.io/postcodes/%s'%(form['postcode'].value())
            # data = requests.get(url).json()
            # print(data['status'])
            # if data['status']==200:
                # print("Working2")
                # data=data['result']
                # print(data['longitude'])
                # form.cleaned_data['longitude'] = data['longitude']
                # form.cleaned_data['latitude'] = data['latitude']
            
            # if 'picture' in request.FILES:
                # form.picture = request.FILES['picture']
            
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
    property_initial = PropertyFilter(request.GET, queryset=Property.objects.none())
    if request.method== 'POST':
        property_list = Property.objects.all()
        property_filter = PropertyFilter(request.POST, queryset=property_list)
        return render(request, 'webapp_flatswapp/search.html', {'filter': property_filter})
    return render(request, 'webapp_flatswapp/search.html', {'filter': property_initial})

@login_required    
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Your password was successfully updated!')
            return redirect('/flatswapp/change_password')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'webapp_flatswapp/change_password.html', {'form': form})