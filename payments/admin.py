from django.contrib import admin
from .models import SubscriptionPackage, Transaction

@admin.register(SubscriptionPackage)
class SubscriptionPackageAdmin(admin.ModelAdmin):
    list_display = ['name', 'price', 'duration_months', 'is_active', 'created_at']
    list_filter = ['is_active', 'duration_months']
    search_fields = ['name']

@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ['invoice_number', 'user', 'package', 'course', 'amount', 'status', 'payment_method', 'transaction_date']
    list_filter = ['status', 'payment_method', 'transaction_date']
    search_fields = ['invoice_number', 'user__username']
    readonly_fields = ['invoice_number', 'transaction_date']
