import os
import django
import random

os.environ.setdefault('DJANGO_SETTINGS_MODULE' , 'flatswapp.settings')
django.setup()

from webapp_flatswapp.models import *
def populate():

    users_out = [
    {'username':'alig', 'email': 'ali@g.com', 'mobile':'+12345678910','address':'Argyle Street, Glasgow'},
    ]
   
    users_in = [
    {'username':'tudorov', 'email': 'tudorov@vk.com', 'mobile':'+4412345789','address':'Buchanan Street, Glasgow'},
    {'username':'ash', 'email': 'ash@pokemon.com', 'mobile':'+12103456789','address':'Sauchihall Street, Glasgow'},
    ]
    
    properties = [
    {'propert_id':'34','views': 10, 'name': '4 BHK on Argyl Street', 'description': 'This is a fully furnished flat at a very good location', 'address':'Argyl Street, Glasgow', 'n_bedrooms': 4, 'furnished': 'Yes', 'rent': 900},
    {'propert_id':'35','views': 12, 'name': '1 Flatmate required', 'description': 'I am a tenant and there is 1 room empty in my flat. This flat is very good with all facilities and near to the university of glasgow', 'address':'Cooprage place,Glasgow', 'n_bedrooms': 1, 'furnished': 'Yes', 'rent': 750},
    {'propert_id':'36','views': 30, 'name': '1 person can swap with me', 'description': 'I am reloacating to London, I will be leaving next week, About room, Good location, spacious, with gym facilty nearby, ', 'address':'Kelvinhaugh, Glasgow', 'n_bedrooms': 1, 'furnished': 'Yes', 'rent': 500},
    {'propert_id':'37','views': 16, 'name': 'space for 5 tenenats', 'description': 'This flat is not furnished so you can decorate as you wish', 'address':'Argyl Street, Glasgow', 'n_bedrooms': 3, 'furnished': 'No', 'rent': 600},
    {'propert_id':'38','views': 24, 'name': '2 BHK near City center', 'description': 'This is a fully furnished flat at a very good location', 'address':'Argyl Street, Glasgow', 'n_bedrooms': 4, 'furnished': 'Yes', 'rent': 500},
    ]
    
    for user in users_out:
        u = add_user(user)
        for prop in properties:   
            p = add_property(prop,u)
            
    for user in users_in:
        u = add_user(user)
        


def add_property(property,user):
    p, created = Property.objects.get_or_create(
    property_id=property['propert_id'],views=property['views'],name = property['name'],description = property['description'],
    address = property['address'],n_bedrooms = property['n_bedrooms'],furnished = property['furnished'],rent = property['rent'],user = user)
    p.save()
            
    return p
    
def add_user(user):
    u, created = User.objects.get_or_create(username=user['username'],password='')
    u.set_password('password')
    u.save()
    up, innerCreated = UserProfile.objects.get_or_create(user=u,mobile=user['mobile'],email=user['email'],address=user['address'])
    up.save()
    return up
    
if __name__=='__main__':
    print('Staring Flatswapp population script......')
    populate()