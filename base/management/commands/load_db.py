from django.core.management.base import BaseCommand, CommandError
from shop.search import Search


class Command(BaseCommand):
    help = 'load_db'

    def handle(self, *args, **kwargs):
        try:
            from news.models import Products
            client = Search()
            client.create_index('search_products')
            products = Products.objects.all()

            for product in products:
                client.create_product(
                    id=product.id,
                    index='search_products',
                    title=product.title,
                    additional_info=product.additional_info,
                    category=product.category
                )
                print(f"INFO: База данных выгружена в opensearch индекс {'search_products'}")
        except:
            raise CommandError('Initalization failed.')