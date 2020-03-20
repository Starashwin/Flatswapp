from django import forms
from django.contrib.auth.models import User
from webapp_flatswapp.models import UserProfile

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