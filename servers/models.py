import datetime
import os
import uuid
from django.db import models
from django.contrib.auth.models import User


class Colors(models.Model):
    title = models.TextField(max_length=15, verbose_name='Цвет')
    shadow = models.TextField(verbose_name='Тень')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = "Раскраски"


class Tags(models.Model):
    title = models.TextField()
    icon = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = "Атрибуты"


def rename_banner(instance, filename):
    upload_to = 'posters/'
    ext = filename.split('.')[-1]
    filename = '{}.{}'.format(str(uuid.uuid4()), ext)

    return os.path.join(upload_to, filename)


class Banners(models.Model):
    title = models.CharField(max_length=200)
    image = models.ImageField(upload_to=rename_banner)
    date = models.DateTimeField(auto_now_add=True, blank=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = "Баннеры"


def rename_illustration(instance, filename):
    upload_to = 'illustrations/'
    ext = filename.split('.')[-1]
    filename = '{}.{}'.format(str(uuid.uuid4()), ext)

    return os.path.join(upload_to, filename)


class Illustrations(models.Model):
    title = models.CharField(max_length=200)
    image = models.ImageField(upload_to=rename_illustration)
    date = models.DateTimeField(auto_now_add=True, blank=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = "Иллюстрации"


class Servers(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Владелец')
    name = models.CharField(max_length=50, blank=False, verbose_name='Название')
    description = models.TextField(max_length=1600, blank=True, verbose_name='Описание')
    ip = models.CharField(max_length=36, blank=False, verbose_name='Адрес')
    port = models.CharField(default='25565', max_length=5, blank=False, verbose_name='Порт')
    icon = models.ForeignKey(Banners, on_delete=models.CASCADE, default=1, verbose_name='Картинка')
    illustrations = models.ManyToManyField(Illustrations, null=True, blank=True, verbose_name='Иллюстрации')
    mode = models.CharField(max_length=30, choices=[('VANILLA', 'Ванилла'), ('ANARCHY', 'Анархия'), ('MMORPG', 'MMO-RPG'), ('MINIGAMES', 'Мини-игры'), ('ADVENTURE', 'Приключение'), ('CONSTRUCTION', 'Строительство')], verbose_name='Режим', default="VANILLA")
    version = models.CharField(max_length=10, choices=[('1.7', '1.7.X'), ('1.8', '1.8.X'), ('1.9', '1.9.X'), ('1.10', '1.10.X'), ('1.11', '1.11.X'), ('1.12', '1.12.X'), ('1.13', '1.13.X'), ('1.14', '1.14.X'), ('1.15', '1.15.X'), ('1.16', '1.16.X'), ('1.17', '1.17.X'), ('1.18', '1.18.X'), ('1.19', '1.19.X')], default="1.19", verbose_name='Версия')
    license = models.BooleanField(default=False, verbose_name='Лицензия')
    launcher = models.BooleanField(default=False, verbose_name='Лаунчер')
    website = models.URLField(max_length=60, blank=True, verbose_name='Сайт')
    premium_status = models.BooleanField(default=False, verbose_name='Премиум-статус')
    premium_regdate = models.DateTimeField(verbose_name='Дата регистрации премиум-статуса', null=False, default=datetime.datetime.today())
    premium_color = models.ForeignKey(Colors, on_delete=models.CASCADE, verbose_name='Премиум-раскраска', default=1)
    boost_status = models.BooleanField(default=False, verbose_name='CloudBoost-статус')
    boost_regdate = models.DateTimeField(verbose_name='Дата регистрации CloudBoost-статуса', null=False, default=datetime.datetime.today())
    online_status = models.BooleanField(default=False, verbose_name='Статус')
    current_players = models.IntegerField(default=0, verbose_name='Игроки (Онлайн)')
    max_players = models.IntegerField(default=20, verbose_name='Игроки (Макс.)')
    description_rate_add = models.BooleanField(default=False, verbose_name='Рейтинг за описание')
    banner_rate_add = models.BooleanField(default=False, verbose_name='Рейтинг за баннер')
    illustrations_rate_add = models.BooleanField(default=False, verbose_name='Рейтинг за иллюстрации')
    premium_rate_add = models.BooleanField(default=False, verbose_name='Рейтинг за премиум')
    boost_rate_add = models.BooleanField(default=False, verbose_name='Рейтинг за Boost')
    online_rate_add = models.BooleanField(default=False, verbose_name='Рейтинг за онлайн')
    activity_rate_add = models.BooleanField(default=False, verbose_name='Рейтинг за 5+ игроков')
    popularity_rate_add = models.BooleanField(default=False, verbose_name='Рейтинг за 50+ игроков')
    superiority_rate_add = models.BooleanField(default=False, verbose_name='Рейтинг за 500+ игроков')
    verification_rate_add = models.BooleanField(default=False, verbose_name='Рейтинг верификацию')
    rate = models.IntegerField(default=10, verbose_name='Рейтинг')
    rate_old = models.IntegerField(default=0, verbose_name='Рейтинг (Старый)')
    attributes = models.ManyToManyField(Tags, null=True)
    verification = models.BooleanField(default=False, verbose_name='Верификация')
    block = models.BooleanField(default=False, verbose_name='Блокировка')
    date = models.DateTimeField(auto_now=True, verbose_name='Дата регистрации сервера')

    def __str__(self):
        return self.name

    def players(self):
        return self.current_players

    def premium(self):
        return self.premium_status

    def online(self):
        return self.online_status

    class Meta:
        verbose_name_plural = "Серверы"