from .models import Products, Categories
# from shop.search import client
from django.contrib import admin

from users.models import Basket

from .forms import ProductsAdminForm


class ProductsAdmin(admin.ModelAdmin):
    form = ProductsAdminForm
    list_display = ('title', 'quantity', 'price')

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

    def save_model(self, request, obj, form, change):
        obj.category = form.cleaned_data['category']  # Сохраняем категории в нужном формате
        super().save_model(request, obj, form, change)


class CategoriesAdmin(admin.ModelAdmin):
    list_display = ('category', 'parent_category')
    list_filter = ('parent_category', )
    search_fields = ("category",)

    # class Meta:
    #     ordering = ("parent_category", "category")


admin.site.register(Products, ProductsAdmin)
admin.site.register(Categories, CategoriesAdmin)

# admin.site.register(Products)
# admin.site.register(Reviews)
