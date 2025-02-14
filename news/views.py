from django.shortcuts import render, redirect
from users.models import Basket
from .models import Products

def news_home(request):
    products = Products.objects.all()
    all_quantity = len(list(Basket.objects.filter(username=request.user.username)))
    return render(request, 'news/news_home.html', {'all_q': all_quantity, 'products': products})


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
            with open('media/images/' + image_name, 'wb+') as destination:
                for chunk in image.chunks():
                    destination.write(chunk)

            return redirect('assortment')

    return redirect('home')


