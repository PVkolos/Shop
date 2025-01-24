from .models import Products
# from shop.search import client
from django.contrib import admin

from users.models import Basket


class ProductsAdmin(admin.ModelAdmin):
    def delete_queryset(self, request, queryset):
        # Удаление товара из opensearch
        try:
            for _id in [int(el.id) for el in queryset]:
                # client.delete_product(
                #     index='search_products',
                #     id=_id
                # )
                Basket.objects.filter(id_product=_id).delete()
                print(f"SUCCESS DELETED PRODUCT {_id} ADMIN")
        except Exception as e:
            print("ERR Delete.news.admin.16: ", e)

        super().delete_queryset(request, queryset)


admin.site.register(Products, ProductsAdmin)

# admin.site.register(Products)
# admin.site.register(Reviews)
