from django.db import models
from users.models import UserProfile
from accounts.models import Account
from categories.models import Category

TYPE_CHOICES = [('ingreso','Ingreso'),('gasto','Gasto')]

class Transaction(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='transactions')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    type = models.CharField(max_length=10, choices=TYPE_CHOICES)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name='transactions')
    account = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='transactions')
    description = models.TextField(blank=True, null=True)
    date = models.DateField(auto_now_add=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta: 
        db_table = 'transactions'
        ordering = ['-date', '-created_at']
        indexes = [
            models.Index(fields=['user']),
            models.Index(fields=['user', '-date']),
            models.Index(fields=['-type']),
        ]

    def __str__(self):
        return f"{self.type} - {self.amount} - {self.date}"

    def save(self, *args, **kwargs):
        if self.pk is None:
            if self.type == 'ingreso':
                self.account.actual_balance += self.amount
            else:
                self.account.actual_balance -= self.amount
            self.account.save()
        super().save(*args, **kwargs)