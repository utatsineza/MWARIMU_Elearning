from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models

# Create your models here.

class CustomUserManager(BaseUserManager):
    def create_user(self, email, username, password=None, **extra_fields):
        email = self.normalize_email(email)
        user = self.model(email=email, username=username, **extra_fields)
        user.set_password(password)
        user.save()
        return user
    
    def create_superuser(self, email, username, password=None, **extra_fields):
        user             = self.create_user(email, username, password, **extra_fields)
        user.is_staff    = True
        user.is_superuser = True
        user.save()
        return user

class User(AbstractBaseUser):
    ROLE_CHOICES = [
        ('student',    'Student'),
        ('instructor', 'Instructor'),
        ('admin',      'Admin'),
    ]

    user_id      = models.AutoField(primary_key=True)
    fullname     = models.CharField(max_length=255)
    username     = models.CharField(max_length=150, unique=True)
    email        = models.EmailField(unique=True)
    role         = models.CharField(max_length=20, choices=ROLE_CHOICES, default='student')
    is_staff     = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_active    = models.BooleanField(default=True)
    created_at   = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
    objects = CustomUserManager()

    def has_perm(self, perm, obj=None):
        return self.is_superuser

    def has_module_perms(self, app_label):
        return self.is_superuser

    def __str__(self):
        return self.email

class OTPVerification(models.Model):
    user       = models.ForeignKey(User, on_delete=models.CASCADE)
    otp_code   = models.CharField(max_length=10)
    expires_at = models.DateTimeField()
    verified   = models.BooleanField(default=False)

class PasswordReset(models.Model):
    user        = models.ForeignKey(User, on_delete=models.CASCADE)
    reset_token = models.CharField(max_length=255)
    expires_at  = models.DateTimeField()
    used        = models.BooleanField(default=False)
    created_at  = models.DateTimeField(auto_now_add=True)

class Settings(models.Model):
    user           = models.OneToOneField(User, on_delete=models.CASCADE)
    language       = models.CharField(max_length=50)
    switch_role    = models.CharField(max_length=50)
    payment_method = models.CharField(max_length=100)
    created_at     = models.DateTimeField(auto_now_add=True)