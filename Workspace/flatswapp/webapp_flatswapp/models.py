from django.db import models
from django.contrib.auth.models import User
from phonenumber_field.modelfields import PhoneNumberField #https://github.com/stefanfoulis/django-phonenumber-field

# Create your models here.
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    mobile = PhoneNumberField()
    picture = models.ImageField(upload_to='profile_images', blank=True)

    def __str__(self):
        return self.user.username