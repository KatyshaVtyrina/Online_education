from rest_framework import serializers

from education.serializers import PaymentSerializer
from users.models import User


class UserSerializer(serializers.ModelSerializer):
    """Класс-сериализатор для модели User"""
    payments = PaymentSerializer(source='payments_set.all', many=True)

    class Meta:
        model = User
        fields = '__all__'
