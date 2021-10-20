from django.contrib.auth.models import User
from django.db import models


class Poll(models.Model):
    """Модель опросов"""
    name = models.CharField('название', max_length=200)
    start_date = models.DateTimeField('дата начала')
    end_date = models.DateTimeField('дата окончания')

    description = models.CharField('описание', max_length=200)

    class Meta:
        verbose_name = 'опрос'
        verbose_name_plural = 'опросы'

    def __str__(self):
        return self.name


class Question(models.Model):
    """Модель вопросов"""
    TYPES = (
        (TEXT := 1, 'Ответ текстом'),
        (ONE  := 2, 'Ответ с выбором одного варианта'),
        (MANY := 3, 'Ответ с выбором нескольких вариантов'),
    )

    poll = models.ForeignKey(Poll, related_name='questions', on_delete=models.CASCADE)
    text = models.CharField('вопрос', max_length=200)
    type = models.PositiveSmallIntegerField('Тип ответа', choices=TYPES)

    class Meta:
        verbose_name = 'вопрос'
        verbose_name_plural = 'вопросы'

    def __str__(self):
        return self.poll.name + ' - ' + self.text


class Choice(models.Model):
    """Модель вариантов ответов на вопросы"""
    question = models.ForeignKey(Question, related_name='choices', on_delete=models.CASCADE)
    choice = models.CharField('вариант ответа', max_length=200, null=True, blank=True)

    class Meta:
        verbose_name = 'варианты ответов'
        verbose_name_plural = 'варианты ответов'

    def __str__(self):
        return f'{self.question} - {self.choice} - pk:{self.pk}' if self.choice else f'{self.question} - Text Response - pk:{self.pk}'


class UserResponse(models.Model):
    """Модель ответов"""
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    poll = models.ForeignKey(Poll, related_name='responses', on_delete=models.CASCADE)
    choice = models.OneToOneField(Choice, on_delete=models.CASCADE, null=True, blank=True)
    boolean_response = models.BooleanField('ответ на вариант', null=True, blank=True)
    text_response = models.TextField('текстовый ответ', null=True, blank=True)

    class Meta:
        verbose_name = 'ответ'
        verbose_name_plural = 'ответы'

    def __str__(self):
        return f'{self.choice}'
