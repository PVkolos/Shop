from django.db import models


class Products(models.Model):
    title = models.CharField('Название товара', max_length=200)
    price = models.FloatField('Цена товара')
    additional_info = models.TextField('Описание товара')
    image = models.ImageField('Картинка', upload_to='images')
    # photo_products = models.CharField('Название картинки', max_length=150, unique=True)
    THEME_CHOICES = (
        ('Пакеты', 'Пакеты'),
        ('Пластиковая одноразовая посуда', 'Пластиковая одноразовая посуда'),
        ('Бумажная одноразовая посуда', 'Бумажная одноразовая посуда'),
        ('Пластиковая упаковка', 'Пластиковая упаковка'),
        ('Бумажная упаковка', 'Бумажная упаковка'),
        ('Ланч боксы и лотки', 'Ланч боксы и лотки'),
        ('Пленка и скотч', 'Пленка и скотч'),
        ('Товары хоз назначения', 'Товары хоз назначения'),
        ('Монтажные летны', 'Монтажные летны'),
        ('Сезонные товары', 'Сезонные товары'),
        ('Продукты питания', 'Продукты питания'),
        ('Бытовая химия', 'Бытовая химия'),
        ('Подарочная упаковка', 'Подарочная упаковка'),
        ('Новогодняя продукция', 'Новогодняя продукция'),
        ('Канцелярские товары', 'Канцелярские товары'),
    )
    category = models.CharField('Категория', max_length=100, choices=THEME_CHOICES)
    quantity = models.IntegerField('Штук в наличии')

    def __str__(self):
        return self.title

    # def save(self, *args, **kwargs):
    #     super().save(*args, **kwargs)
    #     es = Elasticsearch()
    #     es.index(index='products', id=self.id, body={
    #         'name': self.name,
    #         'description': self.description,
    #         'price': self.price
    #     })

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'


# class Reviews(models.Model):
#     stars = models.IntegerField('Количество звезд')
#     name_user = models.CharField('Имя человека', max_length=100)
#     date = models.DateTimeField('Дата и время создания отзыва')
#     text = models.TextField('Текст отзыва', max_length=500)
#     photo = models.CharField('Название картинки', max_length=150)
#
#     def __str__(self):
#         return self.text
#
#     class Meta:
#         verbose_name = 'Отзыв'
#         verbose_name_plural = 'Отзывы'