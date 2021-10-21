from django.db.models import fields
from rest_framework import serializers
from drf_writable_nested.mixins import UniqueFieldsMixin
from drf_writable_nested.serializers import WritableNestedModelSerializer

from .models import Choice, Poll, Question, UserResponse


class PollSerializer(serializers.ModelSerializer):
    """
    Сериализатор модели опросов
    """
    class Meta:
        model = Poll
        fields = '__all__'


class ChoiceSerializer(serializers.ModelSerializer):
    """
    Сериализатор модели вариантов ответов
    """
    class Meta:
        model = Choice
        fields = ('id', 'choice')


class QuestionNestedChoiceSerializer(WritableNestedModelSerializer):
    """
    Сериализатор модели вопросов с вариантами ответов
    """
    choices = ChoiceSerializer(many=True)

    class Meta:
        model = Question
        fields = ('id', 'type', 'text', 'choices')


class PollNestedQuestionSerializer(WritableNestedModelSerializer):
    """
    Сериализатор модели опросов с вопросами
    """
    questions = QuestionNestedChoiceSerializer(many=True)

    class Meta:
        model = Poll
        fields = ('id', 'name', 'start_date', 'end_date', 'description', 'questions')


class PollNestedQuestionForUpdateSerializer(WritableNestedModelSerializer):
    """
    Сериализатор модели опросов с вопросами без возможности обновления start_date.
    """
    questions = QuestionNestedChoiceSerializer(many=True)

    class Meta:
        model = Poll
        fields = ('id', 'name', 'end_date', 'description', 'questions')


class UserResponseSerializer(UniqueFieldsMixin, serializers.ModelSerializer):
    """
    Сериализатор ответов пользователя    
    """
    class Meta:
        model = UserResponse
        fields = '__all__'


class PollNestedUserResponseSerializer(WritableNestedModelSerializer):
    """
    Сериализатор для добавления и обновления ответов пользователя
    """    
    responses = UserResponseSerializer(many=True)

    class Meta:
        model = Poll
        fields = ('id', 'responses')
