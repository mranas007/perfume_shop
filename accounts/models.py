from django.db import models
from django.contrib.auth.models import AbstractUser, PermissionsMixin
from django.utils.text import slugify
from django.contrib.auth.models import AbstractUser, PermissionsMixin, BaseUserManager



# User Manager - Custom User Manager for User Model
class UserManager(BaseUserManager):

    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, password, **extra_fields)


class User(AbstractUser, PermissionsMixin):
    slug = models.SlugField(max_length=160, unique=True, blank=True)
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    avatar = models.ImageField(null=True, blank=True, default='uploads/user/avatar.svg', upload_to='uploads/user')
    is_active = models.BooleanField(default=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


