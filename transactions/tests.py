from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from django.contrib.auth import get_user_model
from .models import Transaction
from accounts.models import Account
from categories.models import Category
from users.models import UserProfile

User = get_user_model()

class TransactionTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', email='test@example.com', password='password123')
        self.user_profile = self.user
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)
        
        self.account = Account.objects.create(
            name="Test Account", 
            user=self.user_profile, 
            actual_balance=1000,
            initial_balance=1000,
            type='efectivo',
            money_type='ARS'
        )
        self.category = Category.objects.create(name="Test Category", user=self.user_profile, type='gasto')

    def test_create_transaction(self):
        data = {
            'amount': 100,
            'type': 'gasto',
            'description': 'Test Transaction',
            'date': '2023-01-01',
            'account_id': self.account.id,
            'category_id': self.category.id
        }
        response = self.client.post('/api/transactions/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Transaction.objects.count(), 1)
        self.assertEqual(Transaction.objects.get().user, self.user_profile)

    def test_list_transactions(self):
        Transaction.objects.create(
            user=self.user_profile,
            amount=50,
            type='gasto',
            account=self.account,
            category=self.category,
            date='2023-01-01'
        )
        response = self.client.get('/api/transactions/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
