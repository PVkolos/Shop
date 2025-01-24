from django.contrib import admin

# Register your models here.
from users.models import Basket


class BasketAdmin(admin.ModelAdmin):
    list_display = ('username', 'id_product', 'quantity')


admin.site.register(Basket, BasketAdmin)