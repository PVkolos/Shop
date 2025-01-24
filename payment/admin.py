from django.contrib import admin

# Register your models here.

from payment.models import Orders


class OrdersAdmin(admin.ModelAdmin):
    list_display = ('phone', 'name', 'date', 'summ', 'status', 'index')


admin.site.register(Orders, OrdersAdmin)
