# Generated by Django 5.0.7 on 2024-08-02 21:15

import users.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0003_user_groups_user_user_permissions"),
    ]

    operations = [
        migrations.AlterModelManagers(
            name="user",
            managers=[
                ("objects", users.models.MyUserManager()),
            ],
        ),
        migrations.AddField(
            model_name="user",
            name="username",
            field=models.CharField(default="me", max_length=34),
            preserve_default=False,
        ),
    ]