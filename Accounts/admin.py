from django.contrib import admin
from .models import User, OTPVerification, PasswordReset, Settings

@admin.register(User)
class CustomUserAdmin(admin.ModelAdmin):
    list_display  = ['user_id', 'fullname', 'username', 'email', 'created_at']
    search_fields = ['username', 'email', 'fullname']
    ordering      = ['-created_at']

@admin.register(OTPVerification)
class OTPAdmin(admin.ModelAdmin):
    list_display  = ['user', 'otp_code', 'expires_at', 'verified']
    search_fields = ['user__email']

@admin.register(PasswordReset)
class PasswordResetAdmin(admin.ModelAdmin):
    list_display  = ['user', 'reset_token', 'expires_at', 'used']
    search_fields = ['user__email']

@admin.register(Settings)
class SettingsAdmin(admin.ModelAdmin):
    list_display  = ['user', 'language', 'switch_role', 'payment_method']