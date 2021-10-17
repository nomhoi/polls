from rest_framework import serializers
from drf_writable_nested.serializers import WritableNestedModelSerializer

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


class ChoiceNestedSerializer(serializers.ModelSerializer):
    """
    Сериализатор модели вариантов ответов
    """
    class Meta:
        model = Choice
        fields = ('text',)


class QuestionNestedSerializer(WritableNestedModelSerializer):
    """
    Сериализатор модели вопросов с вариантами ответов
    """
    choices = ChoiceNestedSerializer(many=True)

    class Meta:
        model = Question
        fields = ('type', 'text', 'choices')


class PoolNestedSerializer(WritableNestedModelSerializer):
    """
    Сериализатор модели опросов с вопросами
    """
    questions = QuestionNestedSerializer(many=True)

    class Meta:
        model = Pool
        fields = ('name', 'start_date', 'end_date', 'description', 'questions')
