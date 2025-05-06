from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.utils import timezone
from .models import Assignment, Notification

@receiver(pre_save, sender=Assignment)
def update_assignment_status(sender, instance, **kwargs):
    if instance.due_date < timezone.now() and instance.status != 'completed':
        instance.status = 'overdue'

@receiver(post_save, sender=Assignment)
def create_assignment_notification(sender, instance, created, **kwargs):
    if created:
        Notification.objects.create(
            user=instance.assigned_to,
            title=f"New Assignment: {instance.title}",
            message=f"You have been assigned a new task: {instance.description}",
            notification_type='assignment',
            related_assignment=instance
        ) 