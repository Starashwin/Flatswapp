#This is the model for the Flatswapp project

#Required imports for creating models
from django.db import models
from django.contrib.auth.models import User
from phonenumber_field.modelfields import PhoneNumberField #https://github.com/stefanfoulis/django-phonenumber-field
from django.template.defaultfilters import slugify

#Below model extends from model.Models and is used to create a UserProfile using the User model of django auth model.
class UserProfile(models.Model):
    #user is a one to one field is created using the User model, when deleted it is cascaded
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile',null=True)
    email=models.EmailField(null=False,default='') #Email Id for the user using the Email field.
    mobile = PhoneNumberField() #Phone number field to store the mobile number of the user created using the PhoneNumberField model, github link to it is in the import section.
    picture = models.ImageField(upload_to='profile_images', blank=True) # an Image field which is used to save the profile picture of a user.
    address= models.TextField(default='') #Text field to store the address of the user.


    def __str__(self):
        return self.user.username # return the username using the User model.

#This model is used to create and store the facilities of a property.
class Facility(models.Model):    
    feature = models.CharField(max_length=400) #features are stored using the char field with max length 400. 
    slug = models.SlugField() #Creates a slug field to stor the slug
    
    def __str__(self):
        return self.feature
        
#This model is used to create the property and extends model.Models
class Property(models.Model):

    property_id = models.AutoField(primary_key=True) #Every property is assigned an Id which is a primary key in the database and thus is unique to each property.
    views = models.IntegerField(default=0) #This variable is used as counter and is later on used to list the most viewed properties
    likes = models.IntegerField(default=0) #This is used to store is someone likes a property, but will be used in the next version to enhance features on the website.
    slug = models.SlugField(unique=True) # This variable is used to create the slug field for unique urls for each property.
    name=models.TextField() #name or title for the property using a text field.
    description=models.TextField(default='')#Field to describe the property.
    address=models.TextField(default='')#Address of the property.
    outdata=models.DateField(null=True)#Date field to get the date of the avilability of the property.
    n_bedrooms=models.IntegerField(default=0)
    furnished=models.TextField(default='')
    rent=models.IntegerField(default=0)
    cover=models.ImageField(upload_to='home_images/', blank=True)#A cover photo for the property.
    outward=models.TextField(default='')
    nearest=models.TextField(default='')
    neighbour=models.TextField(default='')
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE,null=True)#property can only be created by an autheticated user therefore a User field in the database, it is a foreign key.
    facility = models.ForeignKey(Facility, on_delete=models.CASCADE,null=True)# A foreign key to the Facility model for stating the available facilities of a property.
    
    def save(self, *args, **kwargs):#save function to save the property using a slug for unique porperty specific URL
        super(Property, self).save(*args, **kwargs)
        if not self.slug:
            self.slug = slugify(self.name) + "-" + str(self.property_id)
            self.save()

    class Meta:
        verbose_name_plural = 'Properties' # Plural verbose name

    def __str__(self):
        return str(self.property_id)

#This model is used to upload multiple images of a property.
class Images(models.Model):
    property = models.ForeignKey(Property, on_delete=models.CASCADE, default=None) #Since pictures will be defined for a particular property therefore using a foreign key to Property model
    image = models.ImageField(upload_to='property_images/', verbose_name='Image')# Image can be uploaded using the Image Field.


#This model is used to shortlist property for an authenticated user. So that user can easily access that property in their shortlist.
class Shortlist(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='shortlisting') #Short list is unique to each user there a foreign key referrring to the UserProfile model.
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='shortlisted') #A particular property will be shortlisted therefore a foreign key to Property model.
    
    class Meta:
        unique_together = ('user', 'property',) #This thing will be unique together
    
    def __str__(self):
        return self.user
    
    def save(self, *args, **kwargs):
        super(Shortlist, self).save(*args, **kwargs) #Save the shortlist.
    
