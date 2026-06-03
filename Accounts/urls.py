from django.urls import path
from .views import (
    RegisterView, LoginView, LogoutView, RefreshTokenView,
    UserDetailView, SettingsView,
    SendOTPView, VerifyOTPView, ForgotPasswordView, ResetPasswordView
)

urlpatterns = [
    path('register/',              RegisterView.as_view(),        name='register'),
    path('login/',                 LoginView.as_view(),           name='login'),
    path('logout/',                LogoutView.as_view(),          name='logout'),
    path('token/refresh/',         RefreshTokenView.as_view(),    name='token-refresh'),
    path('<int:user_id>/',         UserDetailView.as_view(),      name='user-detail'),
    path('<int:user_id>/settings/', SettingsView.as_view(),       name='user-settings'),
    path('send-otp/',              SendOTPView.as_view(),         name='send-otp'),
    path('verify-otp/',            VerifyOTPView.as_view(),       name='verify-otp'),
    path('forgot-password/',       ForgotPasswordView.as_view(),  name='forgot-password'),
    path('reset-password/',        ResetPasswordView.as_view(),   name='reset-password'),
]