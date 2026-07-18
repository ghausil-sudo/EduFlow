from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from .models import Profile


class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = 'Profil'
    fields = ['phone', 'address', 'birth_date', 'bio', 'photo']
    extra = 1


class CustomUserAdmin(UserAdmin):
    inlines = (ProfileInline,)
    list_display = ['username', 'email', 'first_name', 'last_name', 'is_active', 'is_staff', 'is_superuser', 'date_joined']
    list_filter = ['is_active', 'is_staff', 'is_superuser', 'date_joined']
    search_fields = ['username', 'email', 'first_name', 'last_name']
    ordering = ['-date_joined']
    fieldsets = (
        ('Informasi Akun', {
            'fields': ('username', 'password')
        }),
        ('Data Pribadi', {
            'fields': ('first_name', 'last_name', 'email')
        }),
        ('Hak Akses', {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
            'classes': ('collapse',)
        }),
        ('Tanggal', {
            'fields': ('last_login', 'date_joined'),
            'classes': ('collapse',)
        }),
    )


class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'phone', 'address', 'birth_date']
    search_fields = ['user__username', 'user__email', 'phone']
    list_filter = ['birth_date']
    raw_id_fields = ['user']


try:
    admin.site.unregister(User)
except admin.sites.NotRegistered:
    pass

admin.site.register(User, CustomUserAdmin)
admin.site.register(Profile, UserProfileAdmin)
