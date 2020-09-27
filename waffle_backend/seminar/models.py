from django.contrib.auth.models import User
from django.db import models


# Create your models here.

class Seminar(models.Model):
    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    userseminar = models.ForeignKey(UserSeminar, null=True, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)

class UserSeminar(models.Model):
    user = models.ForeignKey(User, null=True, on_delete = models.CASCADE)
    seminar = models.ForeignKey(Seminar, null=True, on_delete = models.CASCADE)
    role = models.CharField(blank=False, on_delete = models.CASCADE)
