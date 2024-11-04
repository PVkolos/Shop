from django.http import JsonResponse
from django.shortcuts import render, redirect
import json

from yookassa import Configuration
from yookassa import Payment
import uuid
from payment.models import Orders
from django.conf import settings

Configuration.account_id = int # todo
Configuration.secret_key = '' # todo
idempotence_key = str(uuid.uuid4())
SUCCESS_URL = settings.SUCCESS_URL
# SUCCESS_URL = 'www.google.com'


def success(request):
    if request.method == 'POST':
        req_data = request.get_json()
        status = req_data['object']['status']
        # print(req_data['object']['status'])
        if status == 'waiting_for_capture':
            # Подтверждение платежа
            Payment.capture(
                req_data['object']['id'],
                idempotence_key
            )
            order = Orders.objects.get(id_yk=req_data['object']['id'])
            order.status = 1
            order.save()
        # проверить статус платежа, если ожидает подтв, то подтв и проверяем еще раз
    return render(request, 'payment/success.html')


def create_link(username, price):
    idempotence_key = str(uuid.uuid4())
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
        "description": f"Заказ {username} на сумму {price} руб"
    }, idempotence_key)

    # get confirmation url
    confirmation_url = payment.confirmation.confirmation_url
    return confirmation_url


def create_payment(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        link = create_link(data['username'], str(data['summa']).replace(',', '.'))
        order_id = link.split('orderId=')[1]
        response_data = {
            'link': link
        }

        # Добавление ордера в БД
        order = Orders(phone=data['username'], name=data['name'], summ=str(data['summa']).replace(',', '.'), id_yk=order_id)
        order.save()

        return JsonResponse(response_data)

