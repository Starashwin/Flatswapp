from django.db import models
from django.contrib.auth.models import User
from phonenumber_field.modelfields import PhoneNumberField #https://github.com/stefanfoulis/django-phonenumber-field
from django_google_maps import fields as map_fields #for Google Maps
import postcodes_io_api
# Create your models here.
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    mobile = PhoneNumberField()
    picture = models.ImageField(upload_to='profile_images', blank=True)
    address = models.TextField(default='default adress')

    def __str__(self):
        return self.user.username

class Locations(models.Model):
    address = map_fields.AddressField(max_length=200)
    geolocation = map_fields.GeoLocationField(max_length=100)

class Address(models.Model):
    api  = postcodes_io_api.Api(debug_http=True)
    street=models.TextField()
    city=models.TextField()
    province=models.TextField()
    postcode=models.TextField()