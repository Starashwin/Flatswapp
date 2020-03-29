# Generated by Django 2.1.5 on 2020-03-28 20:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('webapp_flatswapp', '0029_auto_20200328_0117'),
    ]

    operations = [
        migrations.CreateModel(
            name='PropertyImages',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='property_images')),
                ('prop', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='images', to='webapp_flatswapp.Property')),
            ],
        ),
    ]