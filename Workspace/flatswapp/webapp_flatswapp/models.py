from django.db import models
from django.contrib.auth.models import User
from phonenumber_field.modelfields import PhoneNumberField #https://github.com/stefanfoulis/django-phonenumber-field
from django_google_maps import fields as map_fields #for Google Maps
from django.template.defaultfilters import slugify
# import postcodes_io_api
# Create your models here.
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    mobile = PhoneNumberField()
    picture = models.ImageField(upload_to='profile_images', blank=True)
    #postcode= models.TextField(null=True) 
    address= models.TextField(default='') 


    def __str__(self):
        return self.user.username

class Locations(models.Model):
    address = map_fields.AddressField(max_length=200)
    geolocation = map_fields.GeoLocationField(max_length=100)

#class Address(models.Model):
    #api  = postcodes_io_api.Api(debug_http=True)
    

    
class Category(models.Model):
    id = models.AutoField(primary_key=True)
    views = models.IntegerField(default=0)
    likes = models.IntegerField(default=0)
    slug = models.SlugField(unique=True)
    name=models.TextField()
    address=models.TextField(default='')
    n_bedrooms=models.IntegerField(default=0)
    furnished=models.TextField(default='')
    rent=models.IntegerField(default=0)
    picture=models.ImageField(upload_to='home_images', blank=True)
    
    
    def save(self, *args, **kwargs):
        self.slug = slugify(self.id)
        super(Category, self).save(*args, **kwargs)

    class Meta:
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.id
        
class Page(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    title = models.CharField(max_length=128)
    url = models.URLField()
    views = models.IntegerField(default=0)
    def __str__(self):
        return self.title