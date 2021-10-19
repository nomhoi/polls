from django.contrib import admin
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _

from .models import Choice, Poll, Question, UserResponse


class QuestionInline(admin.StackedInline):
    """Вопросы"""
    model = Question
    extra = 0


@admin.register(Poll)
class PollAdmin(admin.ModelAdmin):
    """Опросы"""
    inlines = [QuestionInline]


class ChoiceInline(admin.StackedInline):
    """Выборы"""
    model = Choice
    extra = 0


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    """Вопросы"""
    inlines = [ChoiceInline]
    list_filter = ['poll']
    

@admin.register(UserResponse)
class UserResponseAdmin(admin.ModelAdmin):
    """Вопросы"""
    list_filter = ['poll', 'user']
    # TODO: фильтровать список ответов после выбора опроса и пользователя