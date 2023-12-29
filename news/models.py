from django.db import models
from django.contrib.auth.models import User


class News(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Владелец')
    title = models.TextField(max_length=100, blank=False, verbose_name='Заголовок')
    description = models.TextField(max_length=2000, blank=True, verbose_name='Текст')
    date = models.DateTimeField(auto_now=True, verbose_name='Дата публикации')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = "Новости"