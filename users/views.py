from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.views import LoginView
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from .forms import RegisterUserForm
from django.contrib.auth import get_user_model


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
        c_def = self.get_user_context(title="Регистрация")
        return dict(list(context.items()) + list(c_def.items()))

    # def form_invalid(self, form):
    #     print(form.errors)
    #     return redirect('register')

    def form_valid(self, form):
        email = form.cleaned_data.get('email')
        if get_user_model().objects.filter(email=email).exists():
            form.add_error('email', 'Такая почта уже зарегистрирована. Выберете другую почту или войдите в существующий аккаунт.')
            return render(self.request, 'users/register.html', {'form': form})
        else:
            user = form.save()
            login(self.request, user)
            return redirect('register')


class LoginUser(DataMixin, LoginView):
    form_class = AuthenticationForm
    template_name = 'users/login.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Авторизация")
        return dict(list(context.items()) + list(c_def.items()))

    def get_success_url(self):
        return reverse_lazy('home')


def private_office(request):
    return render(request, 'users/private_office.html', {'active_b': 'private'})
