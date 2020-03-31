import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE' , 'flatswapp.settings')
django.setup()

from webapp_flatswapp.models import *

