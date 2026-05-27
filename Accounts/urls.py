from django.urls import path
from .views import RegisterView, UserDetailView, SettingsView, LoginView, LogoutView, RefreshTokenView

urlpatterns = [
    path('register/',      RegisterView.as_view(),     name='register'),
    path('login/',         LoginView.as_view(),         name='login'),
    path('logout/',        LogoutView.as_view(),        name='logout'),
    path('token/refresh/', RefreshTokenView.as_view(),  name='token-refresh'),
    path('<int:user_id>/', UserDetailView.as_view(),    name='user-detail'),
    path('<int:user_id>/settings/', SettingsView.as_view(), name='user-settings'),
]