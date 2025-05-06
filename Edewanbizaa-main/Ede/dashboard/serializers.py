from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Course, Assignment, Notification

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name']

class CourseSerializer(serializers.ModelSerializer):
    instructor = UserSerializer(read_only=True)
    students = UserSerializer(many=True, read_only=True)
    
    class Meta:
        model = Course
        fields = ['id', 'title', 'description', 'instructor', 'students', 'created_at', 'updated_at']

class AssignmentSerializer(serializers.ModelSerializer):
    assigned_by = UserSerializer(read_only=True)
    assigned_to = UserSerializer(read_only=True)
    course = CourseSerializer(read_only=True)
    
    class Meta:
        model = Assignment
        fields = ['id', 'title', 'description', 'course', 'assigned_by', 'assigned_to', 
                 'due_date', 'status', 'created_at', 'updated_at']

class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = ['id', 'title', 'message', 'notification_type', 'is_read', 
                 'related_course', 'related_assignment', 'created_at']