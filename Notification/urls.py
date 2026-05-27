from django.urls import path
from .views import NotificationListView, NotificationDetailView

urlpatterns = [
    path('<int:user_id>/', NotificationListView.as_view(), name='notification-list'),
    path('create/', NotificationListView.as_view(), name='notification-create'),
    path('<int:notification_id>/read/', NotificationDetailView.as_view(), name='notification-read'),
]