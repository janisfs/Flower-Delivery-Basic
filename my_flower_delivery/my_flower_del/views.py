from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect, get_object_or_404
from .forms import RegisterForm
from .forms import LoginForm, RegisterForm
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.decorators import login_required
from .models import Product, Order, OrderItem
from .forms import ShippingAddressForm



# Create your views here.
def index(request):
    products = Product.objects.all()  # Выбираем все товары, которые есть в базе данных
    # Вариант с фильтрацией по типу цветка
    # flower_type = request.GET.get('type')  # Получаем параметр фильтрации из URL
    # if flower_type:  # Если параметр есть, фильтруем товары
    #     products = Product.objects.filter(flower_type=flower_type)
    # else:  # Иначе показываем все товары
    #     products = Product.objects.all()

    return render(request, 'my_flower_del/index.html', {'products': products})


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


@login_required
def checkout(request):
    cart_items = request.session.get('cart', {})
    if not cart_items:
        return redirect('cart')  # Если корзина пуста

    order = Order.objects.create(user=request.user, status='pending', total_amount=0)

    total_amount = 0
    for product_id, quantity in cart_items.items():
        product = Product.objects.get(id=product_id)
        order_item = OrderItem.objects.create(order=order, product=product, quantity=quantity, price=product.price)
        total_amount += product.price * quantity

    order.total_amount = total_amount
    order.save()

    if request.method == 'POST':
        form = ShippingAddressForm(request.POST)
        if form.is_valid():
            shipping_address = form.save(commit=False)
            shipping_address.order = order
            shipping_address.save()
            return redirect('order_confirmation', order_id=order.id)
    else:
        form = ShippingAddressForm()

    return render(request, 'checkout.html', {'form': form, 'order': order})


def add_to_cart(request, product_id):
    cart = request.session.get('cart', {})
    cart[product_id] = cart.get(product_id, 0) + 1
    request.session['cart'] = cart
    return redirect('cart')



def order_confirmation(request, order_id):
    order = Order.objects.get(id=order_id, user=request.user)
    return render(request, 'my_flower_del/order_confirmation.html', {'order': order})


def catalog(request):
     products = Product.objects.all()  # Выбираем все товары
     return render(request, 'index.html', {'products': products})  # Используем шаблон index.html


def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug)  # Находим товар по slug
    return render(request, 'product_detail.html', {'product': product})
