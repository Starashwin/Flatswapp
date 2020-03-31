import os
import django
import random

os.environ.setdefault('DJANGO_SETTINGS_MODULE' , 'flatswapp.settings')
django.setup()

from webapp_flatswapp.models import *
#from faker import Faker

'''def create_property(N):
    fake= Faker()
    for i in range(N):
        property_id = i
        views = random.randint(10,100)
        likes = random.randint(10,50)
        name = fake.name()
        slug = "-".join(name.lower().split())
        description = fake.text()
        address = fake.address()
        n_bedroom=random.randint(1,5)
        Property.objects.create(property_id=property_id, views=views, likes=likes, name=name, slug=slug, description=description, address=address,n_bedrooms=n_bedroom)

create_property(10)
print("Successful")'''

def populate():
    properties = [
    {'propert_id':'1','views': 10, 'name': '4 BHK on Argyl Street', 'description': 'This is a fully furnished flat at a very good location', 'address':'Argyl Street, Glasgow', 'n_bedrooms': 4, 'furnished': 'Yes', 'rent': 900},
    {'propert_id':'2','views': 12, 'name': '1 Flatmate required', 'description': 'I am a tenant and there is 1 room empty in my flat. This flat is very good with all facilities and near to the university of glasgow', 'address':'Cooprage place,Glasgow', 'n_bedrooms': 1, 'furnished': 'Yes', 'rent': 750},
    {'propert_id':'3','views': 30, 'name': '1 person can swap with me', 'description': 'I am reloacating to London, I will be leaving next week, About room, Good location, spacious, with gym facilty nearby, ', 'address':'Kelvinhaugh, Glasgow', 'n_bedrooms': 1, 'furnished': 'Yes', 'rent': 500},
    {'propert_id':'4','views': 16, 'name': 'space for 5 tenenats', 'description': 'This flat is not furnished so you can decorate as you wish', 'address':'Argyl Street, Glasgow', 'n_bedrooms': 3, 'furnished': 'No', 'rent': 600},
    {'propert_id':'5','views': 24, 'name': '2 BHK near City center', 'description': 'This is a fully furnished flat at a very good location', 'address':'Argyl Street, Glasgow', 'n_bedrooms': 4, 'furnished': 'Yes', 'rent': 500},
    ]
    
    for prop in properties:
        p = add_property(prop)

def add_property(property.property_id):
    p, created = Property.objects.get_or_create(property_id=property.property_id)
    if not created:
        p.views = views
        p.name = name
        p.description = description
        p.address = address
        p.n_bedrooms = n_bedrooms
        p.furnished = furnished
        p.rent = rent
        p.save()
            
    return p
    
if __name__=='__main__':
    print('Staring Flatswapp population script......')
    populate()