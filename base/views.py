from pprint import pprint
from re import search

from django.shortcuts import render, redirect
from news.models import Products
from unicodedata import category
from users.models import Basket
from django.http import JsonResponse
import json
from .forms import OrderForm
import requests
from shop.search import client
# import pymorphy2


def index(request):
    return render(request, 'base/index.html', {'active_b': 'index'})


def about(request):
    return render(request, 'base/about.html', {'active_b': 'about'})


def search_on(request, query):
    response = client.search_product(query, ['title', 'additional_info', 'category'])
    # pprint(response)
    ids = []
    products = []
    products_itog = []
    for product in response['hits']['hits']:
        if product['_id'].isdigit():
            ids.append([int(product['_id']), product['_score']])
            products.append(Products.objects.get(id=int(product['_id'])))

    return render(request, 'base/assortment.html', {'products': products, 'flag': 'true', 'products_itog': products_itog, 'active_b': 'assortment'})


def assortment(request):
    request.session['button_active'] = 'assortment'
    if 'search' in request.GET:
        query = request.GET['search']
        category = f'Результат запроса: "{query}"'
        products = []
        products_all = []
        response = client.search_few_products(request.GET.get('search').split(), ['title', 'additional_info', 'category'])
        flag = 'true'
        for product in response:
            products_all.append(Products.objects.get(id=int(product[0])))
            products.append(Products.objects.get(id=int(product[0])))

    else:
        category = request.GET.get("category", "Все товары")
        products_all = Products.objects.all()
        products = []
        for product in products_all:
            if product.category == category or category == 'Все товары':
                products.append(product)
        flag = 'false'

    products_ = list(Basket.objects.filter(username=request.user.username))
    products_itog = []  # id товаров из корзины
    for el in products_: # Перебираем все продукты из корзины пользователя
        product_user = Products.objects.get(id=el.id_product) # Достаем данные о товаре из общей таблицы
        products_itog.append(product_user.id)
    for el in products_all:
        if el.id in products_itog:
            item = Basket.objects.filter(id_product=el.id, username=request.user.username)[0]
            el.quantity_basket = item.quantity
        else:
            el.quantity_basket = 0
    print(1111, products, products_itog, category)
    return render(request, 'base/assortment.html', {'flag': flag, 'products': products, 'category': category, 'products_itog': products_itog, 'active_b': 'assortment'})


def contacts(request):
    return render(request, 'base/contacts.html', {'active_b': 'contacts'})


def basket(request):
    products = list(Basket.objects.filter(username=request.user.username))
    products_itog = []
    products_id = []
    for el in products: # Перебираем все продукты из корзины пользователя
        product_user = Products.objects.get(id=el.id_product) # Достаем данные о товаре из общей таблицы
        product_user.quantity_basket = el.quantity
        products_itog.append(product_user)
        products_id.append(product_user.id)
    # if not products_itog: products_itog = None
    return render(request, 'base/basket.html',
                  {'products_id': products_id, 'products': products_itog, 'active_b': 'basket',
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
            user = request.user.username
            if not Basket.objects.filter(username=user, id_product=id_).exists():
                product = Basket.objects.create(id_product=id_, username=user)
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
            data = json.loads(request.body)
            product_id = data.get('product_id')
            quantity = data.get('quantity')

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

