# Generated by Django 2.1.5 on 2020-03-30 21:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('webapp_flatswapp', '0038_auto_20200330_2227'),
    ]

    operations = [
        migrations.AlterField(
            model_name='shortlist',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='shortlisting', to='webapp_flatswapp.UserProfile'),
        ),
    ]
