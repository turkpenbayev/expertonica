from decimal import Decimal
import random
import string
import datetime
import os

from django.db import models
from django.db.models import Q
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.core.validators import MinValueValidator
from django.dispatch import receiver


def upload_path(instance, filename):
    return os.path.join(str(instance.__class__.__name__).lower() + '/', filename)


def number_generator(size=6, chars=string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


class MyUserManager(BaseUserManager):
    def _create_user(self, username, password, **extra_fields):
        if not username:
            raise ValueError('The username must be set')
        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_user(self, username, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(username, password, **extra_fields)

    def create_superuser(self, username, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        return self._create_user(username, password, **extra_fields)


class User(AbstractUser):
    """
    An abstract base class implementing a fully featured User model with
    admin-compliant permissions.

    Username and password are required. Other fields are optional.
    """

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []
    objects = MyUserManager()

    def full_name(self,):
        """
        Return the first_name plus the last_name, with a space in between.
        """
        return self.first_name + ' ' + self.last_name

    def __str__(self,):
        return f"{self.username} - {self.first_name} {self.last_name}"


class Session(models.Model):
    """
        Session class
        Saves info about session file name, counts number of sites in file
    """
    PENDING, STARTED, SUCCESS, FAILURE = range(4)
    TYPE_CHOICES = (
        (PENDING, 'PENDING'),
        (STARTED, 'STARTED'),
        (SUCCESS, 'SUCCESS'),
        (FAILURE, 'FAILURE')
    )

    sites_file = models.FileField(upload_to='sites', null=True, blank=True)
    sites_counter = models.PositiveIntegerField(default=0)
    status = models.PositiveSmallIntegerField(
        choices=TYPE_CHOICES, default=STARTED)
    start_date = models.DateTimeField(null=True, blank=True)
    end_date = models.DateTimeField(null=True, blank=True)

    def filename(self):
        """
        Return the filename.
        """
        return os.path.basename(self.sites_file.name)

    def __str__(self,):
        return f"{self.sites_file.name}"


class SiteInfo(models.Model):
    session = models.ForeignKey(
        Session, on_delete=models.CASCADE, related_name='sites')
    name = models.CharField(max_length=128, null=True, blank=True)
    status = models.CharField(max_length=3, null=True, blank=True)
    check_time = models.DateTimeField(null=True, blank=True)
    ip = models.CharField(max_length=32, null=True, blank=True)
    is_checked = models.BooleanField(default=False)
    responce_time = models.CharField(max_length=128, null=True, blank=True)

    def __str__(self,):
        return f" {self.name} {self.status}"
