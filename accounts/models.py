from django.db import models
from users.models import UserProfile

TIPO_CUENTA_CHOICES = [
        ('efectivo', 'Efectivo'),
        ('banco', 'Cuenta Bancaria'),
        ('tarjeta', 'Tarjeta de Crédito'),
        ('ahorro', 'Cuenta de Ahorro'),
        ('otro', 'Otro'),
    ]

# Create your models here.
class Account(models.Model):
    name = models.CharField(max_length=100)
    type = models.CharField(max_length=100, choices=TIPO_CUENTA_CHOICES)
    actual_balance = models.DecimalField(max_digits=10, decimal_places=2)
    initial_balance = models.DecimalField(max_digits=10, decimal_places=2)
    money_type = models.CharField(max_length=100)
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='accounts')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'accounts'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['name']),
        ]

    def __str__(self):
        return f"{self.name} - {self.actual_balance} {self.money_type}"
