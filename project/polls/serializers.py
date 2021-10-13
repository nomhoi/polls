from rest_framework import serializers

from .models import Pool


class PoolSerializer(serializers.ModelSerializer):
    """
    Сериализатор модели опросов
    """
    class Meta:
        model = Pool
        fields = '__all__'
