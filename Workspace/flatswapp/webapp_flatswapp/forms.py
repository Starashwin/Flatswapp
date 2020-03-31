from django import forms
from django.contrib.auth.models import User
from webapp_flatswapp.models import *
import requests

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class' : 'list-group-item','placeholder':'Password'}), label='')
    username = forms.CharField(widget=forms.TextInput (attrs={'class' : 'list-group-item','placeholder':'Username'}), label='')
    
    class Meta:
    
        model = User
        fields = ('username', 'password',)
        

class UserProfileForm(forms.ModelForm):
    email = forms.CharField(widget=forms.TextInput (attrs={'class' : 'list-group-item','placeholder':'Email'}), label='')
    mobile = forms.CharField(widget=forms.TextInput(attrs={'class' : 'list-group-item','type':'tel','placeholder':'Phone number (eg. +44123456789)'}), label='')
    postcode= forms.CharField(widget=forms.TextInput (attrs={'class' : 'list-group-item', 'id':'customInput','placeholder':'Post Code','onchange':"javascript:document.getElementById('dummyButton').click();"}), label='')
    address= forms.CharField(widget=forms.TextInput (attrs={'class' : 'list-group-item','id':'output_field','placeholder':'Address'}), label='')

    class Meta:     
        model = UserProfile
        fields = ('email','mobile', 'picture','postcode','address',)

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
    feature = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple,choices=OPTIONS)
    slug = forms.CharField(widget=forms.HiddenInput(), required=False)

    class Meta:     
        model = Facility
        fields = ('feature', )

    
class PropertyForm(forms.ModelForm):
    views = forms.IntegerField(widget=forms.HiddenInput(), initial=0)
    likes = forms.IntegerField(widget=forms.HiddenInput(), initial=0)
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
    
    name=forms.CharField(widget=forms.TextInput(attrs={'class' : 'list-group-item','placeholder':'Ad Title'}), label='')
    postcode=forms.CharField(widget=forms.TextInput(attrs={'class' : 'list-group-item','id':'customInput','placeholder':'Postcode','onchange':"javascript:getAPI();document.getElementById('dummyButton').click();"}), label='')
    address=forms.CharField(widget=forms.TextInput (attrs={'class' : 'list-group-item','id':'output_field','placeholder':'Address'}), label='')
    n_bedrooms=forms.ChoiceField(widget=forms.Select(attrs={'class' : 'list-group-item','placeholder':'Number of Bedrooms'}),choices=BEDROOMS_OPTIONS, label='')
    furnished=forms.ChoiceField(widget=forms.Select(attrs={'class' : 'list-group-item','placeholder':'Is it furnished?'}),choices=FURNISHED_OPTIONS, label='')
    rent=forms.IntegerField(widget=forms.TextInput(attrs={'class' : 'list-group-item','placeholder':'Rent Amount'}), label='')
    cover = forms.ImageField(label='Cover Picture')
    outdata = forms.DateField(widget=forms.DateInput(attrs={'class' : 'list-group-item input-sm','id':'datepicker','style':'height:50px;','placeholder':'Moving Out Date'}), label='')
    description = forms.CharField(widget=forms.Textarea(attrs={'class' : 'list-group-item','style' : 'height:100px','placeholder':'Description'}), label='')
    
    outward=forms.CharField(widget=forms.HiddenInput(), initial='', required=False)
    nearest=forms.CharField(widget=forms.HiddenInput(), initial='', required=False)
    neighbour=forms.CharField(widget=forms.HiddenInput(), initial='', required=False)

    class Meta:
    # Provide an association between the ModelForm and a model
        model = Property

        fields = ['name','n_bedrooms','furnished','postcode','address','outdata','rent','description','cover','outward','nearest','neighbour','slug']
        
class PropertyImageForm(forms.ModelForm):
    image = forms.ImageField(widget=forms.FileInput(attrs={'onchange':"javascript:updateImage();readURL(this);"}), label='')
    class Meta:
        model = Images
        fields = ('image', )