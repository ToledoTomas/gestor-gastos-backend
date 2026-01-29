from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class UserProfile(AbstractUser):
    phone = models.CharField(max_length=15, blank=True, null=True)
    money_preference = models.CharField(max_length=3, default='ARS')

    class Meta:
        db_table = 'usuarios'
    