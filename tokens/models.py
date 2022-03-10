from django.core.validators import MinLengthValidator
from django.db import models


class Token(models.Model):

    unique_hash = models.CharField(
        max_length=20,
        validators=[
            MinLengthValidator(20)
        ],
        verbose_name='Хэш токена'
    )
    tx_hash = models.CharField(
        max_length=100,
        verbose_name='Хэш транзакции создания токена'
    )
    media_url = models.URLField(
        verbose_name='URL изображения'
    )
    owner = models.TextField(
        max_length=100,
        verbose_name='Адрес владельца в сети Ethereum'
    )