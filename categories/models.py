from django.db import models
from users.models import UserProfile

TYPE_CHOICES = [('ingreso','Ingreso'),('gasto','Gasto')]

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=100)
    type = models.CharField(max_length=10, choices=TYPE_CHOICES)
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='categories')
    icon = models.CharField(max_length=100, blank=True, null=True)
    color = models.CharField(max_length=100, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'categories'
        ordering = ['-type', 'name']
        unique_together = ['name', 'user', 'type']

    def __str__(self):
        return f"{self.name} - {self.type}"
