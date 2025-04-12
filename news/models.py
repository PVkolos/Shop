from django.db import models
# from shop.search import client

from users.models import Basket


class Categories(models.Model):
    parent_category = models.CharField('Категория', max_length=300)
    category = models.CharField('Подкатегория', max_length=300)
    image = models.CharField('Класс изображения', null=True, max_length=200)

    def __str__(self):
        return self.category

    @staticmethod
    def get_all_categories():
        categories = Categories.objects.all()
        category_choices = [(category.parent_category, category.category) for category in categories]
        return category_choices

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Products(models.Model):
    title = models.CharField('Название товара', max_length=300)
    price = models.FloatField('Цена товара')
    additional_info = models.TextField('Описание товара')
    image = models.ImageField('Картинка', upload_to='images')
    quantity = models.IntegerField('Штук в наличии')
    category = models.CharField('Категория', max_length=100)

    def __str__(self):
        return self.title

    # def save(self, *args, **kwargs):
    #     self.category = '-=-'.join(self.category)
    #     print(self.title, self.price, self.additional_info, self.image, self.quantity, self.category)
    #     super().save(*args, **kwargs)

        # Добавление товара в opensearch
        # try:
            # client.create_product(
            #     id=self.id,
            #     index='search_products',
            #     title=self.title,
            #     additional_info=self.additional_info,
            #     category=self.category
            # )
        #     print("SUCCESS ADDED PRODUCT")
        # except Exception as e:
        #     print("ERR Add.news.models.48", e)

    def delete(self, *args, **kwargs):
        # Удаление товара из opensearch
        try:
            # client.delete_product(
            #     index='search_products',
            #     id=self.id
            # )
            print("SUCCESS DELETED PRODUCT")
        except Exception as e:
            print("ERR Delete.news.models.59: ", e)

        Basket.objects.filter(id_product=self.id).delete()

        super().delete(*args, **kwargs)

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

