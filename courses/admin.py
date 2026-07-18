from django.contrib import admin
from .models import Category, Instructor, Course, Enrollment

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Instructor)
class InstructorAdmin(admin.ModelAdmin):
    list_display = ['name', 'expertise']
    search_fields = ['name', 'expertise']

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'instructor', 'price', 'level', 'is_featured', 'created_at']
    list_filter = ['category', 'level', 'is_featured', 'created_at']
    search_fields = ['title', 'short_description']
    prepopulated_fields = {'slug': ('title',)}
    list_editable = ['is_featured']

@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ['user', 'course', 'status', 'progress', 'enrolled_at']
    list_filter = ['status', 'enrolled_at']
    search_fields = ['user__username', 'course__title']
