from django.shortcuts import render, redirect
from .models import Products
from shop.search import client


def news_home(request):
    products = Products.objects.all()
    return render(request, 'news/news_home.html', {'products': products})


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
            client.create_product(
                id=product.id,
                index='search_products',
                title=title,
                additional_info=additional_info,
                category=category
            )

            image_name = image.name
            with open('media/images/' + image_name, 'wb+') as destination:
                for chunk in image.chunks():
                    destination.write(chunk)

            return redirect('assortment')  # Замените 'home' на имя вашего URL-шаблона

    return redirect('home')  # Отображаем шаблон HTML для добавления товара
