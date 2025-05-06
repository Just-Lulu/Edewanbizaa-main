from django.contrib import admin
from .models import Course, Assignment, Notification

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('title', 'instructor', 'created_at', 'updated_at')
    list_filter = ('created_at', 'updated_at')
    search_fields = ('title', 'description', 'instructor__username')
    filter_horizontal = ('students',)

@admin.register(Assignment)
class AssignmentAdmin(admin.ModelAdmin):
    list_display = ('title', 'course', 'assigned_by', 'assigned_to', 'due_date', 'status')
    list_filter = ('status', 'due_date', 'created_at')
    search_fields = ('title', 'description', 'course__title', 'assigned_by__username', 'assigned_to__username')

@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'notification_type', 'is_read', 'created_at')
    list_filter = ('notification_type', 'is_read', 'created_at')
    search_fields = ('title', 'message', 'user__username') 