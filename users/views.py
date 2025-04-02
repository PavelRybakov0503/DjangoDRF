from rest_framework import viewsets
from django_filters.rest_framework import DjangoFilterBackend
from .models import Payment, User
from .serializers import PaymentSerializer, UserProfileSerializer
from .filters import PaymentFilter


class PaymentViewSet(viewsets.ModelViewSet):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = PaymentFilter
    ordering_fields = ['date']
    ordering = ['date']  # Сортировка по умолчанию


class UserProfileViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserProfileSerializer
