from django import forms
from django.contrib.auth.models import User
from webapp_flatswapp.models import UserProfile, Page, Category
from webapp_flatswapp.models import Address

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class' : 'list-group-item','placeholder':'Password'}), label='')
    username = forms.CharField(widget=forms.TextInput (attrs={'class' : 'list-group-item','placeholder':'Username'}), label='')
    email = forms.CharField(widget=forms.TextInput (attrs={'class' : 'list-group-item','placeholder':'Email'}), label='')
    class Meta:
    
        model = User
        fields = ('username', 'email', 'password',)
        


class UserProfileForm(forms.ModelForm):
    mobile = forms.CharField(widget=forms.TextInput(attrs={'class' : 'list-group-item','placeholder':'Phone number'}), label='')
    
    class Meta:     
        model = UserProfile
        fields = ('mobile', 'picture',)

class Search(forms.ModelForm):
    class Meta:
        fields = ('search',)

class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = ('postcode','address',)
        
class CategoryForm(forms.ModelForm):
    name = forms.CharField(max_length=128,help_text="Please enter the category name.")
    views = forms.IntegerField(widget=forms.HiddenInput(), initial=0)
    likes = forms.IntegerField(widget=forms.HiddenInput(), initial=0)
    slug = forms.CharField(widget=forms.HiddenInput(), required=False)

    # An inline class to provide additional information on the form.
    class Meta:
    # Provide an association between the ModelForm and a model
        model = Category
        fields = ('name',)

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
        