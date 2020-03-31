from django.db import models
from django.contrib.auth.models import User
from phonenumber_field.modelfields import PhoneNumberField #https://github.com/stefanfoulis/django-phonenumber-field
from django_google_maps import fields as map_fields #for Google Maps
from django.template.defaultfilters import slugify
# import postcodes_io_api
# Create your models here.
from django.db.models.signals import post_save

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    email=models.EmailField(null=False,default='')
    mobile = PhoneNumberField()
    picture = models.ImageField(upload_to='profile_images', blank=True)
    #postcode= models.TextField(null=True) 
    address= models.TextField(default='') 
    #shortlisted = models.ManyToManyField(Property, related_name='shortlisted_by')
    def __str__(self):
        return self.user.username


def create_user_profile(sender, instance, created, **kwargs):
  if created:
   UserProfile.objects.create(user=instance)
post_save.connect(create_user_profile, sender=User, dispatch_uid='create_extension')

class Facility(models.Model):
    
    title = models.CharField(max_length=128)
    desciption=models.TextField()
    slug = models.SlugField()
    
    def __str__(self):
        return self.title
        
class Property(models.Model):

    property_id = models.AutoField(primary_key=True)
    views = models.IntegerField(default=0)
    likes = models.IntegerField(default=0)
    slug = models.SlugField(unique=True)
    name=models.TextField()
    description=models.TextField(default='')
    postcode=models.TextField(default='')
    outdata=models.DateField(null=True)
    n_bedrooms=models.IntegerField(default=0)
    furnished=models.TextField(default='')
    rent=models.IntegerField(default=0)
    cover=models.ImageField(upload_to='home_images/', blank=True)
    outward=models.TextField(default='')
    nearest=models.TextField(default='')
    neighbour=models.TextField(default='')
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE,null=True)
    facility = models.ManyToManyField(Facility)
    
    def save(self, *args, **kwargs):
        super(Property, self).save(*args, **kwargs)
        if not self.slug:
            self.slug = slugify(self.name) + "-" + str(self.property_id)
            self.save()

    class Meta:
        verbose_name_plural = 'Properties'

    def __str__(self):
        return str(self.property_id)

#def get_image_filename(instance, filename):
#    title = instance.property.title
#    slug = slugify(title)
#    return "post_images/%s-%s" % (slug, filename)
        
class Images(models.Model):
    property = models.ForeignKey(Property, on_delete=models.CASCADE, default=None)
    image = models.ImageField(upload_to='property_images/', verbose_name='Image')


# class Locations(models.Model):
    # address = map_fields.AddressField(max_length=200)
    # geolocation = map_fields.GeoLocationField(max_length=100)

    
#class Category(models.Model):
#    property_id = models.AutoField(primary_key=True)
#    views = models.IntegerField(default=0)
#    likes = models.IntegerField(default=0)
#    slug = models.SlugField(unique=True)
#    name=models.TextField()
#    address=models.TextField(default='')
#    n_bedrooms=models.IntegerField(default=0)
#    furnished=models.TextField(default='')
#    rent=models.IntegerField(default=0)
#    picture=models.ImageField(upload_to='home_images/', blank=True)

    

        
# class User_Property(models.Model):
    # property = models.ForeignKey(Property, on_delete=models.CASCADE)
    # username = models.ForeignKey(User, on_delete=models.CASCADE)

class Shortlist(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='shortlisting')
    property_id = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='shortlisted')
    
    # class Meta:
        # unique_together = ('user', 'property_id',)
    
    def __str__(self):
        return self.user
    
    def save(self, *args, **kwargs):
    #check if value exists / increment something etc

    #continue with save, if necessary:
        super(Shortlist, self).save(*args, **kwargs)
