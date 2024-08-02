from django.contrib import admin
from django.contrib.admin.sites import ModelAdmin

from .models import User, NormalModel

class UserAdmin(ModelAdmin):
    list_display = ('pk','email', 'is_staff', 'is_superuser')
    filter_horizontal = ('groups', 'user_permissions')

admin.site.register(User, UserAdmin)


class NormalModelAdmin(ModelAdmin):
    list_display = ('name', 'created')

admin.site.register(NormalModel, NormalModelAdmin)
