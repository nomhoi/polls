from django.db import models

class Pool(models.Model):
    name = models.CharField('название', max_length=200)
    start_date = models.DateTimeField('дата начала')
    end_date = models.DateTimeField('дата окончания')

    description = models.TextField('описание')

    class Meta:
        verbose_name = 'опрос'
        verbose_name_plural = 'опросы'

    def __str__(self):
        return self.name
