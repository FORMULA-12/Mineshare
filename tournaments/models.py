from django.db import models
from django.contrib.auth.models import User


class Bedwars(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Отправитель')
    contact = models.TextField(max_length=80, blank=False, verbose_name='Контакт')
    description = models.TextField(max_length=500, blank=True, verbose_name='Описание')
    team = models.CharField(max_length=24, blank=False, verbose_name='Название команды')
    player1 = models.CharField(max_length=20, blank=False, verbose_name='Участник №1')
    player2 = models.CharField(max_length=20, blank=False, verbose_name='Участник №2')
    player3 = models.CharField(max_length=20, blank=False, verbose_name='Участник №3')
    player4 = models.CharField(max_length=20, blank=False, verbose_name='Участник №4')
    working_status = models.BooleanField(default=False, verbose_name='В работе [СТАТУС]')
    completed_status = models.BooleanField(default=False, verbose_name='Завершено [СТАТУС]')
    approved_status = models.BooleanField(default=False, verbose_name='Одобрено [СТАТУС]')
    comment = models.TextField(blank=True, null=True, verbose_name='Комментарий')
    date = models.DateTimeField(auto_now=True, verbose_name='Дата регистрации заявки')

    def __str__(self):
        return self.team

    class Meta:
        verbose_name_plural = "Заявки [BEDWARS]"
