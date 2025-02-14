from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.views import LoginView
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from .forms import RegisterUserForm, LoginUserForm
from django.contrib.auth import get_user_model
from payment.models import Orders
from users.models import Basket
from django.utils.html import mark_safe


menu = [{'title': "О сайте", 'url_name': 'about'},
        {'title': "Добавить статью", 'url_name': 'add_page'},
        {'title': "Обратная связь", 'url_name': 'contact'},
        {'title': "Войти", 'url_name': 'login'}
]


class DataMixin:
    def get_user_context(self, **kwargs):
        context = kwargs
        # cats = Category.objects.all()
        context['menu'] = menu
        # context['cats'] = cats
        if 'cat_selected' not in context:
            context['cat_selected'] = 0
        return context


class RegisterUser(DataMixin, CreateView):
    form_class = RegisterUserForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        all_quantity = len(list(Basket.objects.filter(username=self.request.user.username)))
        c_def = self.get_user_context(title="Регистрация", all_q=all_quantity, active_b='private')
        return dict(list(context.items()) + list(c_def.items()))

    # def form_invalid(self, form):
    #     print(form.errors)
    #     return redirect('register')

    def form_valid(self, form):
        email = form.cleaned_data.get('email')
        if get_user_model().objects.filter(email=email).exists():
            form.add_error('email', 'Такая почта уже зарегистрирована. Выберете другую почту или войдите в существующий аккаунт.')
            return render(self.request, 'users/register.html', {'form': form, 'all_q': len(list(Basket.objects.filter(username=self.request.user.username))), 'active_b': 'private'})
        else:
            user = form.save()
            login(self.request, user)
            return redirect('private')


class LoginUser(DataMixin, LoginView):
    form_class = LoginUserForm
    template_name = 'users/login.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        all_quantity = len(list(Basket.objects.filter(username=self.request.user.username)))
        c_def = self.get_user_context(title="Авторизация", all_q=all_quantity, active_b='private')
        return dict(list(context.items()) + list(c_def.items()))

    # def form_invalid(self, form):
    #     from django.contrib import messages
    #     # Отображение пользовательского сообщения об ошибке
    #     messages.error(self.request, "Неверное имя пользователя или пароль.")
    #     return super().form_invalid(form)

    def get_success_url(self):
        return reverse_lazy('home')


def private_office(request):
    all_quantity = len(list(Basket.objects.filter(username=request.user.username)))
    return render(request, 'users/private_office.html', {'all_q': all_quantity, 'active_b': 'private'})


def orders(request):
    orders_ = Orders.objects.filter(status=1, phone=request.user.username)
    for order in orders_:
        try:
            desc = order.description
            desc_ = ''
            for i in range(len(desc)):
                if desc[i] + desc[i + 1] == 'ID':
                    desc_ += str(i + 1) + ') '
                desc_ += desc[i]
            order.description = mark_safe(desc_)
            # print(desc.split('\n'))
            # desc = desc.split('\n')[1:]
            # order.description = '\n'.join(desc)
            # order.price = order.description.split('\n')[0].split('сумму ')[1]
            # order.description = '\n'.join(order.description.split('\n')[1:])
        except Exception as e:
            pass
    all_quantity = len(list(Basket.objects.filter(username=request.user.username)))
    return render(request, 'users/orders.html', {'all_q': all_quantity, 'active_b': 'private', 'orders': orders_[::-1]})