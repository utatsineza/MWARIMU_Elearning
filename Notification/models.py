from django.db import models
from Accounts.models import User

class NotificationTemplate(models.Model):
    event_name = models.CharField(max_length=255, help_text="e.g., 'course_approved', 'payment_success'")
    title_en = models.CharField(max_length=255)
    title_rw = models.CharField(max_length=255, help_text="Kinyarwanda translation")
    body_en = models.TextField()
    body_rw = models.TextField(help_text="Kinyarwanda translation")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.event_name

class UserNotification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    template = models.ForeignKey(NotificationTemplate, on_delete=models.CASCADE, related_name='user_notifications', help_text="Ties the specific alert back to its origin template type")
    title = models.CharField(max_length=255, help_text="Rendered dynamically based on preferences")
    body = models.TextField(help_text="Rendered dynamically based on preferences")
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Notification for {self.user.username} - {self.title}"
