#This file contains the forms for the Flatswapp Project.

#Required imports for creating the forms.
from django import forms
from django.contrib.auth.models import User
from webapp_flatswapp.models import *
import requests

#This form contains two char fields which is used to get the username and password from the user who wants to login.
class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class' : 'list-group-item','placeholder':'Password'}), label='')
    username = forms.CharField(widget=forms.TextInput (attrs={'class' : 'list-group-item','placeholder':'Username'}), label='')

    class Meta:

        model = User # Uses User model of Django
        fields = ('username', 'password',)#Has 2 fields


#This class is used to create the form for User profile to get the attributes including email, mobile, postcode and address
class UserProfileForm(forms.ModelForm):
    email = forms.CharField(widget=forms.TextInput (attrs={'class' : 'list-group-item','placeholder':'Email'}), label='')
    mobile = forms.CharField(widget=forms.TextInput(attrs={'class' : 'list-group-item','type':'tel','placeholder':'Phone number (eg. +44123456789)'}), label='')
    postcode= forms.CharField(widget=forms.TextInput (attrs={'class' : 'list-group-item', 'id':'customInput','placeholder':'Post Code','onchange':"javascript:document.getElementById('dummyButton').click();"}), label='')
    address= forms.CharField(widget=forms.TextInput (attrs={'class' : 'list-group-item','id':'output_field','placeholder':'Address'}), label='')

    class Meta:     
        model = UserProfile #uses UserProfile model of webapp_flatswapp
        fields = ('email','mobile', 'picture','postcode','address',)

#This class is used to create a form for the user to add facilites to the property and is used while creating the property.
class FacilityForm(forms.ModelForm):
    OPTIONS = (
        ("Electric Heating", "Electric Heating"),
        ("Gas Heating", "Gas Heating"),
        ("Private Parking","Private Parking"),
        ("Dishwasher","Dishwasher"),
        ("Dryer","Dryer"),
        ("Washing Machine","Washing Machine"),
        ("Elevator","Elevator"),
        ("Garden","Garden"),
        )
        #All the above options are displayed as multiple choice fields which a user can choose.
    feature = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple,choices=OPTIONS)
    slug = forms.CharField(widget=forms.HiddenInput(), required=False)

    class Meta:     
        model = Facility #Uses the Facility model of webapp_flatswapp
        fields = ('feature', )


#This class is used as a form to create a property. Extends from ModelForm
class PropertyForm(forms.ModelForm):
    #views and likes are used intially set to 0 and is hidden, user won't be able to predefined them.
    views = forms.IntegerField(widget=forms.HiddenInput(), initial=0) 
    likes = forms.IntegerField(widget=forms.HiddenInput(), initial=0)
    #slug and user are also hidden and can not be seen by user
    slug = forms.CharField(widget=forms.HiddenInput(), required=False)
    user = forms.CharField(widget=forms.HiddenInput(), required=False)
        
    FURNISHED_OPTIONS = (
    ("Furnished","Furnished"),
    ("Yes", "Yes"),
    ("Partially", "Partially"),
    ("No", "No")
    )
    
    BEDROOMS_OPTIONS = (
    (0, '0 bedroom'),
    (1, '1 bedroom'),
    (2, '2 bedrooms'),
    (3, '3 bedrooms'),
    (4, '4 bedrooms'),
    (5, '5 bedrooms'),
    (999, 'More than 5 bedrooms')
    )
    
    #name, postcode and address is taken as input from the user and stored using CharField.
    name=forms.CharField(widget=forms.TextInput(attrs={'class' : 'list-group-item','placeholder':'Ad Title'}), label='')
    postcode=forms.CharField(widget=forms.TextInput(attrs={'class' : 'list-group-item','id':'customInput','placeholder':'Postcode','onchange':"javascript:getAPI();document.getElementById('dummyButton').click();"}), label='')
    address=forms.CharField(widget=forms.TextInput (attrs={'class' : 'list-group-item','id':'output_field','placeholder':'Address'}), label='')
    #n_bedrooms and furnished are displayed as multiple choice option for the user to select.
    n_bedrooms=forms.ChoiceField(widget=forms.Select(attrs={'class' : 'list-group-item','placeholder':'Number of Bedrooms'}),choices=BEDROOMS_OPTIONS, label='')
    furnished=forms.ChoiceField(widget=forms.Select(attrs={'class' : 'list-group-item','placeholder':'Is it furnished?'}),choices=FURNISHED_OPTIONS, label='')
    #Desired rent is also taken as input from the user who is creating the property.
    rent=forms.IntegerField(widget=forms.TextInput(attrs={'class' : 'list-group-item','placeholder':'Rent Amount'}), label='')
    #cover uses ImageField which enables user to upload a cover photo for the property.
    cover = forms.ImageField(label='Cover Picture')
    #Date is taken as input using the date field from user to get ht availability date for the property.
    outdata = forms.DateField(widget=forms.DateInput(attrs={'class' : 'list-group-item input-sm','id':'datepicker','style':'height:50px;','placeholder':'Moving Out Date'}), label='')
    #description is the character fields which can be used by the user to add more details about the property.
    description = forms.CharField(widget=forms.Textarea(attrs={'class' : 'list-group-item','style' : 'height:100px','placeholder':'Description'}), label='')
    
    outward=forms.CharField(widget=forms.HiddenInput(), initial='', required=False)
    nearest=forms.CharField(widget=forms.HiddenInput(), initial='', required=False)
    neighbour=forms.CharField(widget=forms.HiddenInput(), initial='', required=False)

    class Meta:
    # Provide an association between the ModelForm and a model using the Property model
        model = Property 

        fields = ['name','n_bedrooms','furnished','postcode','address','outdata','rent','description','cover','outward','nearest','neighbour','slug']

#This form is used to get images for the property from the user using the File field.
class PropertyImageForm(forms.ModelForm):
    image = forms.ImageField(widget=forms.FileInput(attrs={'onchange':"javascript:updateImage();readURL(this);"}), label='')
    class Meta:
        model = Images #uses Images model
        fields = ('image', )