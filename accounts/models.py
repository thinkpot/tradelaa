from django.db import models
from .managers import CustomUserManager
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from django.core.validators import RegexValidator


class UserType(models.Model):
    type = models.CharField(max_length=20, blank=True, null=True)

    def __str__(self):
        return self.type


class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=255, null=True, blank=True)
    last_name = models.CharField(max_length=255, null=True, blank=True)
    phoneNumberRegex = RegexValidator(regex=r"^\+?1?\d{8,15}$")
    phone_number = models.CharField(validators=[phoneNumberRegex], max_length=16, unique=True, null=True, blank=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)
    user_type = models.ForeignKey(UserType, on_delete=models.DO_NOTHING, blank=True, null=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email


class OwnBrokers(models.Model):
    title = models.CharField(max_length=255, null=True, blank=True)
    short_title = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return str(self.title)


class OwnBrokersCredentials(models.Model):
    broker = models.ForeignKey(OwnBrokers, on_delete=models.DO_NOTHING, null=True, blank=True)
    api_key = models.CharField(max_length=255, null=True, blank=True)
    api_secret = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return str(self.broker)


class ZerodhaUsersAccessToken(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.DO_NOTHING, null=True, blank=True)
    request_token = models.TextField(null=True, blank=True)
    access_token = models.TextField(null=True, blank=True)

    def __str__(self):
        return str(self.user)


class FyersUsersAccessToken(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.DO_NOTHING, null=True, blank=True)
    auth_code = models.TextField(null=True, blank=True)
    access_token = models.TextField(null=True, blank=True)

    def __str__(self):
        return str(self.user)


class IsConnectedBroker(models.Model):
    broker = models.ForeignKey(OwnBrokers, null=True, blank=True, on_delete=models.DO_NOTHING)
    user = models.ForeignKey(CustomUser, null=True, blank=True, on_delete=models.DO_NOTHING)
    broker_unique_id = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return str(self.user.email)