from django import forms
from django.contrib.auth.models import User
from webapp_flatswapp.models import UserProfile
from webapp_flatswapp.models import Address

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    class Meta:
        model = User
        fields = ('username', 'email', 'password',)


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('mobile', 'picture',)

class Search(forms.ModelForm):
    class Meta:
        fields = ('search',)

class Address(forms.ModelForm):
    class Meta:
        model = Address
        fields = ('street', 'city', 'province', 'postcode',)