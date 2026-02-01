from rest_framework import serializers
from .models import Transaction
from accounts.serializers import AccountSerializer
from categories.serializers import CategorySerializer
from accounts.models import Account
from categories.models import Category

class TransactionReadSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    account = AccountSerializer(read_only=True)
    
    class Meta:
        model = Transaction
        fields = [
            'id', 'amount', 'type', 'description', 
            'date', 'created_at', 'updated_at', 
            'account', 'category'
        ]
        read_only_fields = fields

class TransactionWriteSerializer(serializers.ModelSerializer):
    category_id = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(), 
        source='category',
        allow_null=True,
        required=False
    )
    account_id = serializers.PrimaryKeyRelatedField(
        queryset=Account.objects.all(),
        source='account'
    )
    
    class Meta:
        model = Transaction
        fields = [
            'amount', 'type', 'description', 
            'date', 'account_id', 'category_id'
        ]

    def validate_amount(self, value):
        if value <= 0:
            raise serializers.ValidationError("Amount must be greater than 0")
        return value
    
    def validate(self, data):
        # Basic validation to ensure account belongs to user is handled in view/queryset usually,
        # but strictly speaking serializers validting foreign keys existence is default behavior.
        # Custom "ownership" validation usually happens in permission or view level if strictly enforced there,
        # or we could filter the queryset passed to PrimaryKeyRelatedField if we had the request user context.
        return data