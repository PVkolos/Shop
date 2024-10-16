import os

from opensearchpy import OpenSearch, RequestError

#todo добавить логгирование


class Search:
    def __init__(self):
        host = 'localhost'
        port = 9200
        self.client = OpenSearch(
            hosts=[{"host": host, "port": port}],
            http_auth=("admin", "admin"),
            use_ssl=True,
            verify_certs=False,
            ssl_assert_hostname=False,
            ssl_show_warn=False,
        )
        self.client.info()

    def create_index(self, index_name):
        index_body = {
          'settings': {
            'index': {
              'number_of_shards': 4
            }
          }
        }
        try:
            self.client.indices.create(index_name, body=index_body)
        except RequestError as e:
            if 'already exists' in str(e):
                print(f"ERR: Индекс {index_name} уже существует.")


    def create_product(self, id, index, title, additional_info, category):
        document = {
          'title': title,
          'additional_info': additional_info,
          'category': category
        }
        answer = self.client.index(
            index = index,
            body = document,
            id = id,
            refresh = True
        )
        print(answer)

    def search_product(self, query: str, fields: list):
        query = {
            'size': 5,
            'query': {
                'multi_match': {
                    'query': query,
                    'fields': fields
                }
            }
        }
        answer = self.client.search(
            body=query,
            index='search_products'
        )
        print(answer)


client = Search()
client.create_index('search_products')


if __name__ == '__main__':
    client = Search()
    client.create_index('search_products')
    client.create_product(
        id=None,
        index='search_products',
        title='Пакет ПВД 45х45 "Розы Парижа" Альтпак /6уп х 50шт/',
        additional_info='Пакет ПВД 45х45 "Розы Парижа" Альтпак /6уп х 50шт/\nцена - 13.41 за штуку, понял????',
        category='Пакеты'
    )
    client.create_product(
        id=None,
        index='search_products',
        title='Банка 0,28л прозрачная квадратная /70х70х80/ Новосиб/50шт',
        additional_info='банку взял короче вообще, слыш?\nцена - 13.41 за штуку, понял????\nуступать не собираюсь!!!',
        category='банка'
    )
    client.create_product(
        id=None,
        index='search_products',
        title='Перец молотый в стиках порционный 0,25гр. (1000шт/кор.)/50шт',
        additional_info='перчика сыпани ка, булка/6уп х 50шт/\nцена - 13.41 за штуку, нети????',
        category='еда'
    )

    client.search_product('50шт', ['title', 'additional_info'])