from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import User, Settings
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import RegisterSerializer, UserSerializer, SettingsSerializer, LoginSerializer
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from django.utils import timezone
from django.core.mail import send_mail
from datetime import timedelta
import random
import uuid
from .models import OTPVerification, PasswordReset
from .serializers import (
    SendOTPSerializer, VerifyOTPSerializer,
    ForgotPasswordSerializer, ResetPasswordSerializer
)

class RegisterView(APIView):
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        request_body=RegisterSerializer,
        operation_description="Register a new user",
        responses={201: "User registered successfully", 400: "Bad Request"}
    )
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'User registered successfully'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        request_body=LoginSerializer,
        operation_description="Login with email and password",
        responses={
            200: openapi.Response('Login successful', schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'access_token': openapi.Schema(type=openapi.TYPE_STRING),
                    'refresh_token': openapi.Schema(type=openapi.TYPE_STRING),
                    'user': openapi.Schema(type=openapi.TYPE_OBJECT),
                }
            )),
            400: "Invalid credentials"
        }
    )
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user         = serializer.validated_data['user']
            refresh      = RefreshToken.for_user(user)
            return Response({
                'user':          UserSerializer(user).data,
                'access_token':  str(refresh.access_token),
                'refresh_token': str(refresh),
            })
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LogoutView(APIView):
    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['refresh_token'],
            properties={
                'refresh_token': openapi.Schema(type=openapi.TYPE_STRING, description='Refresh token')
            }
        ),
        operation_description="Logout and blacklist the refresh token",
        responses={200: "Logged out successfully", 400: "Invalid token"}
    )
    def post(self, request):
        try:
            refresh_token = request.data['refresh_token']
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({'message': 'Logged out successfully'})
        except Exception:
            return Response({'error': 'Invalid token'}, status=status.HTTP_400_BAD_REQUEST)


class RefreshTokenView(APIView):
    permission_classes = []

    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['refresh_token'],
            properties={
                'refresh_token': openapi.Schema(type=openapi.TYPE_STRING, description='Refresh token')
            }
        ),
        operation_description="Get a new access token using refresh token",
        responses={200: "New access token", 400: "Invalid token"}
    )
    def post(self, request):
        try:
            refresh = RefreshToken(request.data['refresh_token'])
            return Response({'access_token': str(refresh.access_token)})
        except Exception:
            return Response({'error': 'Invalid token'}, status=status.HTTP_400_BAD_REQUEST)


class UserDetailView(APIView):
    @swagger_auto_schema(
        operation_description="Get user details by ID",
        responses={200: UserSerializer, 404: "User not found"}
    )
    def get(self, request, user_id):
        try:
            user = User.objects.get(user_id=user_id)
            serializer = UserSerializer(user)
            return Response(serializer.data)
        except User.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

    @swagger_auto_schema(
        request_body=UserSerializer,
        operation_description="Update user details",
        responses={200: UserSerializer, 404: "User not found"}
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
    @swagger_auto_schema(
        operation_description="Get user settings",
        responses={200: SettingsSerializer, 404: "Settings not found"}
    )
    def get(self, request, user_id):
        try:
            settings = Settings.objects.get(user_id=user_id)
            serializer = SettingsSerializer(settings)
            return Response(serializer.data)
        except Settings.DoesNotExist:
            return Response({'error': 'Settings not found'}, status=status.HTTP_404_NOT_FOUND)

    @swagger_auto_schema(
        request_body=SettingsSerializer,
        operation_description="Update user settings",
        responses={200: SettingsSerializer, 404: "Settings not found"}
    )
    def put(self, request, user_id):
        try:
            settings = Settings.objects.get(user_id=user_id)
            serializer = SettingsSerializer(settings, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Settings.DoesNotExist:
            return Response({'error': 'Settings not found'}, status=status.HTTP_404_NOT_FOUND)
        

class SendOTPView(APIView):
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        request_body=SendOTPSerializer,
        operation_description="Send OTP to user's email",
        responses={200: "OTP sent successfully", 404: "User not found"}
    )
    def post(self, request):
        serializer = SendOTPSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            try:
                user = User.objects.get(email=email)
            except User.DoesNotExist:
                return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

            otp_code = str(random.randint(100000, 999999))
            expires_at = timezone.now() + timedelta(minutes=10)

            # Save OTP
            OTPVerification.objects.create(
                user=user,
                otp_code=otp_code,
                expires_at=expires_at
            )

            # Send email
            send_mail(
                subject='Your OTP Code - Mwarimu',
                message=f'Your OTP code is: {otp_code}\nIt expires in 10 minutes.',
                from_email='your@gmail.com',
                recipient_list=[email],
            )

            return Response({'message': 'OTP sent successfully'})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class VerifyOTPView(APIView):
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        request_body=VerifyOTPSerializer,
        operation_description="Verify OTP code",
        responses={200: "OTP verified", 400: "Invalid or expired OTP"}
    )
    def post(self, request):
        serializer = VerifyOTPSerializer(data=request.data)
        if serializer.is_valid():
            email    = serializer.validated_data['email']
            otp_code = serializer.validated_data['otp_code']
            try:
                user = User.objects.get(email=email)
                otp  = OTPVerification.objects.filter(
                    user=user,
                    otp_code=otp_code,
                    verified=False,
                    expires_at__gt=timezone.now()
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

    @swagger_auto_schema(
        request_body=ForgotPasswordSerializer,
        operation_description="Send password reset link to email",
        responses={200: "Reset link sent", 404: "User not found"}
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

            PasswordReset.objects.create(
                user=user,
                reset_token=reset_token,
                expires_at=expires_at
            )

            reset_link = f'http://localhost:3000/reset-password?token={reset_token}'

            send_mail(
                subject='Password Reset - Mwarimu',
                message=f'Click the link to reset your password:\n{reset_link}\nExpires in 1 hour.',
                from_email='your@gmail.com',
                recipient_list=[email],
            )

            return Response({'message': 'Password reset link sent to your email'})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ResetPasswordView(APIView):
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        request_body=ResetPasswordSerializer,
        operation_description="Reset password using token",
        responses={200: "Password reset successful", 400: "Invalid or expired token"}
    )
    def post(self, request):
        serializer = ResetPasswordSerializer(data=request.data)
        if serializer.is_valid():
            reset_token  = serializer.validated_data['reset_token']
            new_password = serializer.validated_data['new_password']
            try:
                reset = PasswordReset.objects.get(
                    reset_token=reset_token,
                    used=False,
                    expires_at__gt=timezone.now()
                )
                user = reset.user
                user.set_password(new_password)
                user.save()

                reset.used = True
                reset.save()

                return Response({'message': 'Password reset successfully'})
            except PasswordReset.DoesNotExist:
                return Response({'error': 'Invalid or expired token'}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)        