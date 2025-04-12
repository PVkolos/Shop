from django.shortcuts import render, redirect
from news.models import Products, Categories
from phonenumbers.unicode_util import Category
from users.models import Basket
from django.http import JsonResponse
import json
from shop.regexp import search_strings
from django.db.models import Q


def index(request):
    all_quantity = len(list(Basket.objects.filter(username=request.user.username)))
    return render(request, 'base/index.html', {'all_q': all_quantity, 'active_b': 'index'})


def about(request):
    all_quantity = len(list(Basket.objects.filter(username=request.user.username)))
    return render(request, 'base/about.html', {'all_q': all_quantity, 'active_b': 'about'})


# def search_on(request, query):
#     response = client.search_product(query, ['title', 'additional_info', 'category'])
#     # pprint(response)
#     ids = []
#     products = []
#     products_itog = []
#     for product in response['hits']['hits']:
#         if product['_id'].isdigit():
#             ids.append([int(product['_id']), product['_score']])
#             products.append(Products.objects.get(id=int(product['_id'])))
#
#     return render(request, 'base/assortment.html', {'products': products, 'flag': 'true', 'products_itog': products_itog, 'active_b': 'assortment'})


def get_categories():
    categories = Categories.objects.all()
    category_dct = dict()
    for elements in categories:
        category_dct[elements.parent_category] = category_dct.get(elements.parent_category, {'image': elements.image, 'categories_list': []})
        if isinstance(category_dct[elements.parent_category], dict):
            category_dct[elements.parent_category]['categories_list'].append(elements)

    return category_dct


def assortment(request):
    request.session['button_active'] = 'assortment'
    if 'search' in request.GET:
        query = request.GET['search']
        category = f'Результат запроса: "{query}"'
        base = Products.objects.filter(~Q(quantity=0))
        response = search_strings(request.GET.get('search').split(), ['title', 'additional_info', 'category'], base)
        flag = 'true'
        products = response.copy()
        products_all = response.copy()
    else:
        category = request.GET.get("category", "Новинки 2025")
        products_all = Products.objects.all()
        products = []
        for product in products_all:
            if (category.strip() in product.category.split("-=-")) or category == 'Все товары':
                products.append(product)
        flag = 'false'

    products_ = list(Basket.objects.filter(username=request.user.username))
    products_itog = []  # id товаров из корзины

    for el in products_: # Перебираем все продукты из корзины пользователя
        try:
            product_user = Products.objects.get(id=el.id_product) # Достаем данные о товаре из общей таблицы
            products_itog.append(product_user.id)
        except Exception as e:
            if 'not exist' in str(e):
                user = request.user.username
                if Basket.objects.filter(username=user, id_product=el.id_product).exists():
                    Basket.objects.filter(id_product=el.id_product, username=user).delete()
                print("ERR: views.py assortment. Вероятно, товар быд удален")
    all_quantity = len(products_itog)
    for el in products_all:
        if el.id in products_itog:
            item = Basket.objects.filter(id_product=el.id, username=request.user.username)[0]
            el.quantity_basket = item.quantity
            # all_quantity += item.quantity
        else:
            el.quantity_basket = 0
    return render(request, 'base/as3.html', {'all_q': all_quantity, 'flag': flag, 'products': products, 'category': category, 'products_itog': products_itog, 'categories': get_categories(),'active_b': 'assortment'})


def contacts(request):
    all_quantity = len(list(Basket.objects.filter(username=request.user.username)))
    return render(request, 'base/contacts.html', {'all_q': all_quantity, 'active_b': 'contacts'})


def basket(request):
    products = list(Basket.objects.filter(username=request.user.username))
    products_itog = []
    products_id = []
    for el in products: # Перебираем все продукты из корзины пользователя
        try:
            product_user = Products.objects.get(id=el.id_product) # Достаем данные о товаре из общей таблицы
            product_user.quantity_basket = el.quantity
            products_itog.append(product_user)
            products_id.append(product_user.id)
        except Exception as e:
            if 'not exist' in str(e):
                user = request.user.username
                if Basket.objects.filter(username=user, id_product=el.id_product).exists():
                    Basket.objects.filter(id_product=el.id_product, username=user).delete()
                print("ERR: views.py assortment. Вероятно, товар быд удален")
    # if not products_itog: products_itog = None
    all_quantity = len(products_itog)
    return render(request, 'base/basket.html',
                  {'all_q': all_quantity, 'products_id': products_id, 'products': products_itog, 'active_b': 'basket',
                   'number': sum([el.quantity_basket for el in products_itog]), 'summa': round(sum(el.price * el.quantity_basket for el in products_itog), 2)})


