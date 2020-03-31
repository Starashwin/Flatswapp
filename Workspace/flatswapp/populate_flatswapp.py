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

def populate_user():
    user = User.objects.create('username'='testUser1','password'='ptestuser1')
    #Starting with the userprofile

def populate():
    properties = [
    {'property_id': 1,'views': 10, 'likes': 6, 'name': '4 BHK on Argyl Street', 'description': 'This is a fully furnished flat at a very good location', 'address':'Argyl Street, Glasgow', 'outdata': '31/03/2020', 'n_bedrooms': 4, 'furnished': 'yes', 'rent': 900},
    {'property_id': 2,'views': 12, 'likes': 10, 'name': '1 Flatmate required', 'description': 'I am a tenant and there is 1 room empty in my flat. This flat is very good with all facilities and near to the university of glasgow', 'address':'Cooprage place,Glasgow', 'outdata': '31/03/2020', 'n_bedrooms': 1, 'furnished': 'yes', 'rent': 750},
    {'property_id': 3,'views': 30, 'likes': 27, 'name': '1 person can swap with me', 'description': 'I am reloacating to London, I will be leaving next week, About room, Good location, spacious, with gym facilty nearby, ', 'address':'Kelvinhaugh, Glasgow', 'outdata': '31/03/2020', 'n_bedrooms': 1, 'furnished': 'yes', 'rent': 500},
    {'property_id': 4,'views': 16, 'likes': 0, 'name': 'space for 5 tenenats', 'description': 'This flat is not furnished so you can decorate as you wish', 'address':'Argyl Street, Glasgow', 'outdata': '31/03/2020',  'n_bedrooms': 3, 'furnished': 'no', 'rent': 600},
    {'property_id': 5,'views': 24, 'likes': 20, 'name': '2 BHK near City center', 'description': 'This is a fully furnished flat at a very good location', 'address':'Argyl Street, Glasgow', 'outdata': '31/03/2020', 'n_bedrooms': 4, 'furnished': 'yes', 'rent': 500},
    ]
    
    for index, p in properties[0].items():
        prop = add_property(p['property_id'], p['views'], p['likes'], p['name'], p['description'], p['address'], p['n_bedrooms'], p['furnished'], p['rent'])


def add_property(property_id, name, views=0, likes=0, description='', address='', n_bedrooms=0, furnished='', rent=0):
    p = Property.objects.get_or_create()
    p.views = views
    p.likes = likes
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
    