from django.db import models
from django.contrib.auth.models import PermissionsMixin
from django.utils.crypto import get_random_string
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import User
from django.utils import timezone
from django.contrib.postgres.fields import ArrayField


class UserManager(BaseUserManager):
    def create_user(self, email, first_name, last_name, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, first_name=first_name, last_name=last_name, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, first_name, last_name, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, first_name, last_name, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(default='Default Last Name', max_length=255)
    account_id = models.CharField(max_length=10, unique=True, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        UserProfile.objects.get_or_create(user=self)

    def has_module_perms(self, app_label):
        return self.is_superuser

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class UserProfile(models.Model):
    objects = None
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    # add address
    address = models.CharField(max_length=255, blank=True, null=True, default='Default Address')
    addressline2 = models.CharField(max_length=255, blank=True, null=True, default='Default Address')
    phone_number = models.CharField(max_length=255)
    city_or_town = models.CharField(max_length=255)
    state_province_region = models.CharField(max_length=255)
    zip_code = models.CharField(max_length=255, blank=True, null=True)
    age_range = models.CharField(max_length=255)
    profession = models.CharField(max_length=255)
    dress_code = models.CharField(max_length=255)
    dress_code_description = models.TextField()
    upcoming_events = models.CharField(max_length=255)
    upcoming_events_description = models.TextField()
    activity = models.CharField(max_length=255)
    activity_items = ArrayField(models.CharField(max_length=255, blank=True), blank=True, default=list)
    activity_frequency = models.CharField(max_length=255)
    sports_fan = models.CharField(max_length=255)
    sports_team = models.CharField(max_length=255)
    description_items = ArrayField(models.CharField(max_length=255, blank=True), blank=True, default=list)
    outdoor_activities = ArrayField(models.CharField(max_length=255, blank=True), blank=True, default=list)
    fashion_goals = ArrayField(models.CharField(max_length=255, blank=True), blank=True, default=list)
    attention_points = ArrayField(models.CharField(max_length=255, blank=True), blank=True, default=list)
    image_base64 = ArrayField(models.TextField(blank=True), blank=True, default=list)

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"


class PasswordReset(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    token = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField(default=timezone.now() + timezone.timedelta(hours=1))


# create a model for API key generation
class ApiKey(models.Model):
    api_key = models.CharField(max_length=255, default=get_random_string(length=32))

    def __str__(self):
        return f"API Key: {self.api_key}"
