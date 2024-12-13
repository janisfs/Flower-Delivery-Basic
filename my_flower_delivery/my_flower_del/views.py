from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect
from .forms import RegisterForm
from .forms import LoginForm, RegisterForm
from django.contrib.auth import authenticate, login as auth_login

# Create your views here.
def index(request):
    return render(request, 'my_flower_del/index.html')


def login(request):
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        print("Попытка входа")
        print(f"Полученные данные: username={request.POST.get('username')}")  # НЕ выводите пароль в логи!
        if form.is_valid():
            print("Форма валидна")
            user = form.get_user()
            auth_login(request, user)
            print(f"Пользователь {user.username} успешно залогинен")
            return redirect('index')
        else:
            print("Ошибки формы:", form.errors)
    else:
        form = LoginForm()

    return render(request, 'my_flower_del/login.html', {'form': form})


def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            print(f"Создан новый пользователь: {user.username}")
            # Автоматически входим после регистрации
            auth_login(request, user)
            return redirect('index')
    else:
        form = RegisterForm()
    return render(request, 'my_flower_del/register.html', {'form': form})