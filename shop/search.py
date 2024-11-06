from opensearchpy import OpenSearch, RequestError
import pymorphy2
import operator


#todo добавить логгирование


class SingletonMeta(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]


class Search(metaclass=SingletonMeta):
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
        response = self.client.index(
            index = index,
            body = document,
            id = id,
            refresh = True
        )
        print(response)


    def delete_product(self, index, id):
        response = self.client.delete(
            index=index,
            id=id
        )
        print(response)


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
        response = self.client.search(
            body=query,
            index='search_products'
        )
        return response

    def search_few_products(self, query: list, fields: list):
        query_norm = [el for el in query]
        try:
            for word in query:
                for el in morph.parse(word):
                    query_norm.append(el.normal_form)
                    query_norm.append(el.inflect({'gent'}).word) # Родительный
                    query_norm.append(el.inflect({'plur', 'gent'}).word)
                    query_norm.append(el.inflect({'datv'}).word) # Дательный
                    query_norm.append(el.inflect({'plur', 'datv'}).word)
                    query_norm.append(el.inflect({'accs'}).word) # Винительный
                    query_norm.append(el.inflect({'plur', 'accs'}).word)
                    query_norm.append(el.inflect({'ablt'}).word) # Творительный
                    query_norm.append(el.inflect({'plur', 'ablt'}).word)
                    query_norm.append(el.inflect({'loct'}).word) # Предложный
                    query_norm.append(el.inflect({'plur', 'loct'}).word)

            query_norm = set(query_norm)
        except Exception as e:
            print('Слово не склоняется', e)

        ids = []
        ids_lib = dict()
        for product in query_norm:
            query = {
                'size': 5,
                'query': {
                    'multi_match': {
                        'query': product,
                        'fields': fields
                    }
                }
            }
            response = self.client.search(
                body=query,
                index='search_products'
            )
            for element in response['hits']['hits']:
                if element['_id'].isdigit():
                    ids.append([int(element['_id']), element['_score']])
                    ids_lib[int(element['_id'])] = ids_lib.get(int(element['_id']), 0) + 1

                # ids_lib = sorted(ids_lib, key=lambda x: x[1], reverse=True)

                # if element['_id'].isdigit() and int(element['_id']) not in [el[0] for el in ids]:
                #     ids.append([int(element['_id']), element['_score']])
        ids_lib = sorted(ids_lib.items(), key=operator.itemgetter(1), reverse=True)
        return ids_lib


client = Search()
morph = pymorphy2.MorphAnalyzer()

if __name__ == '__main__':
    client = Search()
    # client.create_index('search_products')
    # client.create_product(
    #     id=None,
    #     index='search_products',
    #     title='Пакет ПВД 45х45 "Розы Парижа" Альтпак /6уп х 50шт/',
    #     additional_info='Пакет ПВД 45х45 "Розы Парижа" Альтпак /6уп х 50шт/\nцена - 13.41 за штуку, понял????',
    #     category='Пакеты'
    # )
    # client.create_product(
    #     id=None,
    #     index='search_products',
    #     title='Банка 0,28л прозрачная квадратная /70х70х80/ Новосиб/50шт',
    #     additional_info='банку взял короче вообще, слыш?\nцена - 13.41 за штуку, понял????\nуступать не собираюсь!!!',
    #     category='банка'
    # )
    # client.create_product(
    #     id=None,
    #     index='search_products',
    #     title='Перец молотый в стиках порционный 0,25гр. (1000шт/кор.)/50шт',
    #     additional_info='перчика сыпани ка, булка/6уп х 50шт/\nцена - 13.41 за штуку, нети????',
    #     category='еда'
    # )

    # print(client.search_product('ошибке', ['title', 'additional_info']))
    print(client.search_few_products(['пакет', 'ошибка'], ['title', 'additional_info', 'category']))