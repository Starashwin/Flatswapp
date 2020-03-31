''' This file contains test cases for the Flatswapp project, there are various possible test cases, some of them are written below'''
'''There are total of 22 test cases in the file'''

#Imports required to test certain functionality.
import os 
import importlib

from django.test import TestCase, Client
from .models import *
from django.conf import settings
from django.urls import reverse, resolve
from webapp_flatswapp.views import * 

##Header and footer for the failure of test cases, referred fromt the testcases from tango with django
FAILURE_HEADER = f"{os.linesep}{os.linesep}{os.linesep}================{os.linesep}TwD TEST FAILURE =({os.linesep}================{os.linesep}"
FAILURE_FOOTER = f"{os.linesep}"

#Below class is used to test the successful creation of the UserProfile model.
#The basic logic for testing it is to create a test user and check if the test user is properly saved in using the model UserProfile
class UserCreationTest(TestCase):

#Test case for testing the UserProfile Object Creation
    def test_fields(self):
       u = UserProfile() #Creating the UserProfile variable 
       u.user = User.objects.create_user(username='testuser2', password= 'ptestuser2') #Creates and returns user using the User model in Django
       #Providing some made up user data for creating test user
       u.email = "testuser2@testusers.com"
       u.mobile = "+44 8894561260"
       u.address = "Glasgow"
       u.save() #sving the newly created user
       record = UserProfile.objects.get(pk=u.id) #getting the user using the get method and storing it in the record variable 
       self.assertEqual(record, u) # comparing the created user u and the received data using the get method, if it is equal that means the user profile is successfully created.


#Test class for the Property Model
class PropertyTests(TestCase):
    # To test the property model we also need the a user therefore in this class, first a user profile is created and then the property is created
    def test_property(self):
        #Creating the user profile using the UserProfile and User models
        u = UserProfile() 
        u.user = User.objects.create_user(username='testuser1', password= 'ptestuser1')
        u.email = "testuser1@testusers.com"
        u.mobile = "+44 8894561260"
        u.address = "Glasgow"
        u.save()
    
        #Creating a Property object variable and adding some random data to test the successful creation of the poperty object 
        p = Property()
        p.property_id = 1
        p.views = 5
        p.likes = 3
        p.name = "Test Name"
        p.description = "This is a Description for the test case of property model"
        p.address = "1/1, Some Street, Glasgow"
        p.outdata = "2020-04-17"
        p.n_bedroom = 3
        p.furnished = "No"
        p.rent = 1300
        p.user = u
        p.save() # Saving the property object
        record = Property.objects.get(pk=p.property_id)#retrieving using the get method and comparing the created data if both are equal that means our object is succesfully created and model is working completely fine.
        self.assertEqual(record, p)
        
#Test case for testing the the slug for Property object 
#Slug testing can also be done in the previous function but it will be easier to debug if the everything is serperatly tested
#The process is same to create the user, user profile and the property as above.
    def test_slug_on_save(self):
        u = UserProfile()
        u.user = User.objects.create_user(username='testuser2', password= 'ptestuser2')
        u.email = "testuser2@testusers.com"
        u.mobile = "+44 8894561260"
        u.address = "Glasgow"
        u.save()

        p1 = Property()
        p1.property_id = 2
        p1.views = 5
        p1.likes = 3
        p1.name = "Test Name"
        p1.description = "This is a Description for the test case of property model"
        p1.address = "1/1, Some Street, Glasgow"
        p1.outdata = "2020-04-17"
        p1.n_bedroom = 3
        p1.furnished = "No"
        p1.rent = 1300
        p1.user = u
        p1.save()
        self.assertEqual(p1.slug,'test-name-2') #Comparing the created slug and the required slug, if it is same then test successful.

#Below class is used to test the Facility model
class FacilityTest(TestCase):
    def test_facility(self):
        f = Facility() #creating the facility object for variable f
        #Some random test data below
        f.facility = "These are the test facilities"
        f.slug=''
        f.save()# save the object 
        #below two lines are used to get the object using the get method and then compare with the saved object, if equal, then test successful.
        record = Facility.objects.get()
        self.assertEqual(record, f)

#Below class is used to test if all the images are working by checking the successful creation of the media directory.
class ImageTest(TestCase):
    def setUp(self):
        self.project_base_dir = os.getcwd()
        self.media_dir = os.path.join(self.project_base_dir, 'media')

    def test_image_dir(self):
        does_media_dir_exist = os.path.isdir(self.media_dir)
        self.assertTrue(does_media_dir_exist, f"{FAILURE_HEADER}We couldn't find the /media/ directory in the expected location. Make sure it is in your project directory (at the same level as the manage.py module).{FAILURE_FOOTER}")

