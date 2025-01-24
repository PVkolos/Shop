from django.test import TestCase

import requests

data = {'type': 'notification', 'event': 'payment.waiting_for_capture', 'object': {'id': '2ebd7e66-000f-5000-a000-158183b499d3', 'status': 'waiting_for_capture', 'amount': {'value': '3416.40', 'currency': 'RUB'}, 'description': 'Заказ super на сумму 3416.4 руб\n', 'recipient': {'account_id': '483836', 'gateway_id': '2346743'}, 'payment_method': {'type': 'bank_card', 'id': '2ebd7e66-000f-5000-a000-158183b499d3', 'saved': False, 'title': 'Bank card *4477', 'card': {'first6': '555555', 'last4': '4477', 'expiry_year': '2033', 'expiry_month': '09', 'card_type': 'MasterCard', 'card_product': {'code': 'E'}, 'issuer_country': 'US'}}, 'created_at': '2024-11-06T13:09:58.897Z', 'expires_at': '2024-11-13T13:11:33.471Z', 'test': True, 'paid': True, 'refundable': False, 'metadata': {'cms_name': 'yookassa_sdk_python'}, 'authorization_details': {'rrn': '422194155146241', 'auth_code': '315124'}}}

a = requests.post('https://upak-lab.ru/pay/success', data=data)

if a.status_code == 200:
  print("Сообщение успешно отправлено!")
else:
  print(f"Ошибка при отправке сообщения: {a.status_code} - {a.text}")