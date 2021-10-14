from rest_framework import serializers

from .models import Choice, Pool, Question


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


class ChoiceSerializer(serializers.ModelSerializer):
    """
    Сериализатор модели вариантов ответов
    """
    class Meta:
        model = Choice
        fields = '__all__'
