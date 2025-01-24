from datetime import datetime

from django.db import models


class Orders(models.Model):
    phone = models.CharField('Номер телефона', max_length=20)
    name = models.CharField('Имя пользователя', max_length=20)
    date = models.DateField('Дата', default=datetime.now)
    summ = models.FloatField('Сумма заказа', default=0)
    status = models.IntegerField('Статус оплаты', default=0)
    id_yk = models.CharField('ID из Yookassa', max_length=100, default='')
    description = models.CharField('Детали заказа', max_length=10000, default='')
    index = models.CharField('Почтовый индекс', max_length=20, default='')

    class Meta:
        verbose_name = 'Ордер'
        verbose_name_plural = 'Ордера'

    def __str__(self):
        return self.phone


'''
таблица для хранения транзакций, ордеров
id, phone, name, status
'''
