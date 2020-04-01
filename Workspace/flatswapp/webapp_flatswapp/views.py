#This file contains the views for Flatswapp Project.

#All the required imports to create views.
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

#This function creates view for the index/home page and renders index.html when the URL to this view is requested.
def index(request):
    prop_slider=Property.objects.order_by('-views')[:3] #is used to display properties by the number of views in decreasing order using a slider view.
    context_dict = {}
    context_dict['properties'] = prop_slider 
    return render(request, 'webapp_flatswapp/index.html',context=context_dict)

#This function creates the view to my account page and requires the user to be logged in.
@login_required
def myaccount(request):
    context_dict = {}
    context_dict['shortlist'] = Shortlist.objects.filter(Q(user=request.user.profile))
    return render(request, 'webapp_flatswapp/myaccount.html',context=context_dict) #Renders myaccount.html when URL associated to this view is requested.

#This function renders about.html when the URL assoscaited to this view is requested.
def about(request):
    response = render(request, 'webapp_flatswapp/about.html')
    return response

#This function is creates a view to show property and since all the property is created using slug therefore it also takes slug id as argument.
def show_property(request, id_slug):

    context_dict = {}
    try:
        property = Property.objects.get(slug=id_slug)
        property.views+=1 #increments the number of views when someone requests the view of a particular property using slug
        property.save()

        context_dict['property'] = property #Create the view to display the details of the requested property.
        context_dict['images'] = Images.objects.filter(property=property) #display the property images for the requested property.
        context_dict['shortlisted'] = Shortlist.objects.filter(user=request.user.profile,property=property) #Create the view to display the shortlist status of the property for the user.
    except property.DoesNotExist: # if there is Does not exist exception set the context for the property to none.
        context_dict['property'] = None
    except AttributeError:
        context_dict['shortlisted'] = None
    return render(request, 'webapp_flatswapp/property.html', context=context_dict) #render view, using property.html 

#This function is used to create the view to add the property to the shortlist.
#User must be logged in to access this view.
@login_required
def add_shortlist(request,id_slug):
    if request.method == 'GET': #Check if the request method is GET or POST
        shortlisted = False #initially set shortlist variable to False
        us=UserProfile.objects.get(user=request.user) #Request the user data
        pr=Property.objects.get(slug=id_slug) #Get the slug id to the property
        context_dict = {}
        context_dict['property'] = pr
        sl = Shortlist.objects.create(user=us,property=pr) #if user short lists it save the shortlist
        sl.save()
        shortlisted = True #Set the shortlisted variable to True.
        return render(request,'webapp_flatswapp/property.html',context={'property': pr,  'shortlisted': shortlisted}) #render the property.html with the updated shortlist view

#This function is used to remove the short listed property for the list of a user.
#User must be logged in to aces this view.
@login_required
def remove_shortlist(request,id_slug):#Requires slug id 
    if request.method == 'GET': 
        shortlisted = True
        us=UserProfile.objects.get(user=request.user) #Retrieves the user information.
        pr=Property.objects.get(slug=id_slug) #Retrieves the property detail from the slug.
        context_dict = {}
        context_dict['property'] = pr
        sl = Shortlist.objects.get(user=us,property=pr).delete()#delete the propety from the shortlist
        shortlisted = False #Set the variable to false
        return render(request,'webapp_flatswapp/property.html',context={'property': pr,  'shortlisted': shortlisted}) #Render the updated property.html

#This function is used to create the view to add property.
#User must be authenticated to access this view.
@login_required
def add_property(request):
    ImageFormSet = modelformset_factory(Images, form=PropertyImageForm, extra=3) #Uses modelformset to deal with the multiple images upload.
    #formset for uploading multiple images, extra means the number of images that can be uploaded
    propertyForm = PropertyForm() 
 
    if request.method == 'POST': #Check the request method
        #if the request method is POST use Property form and Image formset to create view for the 2 forms.
        propertyForm = PropertyForm(request.POST,request.FILES,request.user)
        formset = ImageFormSet(request.POST, request.FILES, queryset=Images.objects.none())
        
        
        # # Have we been provided with a valid form? check for both forms
        #If yes then save them
        if propertyForm.is_valid() and formset.is_valid():
            property_form=propertyForm.save(commit=False)
            property_form.user=UserProfile.objects.get(user=request.user)
            property_form.save()
            
            for form in formset.cleaned_data: #to loop around for multiple images upload
            #in case user does not upload 3 photos webpage won't crash
                if form:
                    image = form['image']
                    photo = Images(property=property_form, image=image)
                    photo.save() #save
            return HttpResponseRedirect("/flatswapp/property/"+property_form.slug+"/add_facility/") #redirect to add_facility view using slug.
            
        else:
            # If the supplied form contained errors -
            # just print them to the terminal.
            print(propertyForm.errors, formset.errors)
            formset = ImageFormSet() #reset the formset to avoid errors
    else:
        propertyForm = PropertyForm()
        formset = ImageFormSet(queryset=Images.objects.none())
    # Will handle the bad form, new form, or no form supplied cases.
    # Render the form with error messages (if any).
    return render(request, 'webapp_flatswapp/add_property.html', {'form': propertyForm, 'formset': formset})


