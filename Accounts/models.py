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

class User(AbstractBaseUser):
    ROLE_CHOICES = [
        ('student',    'Student'),
        ('instructor', 'Instructor'),
        ('admin',      'Admin'),
    ]

    user_id    = models.AutoField(primary_key=True)
    fullname   = models.CharField(max_length=255)
    username   = models.CharField(max_length=150, unique=True)
    email      = models.EmailField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
    objects = CustomUserManager()

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