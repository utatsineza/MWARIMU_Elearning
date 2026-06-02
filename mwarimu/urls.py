
from django.contrib import admin
from django.urls import path, include
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi


schema_view = get_schema_view(
    openapi.Info(
        title="Mwarimu E-learning API",
        default_version='v1',
        description="API documentation for Mwarimu E-learning platform",
        contact=openapi.Contact(email="contact@example.local"),
        license=openapi.License(name="MIT License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),

)
urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/accounts/', include('Accounts.urls')),
    path('api/modules/', include('Module.urls')),
    path('api/notifications/', include('Notification.urls')),
    path('api/payments/', include('Payment.urls')),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]
