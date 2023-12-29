from django.db import models
from django.contrib.auth.models import User


class ServersBuffer(models.Model):
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    server_ip = models.TextField(max_length=36, blank=False, verbose_name='Адрес')
    server_port = models.TextField(default='25565', max_length=5, blank=False, verbose_name='Порт')
    name = models.TextField(max_length=50, blank=False, verbose_name='Название')
    published = models.BooleanField(default=False)
    date = models.DateTimeField(auto_now_add=True, blank=True, null=False)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Серверы на проверке"

