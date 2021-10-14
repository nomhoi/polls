from django.db import models


class Pool(models.Model):
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

    pool = models.ForeignKey(Pool, on_delete=models.CASCADE)
    text = models.CharField('вопрос', max_length=200)
    type = models.PositiveSmallIntegerField('Тип ответа', choices=TYPES)

    class Meta:
        verbose_name = 'вопрос'
        verbose_name_plural = 'вопросы'

    def __str__(self):
        return self.pool.name + ' - ' + self.text


class Choice(models.Model):
    """Модель выборов ответов на вопросы"""
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    text = models.CharField('вариант ответа', max_length=200)

    class Meta:
        verbose_name = 'варианты ответов'
        verbose_name_plural = 'варианты ответов'

    def __str__(self):
        return self.text


class TextResponse(models.Model):
    """Модель текстовых ответов"""
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    text = models.CharField('ответ', max_length=200)

    class Meta:
        verbose_name = 'текстовые ответы'
        verbose_name_plural = 'текстовые ответы'

    def __str__(self):
        return self.text