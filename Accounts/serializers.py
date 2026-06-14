from rest_framework import serializers
from .models import User, OTPVerification, PasswordReset, Settings
from django.contrib.auth import authenticate

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model  = User
        fields = ['user_id', 'fullname', 'username', 'email', 'created_at']

class RegisterSerializer(serializers.ModelSerializer):
    password         = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)

    class Meta:
        model  = User
        fields = ['fullname', 'email', 'password', 'confirm_password']

    def validate(self, data):
        if data['password'] != data['confirm_password']:
            raise serializers.ValidationError({'confirm_password': 'Passwords do not match'})
        return data

    def create(self, validated_data):
        validated_data.pop('confirm_password')
        validated_data['username'] = validated_data['email']
        user = User.objects.create_user(**validated_data)
        return user

class OTPSerializer(serializers.ModelSerializer):
    class Meta:
        model  = OTPVerification
        fields = ['user', 'otp_code', 'expires_at', 'verified']

class PasswordResetSerializer(serializers.ModelSerializer):
    class Meta:
        model  = PasswordReset
        fields = ['user', 'reset_token', 'expires_at', 'used']

class SettingsSerializer(serializers.ModelSerializer):
    class Meta:
        model  = Settings
        fields = ['user', 'language', 'switch_role', 'payment_method']

class LoginSerializer(serializers.Serializer):
    email    = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        user = authenticate(username=data['email'], password=data['password'])
        if not user:
            raise serializers.ValidationError('Invalid email or password')
        return {'user': user}

class SendOTPSerializer(serializers.Serializer):
    email = serializers.EmailField()

class VerifyOTPSerializer(serializers.Serializer):
    email    = serializers.EmailField()
    otp_code = serializers.CharField(max_length=10)

class ForgotPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()

class ResetPasswordSerializer(serializers.Serializer):
    email        = serializers.EmailField(required=False)
    otp_code     = serializers.CharField(max_length=10, required=False)
    reset_token  = serializers.CharField(required=False)
    new_password = serializers.CharField(write_only=True)