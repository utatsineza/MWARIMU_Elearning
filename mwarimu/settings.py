from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import User, Settings, OTPVerification, PasswordReset
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from drf_spectacular.utils import extend_schema
from django.utils import timezone
from django.core.mail import send_mail
from datetime import timedelta
from django.conf import settings
import random
import uuid
from .serializers import (
    RegisterSerializer, UserSerializer, SettingsSerializer, LoginSerializer,
    SendOTPSerializer, VerifyOTPSerializer,
    ForgotPasswordSerializer, ResetPasswordSerializer
)


class RegisterView(APIView):
    permission_classes = [AllowAny]

    @extend_schema(
        request=RegisterSerializer,
        description="Register a new user",
        tags=['Authentication']
    )
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'User registered successfully'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    permission_classes = [AllowAny]

    @extend_schema(
        request=LoginSerializer,
        description="Login with email and password",
        tags=['Authentication']
    )
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user    = serializer.validated_data['user']
            refresh = RefreshToken.for_user(user)
            return Response({
                'user':          UserSerializer(user).data,
                'access_token':  str(refresh.access_token),
                'refresh_token': str(refresh),
            })
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LogoutView(APIView):
    @extend_schema(
        description="Logout and blacklist the refresh token",
        tags=['Authentication']
    )
    def post(self, request):
        try:
            token = RefreshToken(request.data['refresh_token'])
            token.blacklist()
            return Response({'message': 'Logged out successfully'})
        except Exception:
            return Response({'error': 'Invalid token'}, status=status.HTTP_400_BAD_REQUEST)


class RefreshTokenView(APIView):
    permission_classes = []

    @extend_schema(
        description="Get a new access token using refresh token",
        tags=['Authentication']
    )
    def post(self, request):
        try:
            refresh = RefreshToken(request.data['refresh_token'])
            return Response({'access_token': str(refresh.access_token)})
        except Exception:
            return Response({'error': 'Invalid token'}, status=status.HTTP_400_BAD_REQUEST)


class UserDetailView(APIView):
    @extend_schema(
        description="Get user details by ID",
        responses={200: UserSerializer},
        tags=['Users']
    )
    def get(self, request, user_id):
        try:
            user = User.objects.get(user_id=user_id)
            return Response(UserSerializer(user).data)
        except User.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

    @extend_schema(
        request=UserSerializer,
        description="Update user details",
        tags=['Users']
    )
    def put(self, request, user_id):
        try:
            user = User.objects.get(user_id=user_id)
            serializer = UserSerializer(user, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except User.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)


class SettingsView(APIView):
    @extend_schema(
        description="Get user settings",
        responses={200: SettingsSerializer},
        tags=['Users']
    )
    def get(self, request, user_id):
        try:
            s = Settings.objects.get(user_id=user_id)
            return Response(SettingsSerializer(s).data)
        except Settings.DoesNotExist:
            return Response({'error': 'Settings not found'}, status=status.HTTP_404_NOT_FOUND)

    @extend_schema(
        request=SettingsSerializer,
        description="Update user settings",
        tags=['Users']
    )
    def put(self, request, user_id):
        try:
            s = Settings.objects.get(user_id=user_id)
            serializer = SettingsSerializer(s, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Settings.DoesNotExist:
            return Response({'error': 'Settings not found'}, status=status.HTTP_404_NOT_FOUND)


class SendOTPView(APIView):
    permission_classes = [AllowAny]

    @extend_schema(
        request=SendOTPSerializer,
        description="Send OTP to user's email",
        tags=['OTP']
    )
    def post(self, request):
        serializer = SendOTPSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            try:
                user = User.objects.get(email=email)
            except User.DoesNotExist:
                return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
            otp_code   = str(random.randint(100000, 999999))
            expires_at = timezone.now() + timedelta(minutes=10)
            OTPVerification.objects.create(user=user, otp_code=otp_code, expires_at=expires_at)
            send_mail(
                subject='Your OTP Code - Mwarimu',
                message=f'Your OTP code is: {otp_code}\nIt expires in 10 minutes.',
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[email],
            )
            return Response({'message': 'OTP sent successfully'})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class VerifyOTPView(APIView):
    permission_classes = [AllowAny]

    @extend_schema(
        request=VerifyOTPSerializer,
        description="Verify OTP code",
        tags=['OTP']
    )
    def post(self, request):
        serializer = VerifyOTPSerializer(data=request.data)
        if serializer.is_valid():
            email    = serializer.validated_data['email']
            otp_code = serializer.validated_data['otp_code']
            try:
                user = User.objects.get(email=email)
                otp  = OTPVerification.objects.filter(
                    user=user, otp_code=otp_code,
                    verified=False, expires_at__gt=timezone.now()
                ).latest('expires_at')
                otp.verified = True
                otp.save()
                return Response({'message': 'OTP verified successfully'})
            except User.DoesNotExist:
                return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
            except OTPVerification.DoesNotExist:
                return Response({'error': 'Invalid or expired OTP'}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ForgotPasswordView(APIView):
    permission_classes = [AllowAny]

    @extend_schema(
        request=ForgotPasswordSerializer,
        description="Send password reset link to email",
        tags=['Password Reset']
    )
    def post(self, request):
        serializer = ForgotPasswordSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            try:
                user = User.objects.get(email=email)
            except User.DoesNotExist:
                return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
            reset_token = str(uuid.uuid4())
            expires_at  = timezone.now() + timedelta(hours=1)
            PasswordReset.objects.create(user=user, reset_token=reset_token, expires_at=expires_at)
            reset_link = f'http://localhost:3000/reset-password?token={reset_token}'
            send_mail(
                subject='Password Reset - Mwarimu',
                message=f'Click the link to reset your password:\n{reset_link}\nExpires in 1 hour.',
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[email],
            )
            return Response({'message': 'Password reset link sent to your email'})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ResetPasswordView(APIView):
    permission_classes = [AllowAny]

    @extend_schema(
        request=ResetPasswordSerializer,
        description="Reset password using token",
        tags=['Password Reset']
    )
    def post(self, request):
        serializer = ResetPasswordSerializer(data=request.data)
        if serializer.is_valid():
            reset_token  = serializer.validated_data['reset_token']
            new_password = serializer.validated_data['new_password']
            try:
                reset = PasswordReset.objects.get(
                    reset_token=reset_token, used=False,
                    expires_at__gt=timezone.now()
                )
                reset.user.set_password(new_password)
                reset.user.save()
                reset.used = True
                reset.save()
                return Response({'message': 'Password reset successfully'})
            except PasswordReset.DoesNotExist:
                return Response({'error': 'Invalid or expired token'}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)