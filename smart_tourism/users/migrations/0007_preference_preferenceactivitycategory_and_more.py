# Generated by Django 5.1.7 on 2025-04-07 18:10

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tourism', '0012_delete_hotelequipment'),
        ('users', '0006_alter_searchhistory_table'),
    ]

    operations = [
        migrations.CreateModel(
            name='Preference',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('budget', models.DecimalField(decimal_places=2, max_digits=10)),
                ('accommodation', models.CharField(choices=[('hôtel', 'Hôtel'), ("maison d'hôte", "Maison d'hôte")], max_length=255)),
                ('stars', models.PositiveIntegerField()),
                ('departure_date', models.DateField()),
                ('arrival_date', models.DateField()),
                ('forks', models.IntegerField()),
                ('arrival_city', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='arrival_preferences', to='tourism.destination')),
                ('departure_city', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='departure_preferences', to='tourism.destination')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='PreferenceActivityCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('activity_category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tourism.activitycategory')),
                ('preference', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='activities', to='users.preference')),
            ],
            options={
                'unique_together': {('preference', 'activity_category')},
            },
        ),
        migrations.CreateModel(
            name='PreferenceCuisine',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cuisine', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tourism.cuisine')),
                ('preference', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cuisines', to='users.preference')),
            ],
            options={
                'unique_together': {('preference', 'cuisine')},
            },
        ),
    ]
