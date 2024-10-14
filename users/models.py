from django.db import models


class Basket(models.Model):
    id_product = models.IntegerField('ID товара')
    username = models.CharField('Юзернейм пользователя', max_length=200)
    quantity = models.IntegerField('Количество', default='1')

    class Meta:
        verbose_name = 'Корзина'
        verbose_name_plural = 'Корзины'
