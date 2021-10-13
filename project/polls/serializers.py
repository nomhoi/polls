from rest_framework import serializers

from .models import Pool, Question


class PoolSerializer(serializers.ModelSerializer):
    """
    Сериализатор модели опросов
    """
    class Meta:
        model = Pool
        fields = '__all__'


class QuestionSerializer(serializers.ModelSerializer):
    """
    Сериализатор модели вопросов
    """
    class Meta:
        model = Question
        fields = '__all__'
