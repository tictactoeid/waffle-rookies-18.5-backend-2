from django.db import models
from django.contrib.auth.models import User
#from seminar.models import Seminar

# Create your models here.

class ParticipantProfile(models.Model):
    user = models.OneToOneField(User, related_name='participant', on_delete = models.CASCADE)
    #seminar = models.ForeignKey(Seminar, related_name='instructors', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    university = models.CharField(max_length=50, blank=True)
    accepted = models.BooleanField(default = True)

'''
@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:'''


class InstructorProfile(models.Model):
    user = models.OneToOneField(User, related_name='instructor', on_delete = models.CASCADE)
    #seminar = models.ForeignKey(Seminar, related_name='participants', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    company = models.CharField(max_length=20, blank=True)
    year = models.PositiveSmallIntegerField(null=True)

