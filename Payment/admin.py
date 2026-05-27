from django.contrib import admin
from .models import Payment

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display  = ['user', 'course', 'amount', 'payment_method', 'status', 'created_at']
    search_fields = ['user__email', 'course__course_name']
    list_filter   = ['status', 'payment_method']