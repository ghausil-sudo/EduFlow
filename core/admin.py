from django.contrib import admin
from .models import ContactMessage

@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'subject', 'status', 'sent_at']
    list_filter = ['status', 'sent_at']
    search_fields = ['name', 'email', 'subject']
