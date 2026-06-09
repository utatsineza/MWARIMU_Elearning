from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView

urlpatterns = [
    path('', lambda request: redirect('/swagger/')),
    path('admin/', admin.site.urls),
    path('api/accounts/', include('Accounts.urls')),
    path('api/modules/', include('Module.urls')),
    path('api/notifications/', include('Notification.urls')),
    path('api/payments/', include('Payment.urls')),

    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('swagger/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
]