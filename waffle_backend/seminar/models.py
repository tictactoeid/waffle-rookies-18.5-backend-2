from django.contrib.auth.models import User
from django.db import models
from user.models import InstructorProfile, ParticipantProfile


# Create your models here.

class Seminar(models.Model):
    instructors = models.ForeignKey(InstructorProfile, null=True, related_name = 'instructors', on_delete=models.CASCADE)
    participants = models.ForeignKey(ParticipantProfile, null=True, related_name = 'participants', on_delete=models.CASCADE)

    #userseminar = models.ForeignKey(UserSeminar, null=True, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    name = models.CharField(max_length=30)
    capacity = models.PositiveIntegerField()
    count = models.PositiveIntegerField()
    time = models.TimeField()
    online = models.BooleanField(default = True)
    #instructor =

    #def __str__(self):
        #return


class UserSeminar(models.Model):
    user = models.ForeignKey(User, null=True, related_name = 'user', on_delete = models.CASCADE)
    seminar = models.ForeignKey(Seminar, null=True, related_name = 'seminar', on_delete = models.CASCADE)
    joined_at = models.DateTimeField()
    is_active = models.BooleanField(null=False, default = True)
    dropped_at = models.DateTimeField(null=True)
    #role = models.CharField(blank=False, on_delete = models.CASCADE)
