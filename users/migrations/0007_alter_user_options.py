# Generated by Django 5.0.7 on 2024-09-10 19:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0006_create_is_active_group"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="user",
            options={
                "permissions": [
                    ("can_access_admin", "Can access the admin"),
                    ("can_access_all_perms", "Can access all permissions"),
                ]
            },
        ),
    ]
