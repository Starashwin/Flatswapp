# Generated by Django 2.1.5 on 2020-03-27 22:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('webapp_flatswapp', '0025_auto_20200327_1850'),
    ]

    operations = [
        migrations.RenameField(
            model_name='shortlist',
            old_name='username',
            new_name='user',
        ),
    ]
