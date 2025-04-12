from django.shortcuts import render, redirect
from users.models import Basket
from .models import Products, Categories
from collections import defaultdict


def news_home(request):
    get_categories_from_admin()
    products = Products.objects.all()
    all_quantity = len(list(Basket.objects.filter(username=request.user.username)))
    return render(request, 'news/news_home.html', {'all_q': all_quantity, 'products': products, 'categories': get_categories()})


def get_categories():
    categories = Categories.objects.all()
    category_dct = dict()
    for elements in categories:
        category_dct[elements.parent_category] = category_dct.get(elements.parent_category, []) + [elements]

    return category_dct


def get_categories_from_admin():
    categories_tuple = [
        ("Новинки 2025", "Новинки 2025"),
        ("Автохимия и автокосметика", "Автохимия и автокосметика"),
        ("Новинки от Grass", "Новинки от Grass"),
        ("Уцененные товары", "Уцененные товары")
    ]

    category_dct = dict()
    for elements in Categories.objects.all():
        if elements.parent_category not in ["Новинки 2025", "Автохимия и автокосметика", "Новинки от Grass",
                                            "Уцененные товары"]:
            category_dct[elements.parent_category] = category_dct.get(elements.parent_category, []) + [elements]

    for categories in category_dct.values():
        for category in categories:
            categories_tuple.append((category, category))
    return tuple(categories_tuple)


def add_product(request):
    if request.method == 'POST' and 'image' in request.FILES:
        # Получаем данные из POST-запроса
        title = request.POST['title']
        price = request.POST['price']
        additional_info = request.POST['additional_info']
        image = request.FILES['image']
        category = request.POST.getlist('category')
        quantity = request.POST['quantity']

        category = "-=-".join(category)

        if image.name.split('.')[-1] in ['jpg', 'jpeg', 'png']:
            product = Products(title=title, price=price, additional_info=additional_info, image='images/' + image.name, category=category, quantity=quantity)
            product.save()

            image_name = image.name
            # with open('images/media/' + image_name, 'wb+') as destination:
            with open('media/images/' + image_name, 'wb+') as destination:
                for chunk in image.chunks():
                    destination.write(chunk)

            return redirect('assortment')

    return redirect('home')


