from django.db import models
from django.db.models.signals import post_save
from django.conf import settings
from django.dispatch import receiver
from rest_framework.authtoken.models import Token




class TimeStampModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Todo(TimeStampModel):

    PENDING = 'Pendiente'
    COMPLETE = 'Completada'
    CHOICES = (
        (PENDING, 'Pendiente'),
        (COMPLETE, 'Completada')
    )

    description = models.CharField(max_length=100)
    duration = models.PositiveSmallIntegerField()
    recorded_time = models.PositiveSmallIntegerField(null=True, blank=True)
    status = models.CharField(
        max_length=20,
        choices=CHOICES,
        default=PENDING
    )
    

    def __str__(self):
        return self.description



@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)