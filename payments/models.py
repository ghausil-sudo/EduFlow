import uuid
import datetime
from django.db import models
from django.conf import settings

class SubscriptionPackage(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    duration_months = models.IntegerField()
    benefits = models.TextField(help_text="Describe benefits, one per line or JSON")
    max_courses = models.IntegerField(default=5, help_text="Number of courses accessible")
    has_certificate = models.BooleanField(default=False)
    has_mentoring = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['price']

    def __str__(self):
        return self.name

class Transaction(models.Model):
    PAYMENT_METHODS = [
        ('bank_transfer', 'Transfer Bank'),
        ('e_wallet', 'E-Wallet'),
    ]

    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Berhasil', 'Berhasil'),
        ('Gagal', 'Gagal'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='transactions')
    package = models.ForeignKey(SubscriptionPackage, on_delete=models.SET_NULL, related_name='transactions', blank=True, null=True)
    course = models.ForeignKey('courses.Course', on_delete=models.SET_NULL, related_name='transactions', blank=True, null=True)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHODS)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    transaction_date = models.DateTimeField(auto_now_add=True)
    invoice_number = models.CharField(max_length=50, unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.invoice_number:
            today = datetime.date.today().strftime('%Y%m%d')
            unique_id = str(uuid.uuid4())[:8].upper()
            self.invoice_number = f"INV-{today}-{unique_id}"
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.invoice_number} - {self.user.username}"
