# Generated by Django 2.1.5 on 2020-03-29 11:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webapp_flatswapp', '0032_auto_20200328_2202'),
    ]

    operations = [
        migrations.AlterField(
            model_name='images',
            name='image',
            field=models.ImageField(upload_to='property_images/', verbose_name='Image'),
        ),
    ]
