from django.db import models
from django.contrib.auth.models import User


class Support(models.Model):
    name_user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Отправитель')
    name_from_user = models.TextField(blank=False, default='Anonimous')
    email = models.TextField(blank=False)
    text = models.TextField(blank=False)
    completed = models.BooleanField(default=False)

    def __str__(self):
        return self.email

    class Meta:
        verbose_name_plural = "Обращения"
