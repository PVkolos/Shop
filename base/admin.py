from django.contrib import admin

from users.models import Basket


class BasketAdmin(admin.ModelAdmin):
    list_display = ('username', 'id_product', 'quantity')
    search_fields = ("username",)


admin.site.register(Basket, BasketAdmin)