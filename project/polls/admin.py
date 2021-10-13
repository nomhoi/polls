from django.contrib import admin
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _

from .models import Choice, Pool, TextResponse, Question


class QuestionInline(admin.StackedInline):
    """Вопросы"""
    model = Question
    extra = 0


@admin.register(Pool)
class PoolAdmin(admin.ModelAdmin):
    """Опросы"""
    inlines = [QuestionInline]


class ChoiceInline(admin.StackedInline):
    """Выборы"""
    model = Choice
    extra = 0


class TextResponseInline(admin.StackedInline):
    """Текстовые ответы"""
    model = TextResponse
    extra = 0


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    """Вопросы"""
    inlines = [ChoiceInline, TextResponseInline]
    list_filter = ['pool']