#Below class is used to test the ShortList model.
#ShortList model requires a user profile and the property. Therefore, userprofile, user and property is created first, then used to create and test the ShortList model.
class ShortListTest(TestCase):
    def test_shortlist(self):
        shortlist = Shortlist() #Creates the ShortList object for the variable shortlist
        
        u = UserProfile()
        u.user = User.objects.create_user(username='testuser2', password= 'ptestuser2')
        u.email = "testuser2@testusers.com"
        u.mobile = "+44 8894561260"
        u.address = "Glasgow"
        u.save()

        p1 = Property()
        p1.property_id = 2
        p1.views = 5
        p1.likes = 3
        p1.name = "Test Name"
        p1.description = "This is a Description for the test case of property model"
        p1.address = "1/1, Some Street, Glasgow"
        p1.outdata = "2020-04-17"
        p1.n_bedroom = 3
        p1.furnished = "No"
        p1.rent = 1300
        p1.user = u
        p1.save()
        
        shortlist.user = u #user is provided to the model
        shortlist.property = p1 # property is provided to the model
        shortlist.save() #saved using the save function
        #below two lines are used to get the object using the get method and then compare with the saved object, if equal, then test successful.
        record = Shortlist.objects.get() 
        self.assertEqual(record, shortlist)

#Below class is used to test the urls and the associated views using reverse and resolve function for the django urls.
#The basic logic is to check if the URL is actually assocaited to the passes view object using the resolve and reverse functions.
class  TestUrls(TestCase):
    
    #This function is used to test the URL for index view
    def test_index_url_is_resolved(self):
        url = reverse('index') #index view object passed to the reverse function
        self.assertEqual(resolve(url).func, index) # checking if the resolved URL actually associated to the provided view.
        
    def test_about_url_is_resolved(self):
        url = reverse('about')
        self.assertEqual(resolve(url).func, about)
        
    def test_register_url_is_resolved(self):
        url = reverse('webapp_flatswapp:register')
        self.assertEqual(resolve(url).func, register)
     
    def test_register1_url_is_resolved(self):
        url = reverse('webapp_flatswapp:register1')
        self.assertEqual(resolve(url).func, after_register)
        
    def test_login_url_is_resolved(self):
        url = reverse('webapp_flatswapp:login')
        self.assertEqual(resolve(url).func, user_login)
        
    def test_logout_url_is_resolved(self):
        url = reverse('webapp_flatswapp:logout')
        self.assertEqual(resolve(url).func, user_logout)
    
    def test_myaccount_url_is_resolved(self):
        url = reverse('webapp_flatswapp:myaccount')
        self.assertEqual(resolve(url).func, myaccount)
     
    def test_change_password_url_is_resolved(self):
        url = reverse('webapp_flatswapp:change_password')
        self.assertEqual(resolve(url).func, change_password)
        
    def test_search_url_is_resolved(self):
        url = reverse('webapp_flatswapp:search')
        self.assertEqual(resolve(url).func, search)
     
    def test_add_property_url_is_resolved(self):
        url = reverse('webapp_flatswapp:add_property')
        self.assertEqual(resolve(url).func, add_property)

#Below class is used to test the view 
class TestViews(TestCase):
    
    def setUp(self):
        self.client = Client()
    
    #This function is used to test the index view, here Client module is used from the django tests to check response for certain type of requests, i.e GET or POST
    def test_index(self):
        response = self.client.get(reverse('index')) #Check and save the response for the reverse for the index view
        self.assertEqual(response.status_code, 200) # if the response is success i.e. 200 it means the view is working fine 
        self.assertTemplateUsed(response, 'webapp_flatswapp/index.html')#Also check the templated used exist or not

    def test_about(self):
        response = self.client.get(reverse('about'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'webapp_flatswapp/about.html')

    def test_register(self):
        response = self.client.get(reverse('webapp_flatswapp:register'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'webapp_flatswapp/register.html')
    
    def test_user_login(self):
        response = self.client.get(reverse('webapp_flatswapp:login'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'webapp_flatswapp/login.html')
        
    def test_search(self):
        response = self.client.get(reverse('webapp_flatswapp:search'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'webapp_flatswapp/search.html')

#Logout test should give 302 error message since the user is not logged and therefore is redireceted and logout page is available to the logged in users only.
    def test_logout(self):
        response = self.client.get(reverse('webapp_flatswapp:logout'))
        self.assertEqual(response.status_code, 302)
