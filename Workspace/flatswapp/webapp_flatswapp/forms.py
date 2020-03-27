from django import forms
from django.contrib.auth.models import User
from webapp_flatswapp.models import *
import requests

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class' : 'list-group-item','placeholder':'Password'}), label='')
    username = forms.CharField(widget=forms.TextInput (attrs={'class' : 'list-group-item','placeholder':'Username'}), label='')
    email = forms.CharField(widget=forms.TextInput (attrs={'class' : 'list-group-item','placeholder':'Email'}), label='')
    class Meta:
    
        model = User
        fields = ('username', 'email', 'password',)
        
#<input type="tel" name="mobile" value="+154889" maxlength="128" required="" id="id_mobile">
#<input type="tel" name="mobile" value="+15416" class="list-group-item" placeholder="Phone number" required="" id="id_mobile">
class UserProfileForm(forms.ModelForm):
    mobile = forms.CharField(widget=forms.TextInput(attrs={'class' : 'list-group-item','type':'tel','placeholder':'Phone number (eg. +44123456789)'}), label='')
    postcode= forms.CharField(widget=forms.TextInput (attrs={'class' : 'list-group-item', 'id':'customInput','placeholder':'Post Code','onchange':"javascript:document.getElementById('dummyButton').click();"}), label='')
    address= forms.CharField(widget=forms.TextInput (attrs={'class' : 'list-group-item','id':'output_field','placeholder':'Address'}), label='')

    class Meta:     
        model = UserProfile
        fields = ('mobile', 'picture','postcode','address',)

# class Search(forms.ModelForm):
    # class Meta:
        # fields = ('search',)
        
#class CategoryForm(forms.ModelForm):
#    views = forms.IntegerField(widget=forms.HiddenInput(), initial=0)
#    likes = forms.IntegerField(widget=forms.HiddenInput(), initial=0)
#    slug = forms.CharField(widget=forms.HiddenInput(), required=False)
#    name=forms.CharField(widget=forms.TextInput(attrs={'class' : 'list-group-item','placeholder':'Post Title'}), label='')
#    address=forms.CharField(widget=forms.TextInput(attrs={'class' : 'list-group-item','placeholder':'Address'}), label='')
#    n_bedrooms=forms.IntegerField(widget=forms.TextInput(attrs={'class' : 'list-group-item','placeholder':'Number of Bedrooms'}), label='')
#    furnished=forms.CharField(widget=forms.TextInput(attrs={'class' : 'list-group-item','placeholder':'Is it furnished?'}), label='')
#    rent=forms.IntegerField(widget=forms.TextInput(attrs={'class' : 'list-group-item','placeholder':'Rent Amount'}), label='')

    # An inline class to provide additional information on the form.
#    class Meta:
    # Provide an association between the ModelForm and a model
#        model = Category
#        fields = ['name','address','n_bedrooms','furnished','picture','rent',]

class PageForm(forms.ModelForm):
    title = forms.CharField(max_length=128,help_text="Please enter the title of the page.")
    url = forms.URLField(max_length=200,help_text="Please enter the URL of the page.")
    views = forms.IntegerField(widget=forms.HiddenInput(), initial=0)

    class Meta:
    # Provide an association between the ModelForm and a model
        model = Page
    # What fields do we want to include in our form?
    # This way we don't need every field in the model present.
    # Some fields may allow NULL values; we may not want to include them.
    # Here, we are hiding the foreign key.
    # we can either exclude the category field from the form,
        exclude = ('category',)
    # or specify the fields to include (don't include the category field).
    #fields = ('title', 'url', 'views')
    def clean(self):
        cleaned_data = self.cleaned_data
        url = cleaned_data.get('url')
        
        # If url is not empty and doesn't start with 'http://',
        # then prepend 'http://'.
        if url and not url.startswith('http://'):
            url = f'http://{url}'
            cleaned_data['url'] = url
            
        return cleaned_data    
    
class PropertyForm(forms.ModelForm):
    views = forms.IntegerField(widget=forms.HiddenInput(), initial=0)
    likes = forms.IntegerField(widget=forms.HiddenInput(), initial=0)
    slug = forms.CharField(widget=forms.HiddenInput(), required=False)

    name=forms.CharField(widget=forms.TextInput(attrs={'class' : 'list-group-item','placeholder':'Post Title'}), label='')
    postcode=forms.CharField(widget=forms.TextInput(attrs={'class' : 'list-group-item','placeholder':'Postcode','onchange':"javascript:loadDoc();"}), label='')
    n_bedrooms=forms.IntegerField(widget=forms.TextInput(attrs={'class' : 'list-group-item','placeholder':'Number of Bedrooms'}), label='')
    furnished=forms.CharField(widget=forms.TextInput(attrs={'class' : 'list-group-item','placeholder':'Is it furnished?'}), label='')
    rent=forms.IntegerField(widget=forms.TextInput(attrs={'class' : 'list-group-item','placeholder':'Rent Amount'}), label='')
    cover = forms.ImageField()
    outdata = forms.DateField(widget=forms.DateInput(attrs={'class' : 'list-group-item input-sm','id':'datepicker','style':'height:50px;','placeholder':'Moving Out Date'}), label='')
    description = forms.CharField(widget=forms.Textarea(attrs={'class' : 'list-group-item','style' : 'height:100px','placeholder':'Description'}), label='')
    
    #id="datepicker" class="form-control" data-type="datepicker" data-guid="02d4517a-7236-bb43-2b2c-1dea160fd41c" data-datepicker="true"
    
    longitude=forms.FloatField(widget=forms.HiddenInput(), initial=0)
    latitude=forms.FloatField(widget=forms.HiddenInput(), initial=0)
    # # print(form['postcode'].value())
    # url = 'http://api.postcodes.io/postcodes/%s'%(postcode)
    # data = requests.get(url).json()
    # print(data)
    # if data['status']==200:
        # print("Working2")
        # data=data['result']
        # longitude = data['longitude']
        # latitude = data['latitude']
    #picture = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True}))
    # An inline class to provide additional information on the form.
    class Meta:
    # Provide an association between the ModelForm and a model
        model = Property
        fields = ['name','postcode','n_bedrooms','furnished','outdata','rent','longitude','latitude','cover','description']