
from django.contrib.auth.models import AbstractBaseUser, UserManager, Group, Permission, _user_get_permissions, _user_has_perm, _user_has_module_perms
from django.db import models
from django.forms.fields import CharField
from django.utils.translation import gettext_lazy as _
from collections.abc import Iterable

class MyUserManager(UserManager):

    def _create_user(self, username, email, password, **extra_fields):
        is_superuser = extra_fields.pop('is_superuser')
        is_staff = extra_fields.pop('is_staff')
        user = super()._create_user(username, email, password, **extra_fields)

        if is_superuser:
            is_superuser_group = Group.objects.get(name='is_superuser')
            is_superuser_group.user_set.add(user)
        if is_staff:
            is_staff_group = Group.objects.get(name='is_staff')
            is_staff_group.user_set.add(user)
        return user

class User(AbstractBaseUser):
    email = models.EmailField(unique=True)
    username= models.CharField(max_length=34)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    groups = models.ManyToManyField(
        Group,
        verbose_name=_("groups"),
        blank=True,
        help_text=_(
            "The groups this user belongs to. A user will get all permissions "
            "granted to each of their groups."
        ),
        related_name="user_set",
        related_query_name="user",
    )
    user_permissions = models.ManyToManyField(
        Permission,
        verbose_name=_("user permissions"),
        blank=True,
        help_text=_("Specific permissions for this user."),
        related_name="user_set",
        related_query_name="user",
    )

    objects = MyUserManager()

    @property
    def is_staff(self):
        return self.groups.filter(name='is_staff').exists()

    @property
    def is_superuser(self):
        return self.groups.filter(name='is_superuser').exists()

    @property
    def is_active(self):
        return self.groups.filter(name='Active Users').exists()

    def get_user_permissions(self, obj=None):
        """
        Return a list of permission strings that this user has directly.
        Query all available auth backends. If an object is passed in,
        return only permissions matching this object.
        """
        return _user_get_permissions(self, obj, "user")

    def get_group_permissions(self, obj=None):
        """
        Return a list of permission strings that this user has through their
        groups. Query all available auth backends. If an object is passed in,
        return only permissions matching this object.
        """
        return _user_get_permissions(self, obj, "group")

    def get_all_permissions(self, obj=None):
        return _user_get_permissions(self, obj, "all")

    def has_perm(self, perm, obj=None):
        """
        Return True if the user has the specified permission. Query all
        available auth backends, but return immediately if any backend returns
        True. Thus, a user who has permission from a single auth backend is
        assumed to have permission in general. If an object is provided, check
        permissions for that object.
        """
        # Active superusers have all permissions.
        if self.is_active and self.is_superuser:
            return True

        # Otherwise we need to check the backends.
        return _user_has_perm(self, perm, obj)

    def has_perms(self, perm_list, obj=None):
        """
        Return True if the user has each of the specified permissions. If
        object is passed, check if the user has all required perms for it.
        """
        if not isinstance(perm_list, Iterable) or isinstance(perm_list, str):
            raise ValueError("perm_list must be an iterable of permissions.")
        return all(self.has_perm(perm, obj) for perm in perm_list)

    def has_module_perms(self, app_label):
        """
        Return True if the user has any permissions in the given app label.
        Use similar logic as has_perm(), above.
        """
        # Active superusers have all permissions.
        if self.is_active and self.is_superuser:
            return True

        return _user_has_module_perms(self, app_label)


class NormalModel(models.Model):

    name = models.CharField(max_length=56)
    created = models.DateTimeField(auto_now_add=True)
