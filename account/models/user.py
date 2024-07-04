import re
from django.db import models
from general.models import TimeStampedModel
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, UserManager

class UserManager(UserManager):
    def _create_user(self, name, email, password, **extra_fields):
        if not email:
            raise ValueError("Invalid email address.")

        email = self.normalize_email(email)
        user = self.model(email=email, name=name, **extra_fields)
        user.set_password(password)
        user.save()

        return user

    def create_user(self, email, password, name='', **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)

        return self._create_user(name, email, password, **extra_fields)

    def create_superuser(self, email, password, name='', **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self._create_user(name, email, password, **extra_fields)

class User(AbstractBaseUser, PermissionsMixin, TimeStampedModel):
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=100, blank=True, default='')
    phone = models.CharField(max_length=20, blank=True, default='')
    avatar = models.ImageField(blank=True, null=True, upload_to='avatars')

    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)

    last_login = models.DateTimeField(null=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        ordering = ['created_at']
        db_table = 'users'

    def __str__(self):
        return f"{self.email}"

    def normalize_phone_number(self, phone):
        # Normalize the phone number to the format +62xx
        if phone.startswith('0'):
            phone = '62' + phone[1:]
        # Remove any non-digit characters
        phone = re.sub(r'\D', '', phone)
        return phone

    def save(self, *args, **kwargs):
        self.phone = self.normalize_phone_number(self.phone)
        super(User, self).save(*args, **kwargs)