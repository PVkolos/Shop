import requests
from django.http import JsonResponse
from django.shortcuts import render, redirect
import json
from users.models import Basket
from news.models import Products


from yookassa import Configuration
from yookassa import Payment
import uuid
from payment.models import Orders
from django.conf import settings

SUCCESS_URL = settings.SUCCESS_URL
BOT_ID = settings.BOT_ID
CHAT_ID = settings.CHAT_ID
SECRET_KEY_KASSA = settings.SECRET_KEY_KASSA
ACCOUNT_ID_KASSA = settings.ACCOUNT_ID_KASSA

Configuration.account_id = ACCOUNT_ID_KASSA
Configuration.secret_key = SECRET_KEY_KASSA
idempotence_key = str(uuid.uuid4())


def recalculation(description):
    for string in description.split('\n')[1:]:
        id_product = int(string.split('ID - ')[1].split('.')[0])
        quantity = int(string.split('КОЛИЧЕСТВО - ')[1].split(' шт')[0])

        product = Products.objects.get(id=id_product)
        product.quantity -= quantity
        product.save()



def success(request):
    if request.method == 'POST':
        # todo тест всей функции на хостинге
        req_data = request.get_json()
        status = req_data['object']['status']
        # print(req_data['object']['status'])
        if status == 'waiting_for_capture':
            # Подтверждение платежа
            Payment.capture(
                req_data['object']['id'],
                idempotence_key
            )

            # Обновление статуса платежа на "оплачен"
            order = Orders.objects.get(id_yk=req_data['object']['id'])
            order.status = 1
            order.save()

            # Уведомление владельца о поступившем заказе
            req = f"https://api.telegram.org/bot{BOT_ID}/sendMessage?chat_id={CHAT_ID}&text=" + order.description
            requests.get(req)

            # Перерасчет количества товара после покупки
            recalculation(order.description)

    return render(request, 'payment/success.html')


def create_link(username, price, description):
    payment = Payment.create({
        "amount": {
          "value": price,
          "currency": "RUB"
        },
        "payment_method_data": {
          "type": "bank_card"
        },
        "capture": False,
        "confirmation": {
          "type": "redirect",
          "return_url": SUCCESS_URL
        },
        "description": description
    }, idempotence_key)

    # get confirmation url
    confirmation_url = payment.confirmation.confirmation_url
    return confirmation_url


def create_payment(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        products = list(Basket.objects.filter(username=data['username']))
        description = f"Заказ {data['username']} на сумму {str(data['summa']).replace(',', '.')} руб\n"

        for el in products:
            product_user = Products.objects.get(id=el.id_product)
            product_user.quantity_basket = el.quantity

            # ПЕРЕМЕННАЯ НЕ ПОДЛЕЖИТ ИЗМЕНЕНИЮ, либо необходимо менять тело функции recalculation()
            description += f'ID - {product_user.id}. НАЗВАНИЕ - {product_user.title}. КОЛИЧЕСТВО - {el.quantity} шт. ЦЕНА - {product_user.price} руб. СУММА ЛОТА - {el.quantity * product_user.price} руб.\n'

        link = create_link(data['username'], str(data['summa']).replace(',', '.'), f"Заказ {data['username']} на сумму {str(data['summa']).replace(',', '.')} руб\n")
        order_id = link.split('orderId=')[1]
        response_data = {
            'link': link
        }

        # Добавление ордера в БД
        order = Orders(phone=data['username'], name=data['name'], summ=str(data['summa']).replace(',', '.'), id_yk=order_id, description=description)
        order.save()

        return JsonResponse(response_data)
