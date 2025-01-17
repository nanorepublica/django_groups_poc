# Generated by Django 5.0.7 on 2024-08-02 19:31

from django.db import migrations

def create_groups(apps, schema_editor):
    Group = apps.get_model('auth.Group')
    Group.objects.create(name='is_staff')
    Group.objects.create(name='is_superuser')

def remove_groups(apps, schema_editor):
    Group = apps.get_model('auth.Group')
    Group.objects.all().delete()

class Migration(migrations.Migration):

    dependencies = [
        ("users", "0001_initial"),
    ]

    operations = [migrations.RunPython(create_groups, remove_groups)]
