from rest_framework import serializers
from .models import Payment, User
from rest_framework.serializers import ModelSerializer


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = ['id', 'amount', 'date', 'paid_course', 'paid_lesson', 'payment_method']


class UserProfileSerializer(serializers.ModelSerializer):
    payments = PaymentSerializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'payments']


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"
