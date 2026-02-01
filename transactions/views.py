from rest_framework import viewsets, permissions
from .models import Transaction
from .serializers import TransactionReadSerializer, TransactionWriteSerializer

class TransactionViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Transaction.objects.filter(user=self.request.user)

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return TransactionReadSerializer
        return TransactionWriteSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
