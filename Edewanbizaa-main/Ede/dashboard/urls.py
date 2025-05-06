from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CourseViewSet, AssignmentViewSet, NotificationViewSet

router = DefaultRouter()
router.register(r'courses', CourseViewSet, basename='course')
router.register(r'assignments', AssignmentViewSet, basename='assignment')
router.register(r'notifications', NotificationViewSet, basename='notification')

urlpatterns = [
    path('', include(router.urls)),
] 