# Generated by Django 2.1.5 on 2020-03-19 18:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webapp_flatswapp', '0004_rental'),
    ]

    operations = [
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('street', models.TextField()),
                ('city', models.TextField()),
                ('province', models.TextField()),
                ('postcode', models.TextField()),
            ],
        ),
        migrations.RenameModel(
            old_name='Rental',
            new_name='Locations',
        ),
        migrations.AddField(
            model_name='userprofile',
            name='address',
            field=models.TextField(default='default adress'),
        ),
    ]
