from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.utils import timezone
from django.contrib.auth.models import AnonymousUser
from .models import Course, Assignment, Notification
from .serializers import CourseSerializer, AssignmentSerializer, NotificationSerializer

class CourseViewSet(viewsets.ModelViewSet):
    serializer_class = CourseSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if isinstance(user, AnonymousUser):
            return Course.objects.none()
        if self.action == 'list':
            return Course.objects.filter(students=user) | Course.objects.filter(instructor=user)
        return Course.objects.all()

    def perform_create(self, serializer):
        serializer.save(instructor=self.request.user)

    @action(detail=True, methods=['post'])
    def enroll(self, request, pk=None):
        if isinstance(request.user, AnonymousUser):
            return Response({'error': 'Authentication required'}, status=status.HTTP_401_UNAUTHORIZED)
        course = self.get_object()
        course.students.add(request.user)
        Notification.objects.create(
            user=request.user,
            title=f"Course Enrollment",
            message=f"You have been enrolled in the course: {course.title}",
            notification_type='course',
            related_course=course
        )
        return Response({'status': 'enrolled'})

    @action(detail=True, methods=['post'])
    def unenroll(self, request, pk=None):
        if isinstance(request.user, AnonymousUser):
            return Response({'error': 'Authentication required'}, status=status.HTTP_401_UNAUTHORIZED)
        course = self.get_object()
        course.students.remove(request.user)
        return Response({'status': 'unenrolled'})

class AssignmentViewSet(viewsets.ModelViewSet):
    serializer_class = AssignmentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if isinstance(user, AnonymousUser):
            return Assignment.objects.none()
        if self.action == 'list':
            return Assignment.objects.filter(assigned_to=user)
        return Assignment.objects.all()

    def perform_create(self, serializer):
        serializer.save(assigned_by=self.request.user)

    @action(detail=True, methods=['post'])
    def update_status(self, request, pk=None):
        if isinstance(request.user, AnonymousUser):
            return Response({'error': 'Authentication required'}, status=status.HTTP_401_UNAUTHORIZED)
        assignment = self.get_object()
        new_status = request.data.get('status')
        if new_status in dict(Assignment.STATUS_CHOICES):
            assignment.status = new_status
            assignment.save()
            Notification.objects.create(
                user=assignment.assigned_to,
                title=f"Assignment Status Updated",
                message=f"Your assignment '{assignment.title}' status has been updated to {new_status}",
                notification_type='assignment',
                related_assignment=assignment
            )
            return Response({'status': 'updated'})
        return Response({'error': 'Invalid status'}, status=status.HTTP_400_BAD_REQUEST)

class NotificationViewSet(viewsets.ModelViewSet):
    serializer_class = NotificationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if isinstance(user, AnonymousUser):
            return Notification.objects.none()
        return Notification.objects.filter(user=user)

    @action(detail=False, methods=['get'])
    def unread(self, request):
        if isinstance(request.user, AnonymousUser):
            return Response({'error': 'Authentication required'}, status=status.HTTP_401_UNAUTHORIZED)
        unread_notifications = Notification.objects.filter(
            user=request.user,
            is_read=False
        )
        serializer = self.get_serializer(unread_notifications, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def mark_as_read(self, request, pk=None):
        if isinstance(request.user, AnonymousUser):
            return Response({'error': 'Authentication required'}, status=status.HTTP_401_UNAUTHORIZED)
        notification = self.get_object()
        notification.is_read = True
        notification.save()
        return Response({'status': 'marked as read'}) 