def add_product(request):
    if request.method == 'POST' and 'image' in request.FILES:
        # Получаем данные из POST-запроса
        title = request.POST['title']
        price = request.POST['price']
        additional_info = request.POST['additional_info']
        image = request.FILES['image']
        category = request.POST['category']
        quantity = request.POST['quantity']

        if image.name.split('.')[-1] in ['jpg', 'jpeg', 'png']:
            product = Products(title=title, price=price, additional_info=additional_info, image='images/' + image.name, category=category, quantity=quantity)
            product.save()

            image_name = image.name
            with open('media/images/' + image_name, 'wb+') as destination:
                for chunk in image.chunks():
                    destination.write(chunk)

            return redirect('assortment')

    return redirect('home')  # Отображаем шаблон HTML для добавления товара


def add_to_cart(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            id_ = data.get('product_id')
            quantity_ = data.get('quantity')
            user = request.user.username
            if not Basket.objects.filter(username=user, id_product=id_).exists():
                product = Basket.objects.create(id_product=id_, username=user, quantity=quantity_)
                product.save()
            return JsonResponse({'sucsess': 'true'})
        except json.JSONDecodeError:
            # Обработка ошибки неверного формата JSON
            pass


def delete_to_cart(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            id_ = data.get('product_id')
            user = request.user.username
            if Basket.objects.filter(username=user, id_product=id_).exists():
                Basket.objects.filter(id_product=id_, username=user).delete()
            return JsonResponse({'sucsess': 'true'})
        except json.JSONDecodeError:
            # Обработка ошибки неверного формата JSON
            pass


def delete_to_cart_basket(request):
    id_ = request.GET.get("id", 1)
    user = request.user.username
    if Basket.objects.filter(username=user, id_product=id_).exists():
        Basket.objects.filter(id_product=id_, username=user).delete()
    return redirect('basket')


def success(request):
    return render(request, 'main/success.html')


def update_cart(request):
    if request.method == 'POST':
        try:
            if not request.user.is_authenticated:
                # return redirect('login')
                pass
            else:
                data = json.loads(request.body)
                product_id = data.get('product_id')
                quantity = data.get('quantity')
                # print(product_id, quantity)

                user = request.user.username
                product_basket = Basket.objects.filter(username=user, id_product=product_id)[0]
                product_basket.quantity = quantity
                product_basket.save()

                product = Products.objects.get(id=product_id)
                product_price = round(float(product.price) * int(quantity), 2)

                # Возвращаем данные в формате JSON
                response_data = {
                    'product_price': product_price
                }
                return JsonResponse(response_data)

        except json.JSONDecodeError:
            # Обработка ошибки неверного формата JSON
            pass


def is_basket(request):
    if request.method == 'POST':
        try:
            # if not request.user.is_authenticated:
            #     return redirect('login')
            data = json.loads(request.body)
            product_id = data.get('product_id')
            user = request.user.username
            if Basket.objects.filter(username=user, id_product=product_id).exists():
                response_data = {
                    'is': 'true'
                }
            else:
                response_data = {
                    'is': 'false'
                }
            return JsonResponse(response_data)
        except Exception as e:
            print(e)


# def update_db_plus(request):
#     if request.method == 'POST':
#         try:
#             pass
#             # data = json.loads(request.body)
#             # product_id = data.get('product_id')
#             # quantity = data.get('quantity')
#             #
#             # product = Products.objects.get(id=product_id)
#             # product_price = float(product.price) * int(quantity)
#             #
#             # # Возвращаем данные в формате JSON
#             # response_data = {
#             #     'product_price': product_price
#             # }
#             # return JsonResponse(response_data)
#         except json.JSONDecodeError:
#             # Обработка ошибки неверного формата JSON
#             pass

