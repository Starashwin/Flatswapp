# Generated by Django 2.1.5 on 2020-03-28 23:37

from django.db import migrations, models
import webapp_flatswapp.models


class Migration(migrations.Migration):

    dependencies = [
        ('webapp_flatswapp', '0032_auto_20200328_2202'),
    ]

    operations = [
        migrations.AlterField(
            model_name='images',
            name='image',
            field=models.ImageField(upload_to=webapp_flatswapp.models.get_image_filename, verbose_name='Image'),
        ),
    ]
