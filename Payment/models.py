from django.db import models
from Module.models import Enrollment

class Payment(models.Model):
    enrollment = models.ForeignKey(Enrollment, on_delete=models.CASCADE, related_name='payments')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.CharField(max_length=50, help_text="'mobile_money', 'card'")
    provider = models.CharField(max_length=50, help_text="'MTN', 'Airtel', 'BK', etc.")
    payment_status = models.CharField(max_length=50, help_text="'initiated', 'completed', 'failed'")
    transaction_reference = models.CharField(max_length=150, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Payment {self.transaction_reference} - {self.payment_status}"
