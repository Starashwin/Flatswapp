from django.shortcuts import render, redirect
from django.forms import modelformset_factory
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

@login_required
def myaccount(request):
    context_dict = {}
    context_dict['shortlist'] = Shortlist.objects.filter(Q(user=request.user.profile))
    return render(request, 'webapp_flatswapp/myaccount.html',context=context_dict)

    
def about(request):
    response = render(request, 'webapp_flatswapp/about.html')
    return response

def show_property(request, id_slug):

    context_dict = {}
    try:
        property = Property.objects.get(slug=id_slug)
        property.views+=1
        property.save()

        context_dict['property'] = property
        context_dict['images'] = Images.objects.filter(property=property)
        context_dict['shortlisted'] = Shortlist.objects.filter(user=request.user.profile,property=property)
    except property.DoesNotExist:
        context_dict['property'] = None
    except AttributeError:
        context_dict['shortlisted'] = None
    return render(request, 'webapp_flatswapp/property.html', context=context_dict)

@login_required
def add_shortlist(request,id_slug):
    if request.method == 'GET':
        shortlisted = False
        us=UserProfile.objects.get(user=request.user)
        pr=Property.objects.get(slug=id_slug)
        context_dict = {}
        context_dict['property'] = pr
        sl = Shortlist.objects.create(user=us,property=pr)
        sl.save()
        shortlisted = True
        return render(request,'webapp_flatswapp/property.html',context={'property': pr,  'shortlisted': shortlisted})
        
@login_required
def remove_shortlist(request,id_slug):
    if request.method == 'GET':
        shortlisted = True
        us=UserProfile.objects.get(user=request.user)
        pr=Property.objects.get(slug=id_slug)
        context_dict = {}
        context_dict['property'] = pr
        sl = Shortlist.objects.get(user=us,property=pr).delete()
        shortlisted = False
        return render(request,'webapp_flatswapp/property.html',context={'property': pr,  'shortlisted': shortlisted})
        
@login_required
def add_property(request):
    ImageFormSet = modelformset_factory(Images, form=PropertyImageForm, extra=3)
    #formset for uploading multiple images, extra means the number of images that can be uploaded
    propertyForm = PropertyForm()
 
    if request.method == 'POST':
        propertyForm = PropertyForm(request.POST,request.FILES,request.user)
        formset = ImageFormSet(request.POST, request.FILES, queryset=Images.objects.none())
        
        
        # # Have we been provided with a valid form? check for both forms 
        if propertyForm.is_valid() and formset.is_valid():
            property_form=propertyForm.save(commit=False)
            property_form.user=UserProfile.objects.get(user=request.user)
            property_form.save()
            
            for form in formset.cleaned_data:
            #in case user does not upload 10 photos webpage won't crash
                if form:
                    image = form['image']
                    photo = Images(property=property_form, image=image)
                    photo.save()
            return HttpResponseRedirect("/flatswapp/property/"+property_form.slug+"/add_facility/")
            
            # Save the new category to the database.

            # Now that the category is saved, we could confirm this.
            # For now, just redirect the user back to the index view.
        else:
            # The supplied form contained errors -
            # just print them to the terminal.
            print(propertyForm.errors, formset.errors)
            formset = ImageFormSet()
    else:
        propertyForm = PropertyForm()
        formset = ImageFormSet(queryset=Images.objects.none())
    # Will handle the bad form, new form, or no form supplied cases.
    # Render the form with error messages (if any).
    return render(request, 'webapp_flatswapp/add_property.html', {'form': propertyForm, 'formset': formset})

@login_required    
def add_facility(request, id_slug):
    try:
        property = Property.objects.get(slug=id_slug)
    except Property.DoesNotExist:
        property = None
    # You cannot add a page to a Category that does not exist...
    if property is None:
        return redirect('/webapp_flatswapp/')
        
    form = FacilityForm()

    if request.method == 'POST':
        form = FacilityForm(request.POST)

        if form.is_valid():
            if property:
                facility = form.save(commit=False)
                facility.save()
                property.facility=facility
                property.save()
                     
                           
                return redirect(reverse('webapp_flatswapp:show_property',kwargs={'id_slug':id_slug}))
        else:
            print(form.errors)
            
    context_dict = {'form': form, 'property': property}
    return render(request, 'webapp_flatswapp/add_facility.html', context=context_dict)
    
def register(request):
    registered = False
    if request.method == 'POST':
        user_form = UserForm(request.POST)
        profile_form = UserProfileForm(request.POST)
        
        if user_form.is_valid()and profile_form.is_valid(): 
            user = user_form.save()
            user.set_password(user.password)
            user.save()
            profile = UserProfile()
            profile = profile_form.save(commit=False)
            profile.user = user

            if 'picture' in request.FILES:
                profile.picture = request.FILES['picture']
            profile.save()
            registered = True
        else:
            print(user_form.errors, profile_form.errors)
    else:
        user_form = UserForm()
        profile_form = UserProfileForm()
    return render(request, 'webapp_flatswapp/register.html', context = {'user_form': user_form, 'profile_form': profile_form,'registered':registered})

def after_register(request):
    if not(UserProfile.objects.filter(user=request.user).exists()):
        if request.method == 'POST':
            user = request.user
            profile_form = UserProfileForm(request.POST)
            if profile_form.is_valid():
                profile = profile_form.save(commit=False)
                profile.user = user

                if 'picture' in request.FILES:
                    profile.picture = request.FILES['picture']
                    profile.save()
                    registered = True
            else:
                print(profile_form.errors)

        else:
            profile_form = UserProfileForm()

        return render(request, 'webapp_flatswapp/after_register.html', context = {'profile_form': profile_form})
    return render(request,'webapp_flatswapp/myaccount.html')



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
                messages.error(request, 'This account is locked. Please create another account')
                return render(request, 'webapp_flatswapp/login.html')
        else:
            messages.error(request, 'Invalid user or password. Please try again.')
            return render(request, 'webapp_flatswapp/login.html')
    else:
        return render(request, 'webapp_flatswapp/login.html')

@login_required
def user_logout(request):
    logout(request)
    return redirect(reverse('webapp_flatswapp:index'))

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
            return redirect('/flatswapp/myaccount')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'webapp_flatswapp/change_password.html', {'form': form})