#This function is used to create the view for the add_facility feature.
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

        if form.is_valid(): #Check if the provided form is valid
            if property:
                facility = form.save(commit=False)
                facility.save()
                property.facility=facility
                property.save()
                #Save it to database
                return redirect(reverse('webapp_flatswapp:show_property',kwargs={'id_slug':id_slug})) #If property added successfully refirect to the page to the newly added property using slug.
        else:
        #If supplied form is invalid print errors.
            print(form.errors)
            
    context_dict = {'form': form, 'property': property}
    return render(request, 'webapp_flatswapp/add_facility.html', context=context_dict)#render facility.html page

#This function is used to create a view for the user to register to Flatswapp.
def register(request):
    registered = False
    if request.method == 'POST':
        user_form = UserForm(request.POST) #Create user form and profile form using the POST requset
        profile_form = UserProfileForm(request.POST)
        
        if user_form.is_valid()and profile_form.is_valid(): #Check if the provided forms are valid.
            user = user_form.save() 
            user.set_password(user.password)
            user.save()#Save user to database
            profile = UserProfile()
            profile = profile_form.save(commit=False)
            profile.user = user

            if 'picture' in request.FILES:
                profile.picture = request.FILES['picture'] #ask for profile pictures
            profile.save() #Save profile to data base
            registered = True
        else:
            print(user_form.errors, profile_form.errors)
    else:
        user_form = UserForm()
        profile_form = UserProfileForm()
    return render(request, 'webapp_flatswapp/register.html', context = {'user_form': user_form, 'profile_form': profile_form,'registered':registered})

#This fuction is used to create  view to the create userprofile for the users which re logged in through social accounts.
def after_register(request):
    if not(UserProfile.objects.filter(user=request.user).exists()): #check if the user profile exist or not, if not then proceed with the profile creation.
        if request.method == 'POST':
            user = request.user
            profile_form = UserProfileForm(request.POST) #Create user profile form 
            if profile_form.is_valid():
                profile = profile_form.save(commit=False)
                profile.user = user

                if 'picture' in request.FILES:
                    profile.picture = request.FILES['picture']
                    profile.save()
                    registered = True
            else:
                print(profile_form.errors) #If invalid form print errors

        else:
            profile_form = UserProfileForm()

        return render(request, 'webapp_flatswapp/after_register.html', context = {'profile_form': profile_form})
    return render(request,'webapp_flatswapp/myaccount.html') #render myaccount.html after successful creation of profile.

#This function is used to create the view for the user to login into Flatswapp with an existing account.
def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username') #Request for user's username and password
        password = request.POST.get('password')
        user = authenticate(username=username, password=password) #Authenticate with the supplied user details
        if user: #If user is successfully autheticated
            if user.is_active: #if user is active, login and render the myaccount.html page
                login(request, user)
                return redirect(reverse('webapp_flatswapp:myaccount'))
            else:   #if user is inactive, display the error message and render the login.html page
                messages.error(request, 'This account is locked. Please create another account')
                return render(request, 'webapp_flatswapp/login.html')
        else:
            messages.error(request, 'Invalid user or password. Please try again.') #if user failed to autheticate display the error message and render login page.
            return render(request, 'webapp_flatswapp/login.html')
    else:
        return render(request, 'webapp_flatswapp/login.html') #if the request is not POST render login page.

#This function is used to create the view for the user to logout. User must be logged in to access this view.
@login_required
def user_logout(request):
    logout(request)
    return redirect(reverse('webapp_flatswapp:index')) #if requested redirect to index page.

#This function is used to create a view to search 
def search(request):
    property_initial = PropertyFilter(request.GET, queryset=Property.objects.none())
    if request.method== 'POST':
        property_list = Property.objects.all() #get all the properties in the list
        property_filter = PropertyFilter(request.POST, queryset=property_list) # Search for the entered query and render the page according to the search query result.
        return render(request, 'webapp_flatswapp/search.html', {'filter': property_filter})
    return render(request, 'webapp_flatswapp/search.html', {'filter': property_initial})

#This function is used to create the view for the user to change the password. User must be logged in to access this view.
@login_required    
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST) #If requested display the password change form.
        if form.is_valid(): #Check the validity of the form.
            user = form.save()
            update_session_auth_hash(request, user)  #A very important step, update the hash for the session.
            messages.success(request, 'Your password was successfully updated!') #Display the success message.
            return redirect('/flatswapp/myaccount') #redirect to the myaccount page
        else:
            messages.error(request, 'Please correct the error below.') #Otherwise display the error message.
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'webapp_flatswapp/change_password.html', {'form': form})#IF the request is not POST render the change_password html again.