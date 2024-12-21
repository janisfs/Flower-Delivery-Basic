# Create your views here.
from django.shortcuts import render, redirect, get_object_or_404
from .forms import LoginForm, RegisterForm
from django.contrib.auth import authenticate, login as auth_login, logout
from .models import Product, Order, OrderItem, Cart, CartItem, Comment
from .forms import ShippingAddressForm, AddToCartForm
from django.contrib.auth.decorators import login_required
from .forms import CommentForm
from django.http import JsonResponse
from django.contrib import messages


# Главная страница
def index(request):
    products = Product.objects.all()  # Выбираем все товары, которые есть в базе данных
    return render(request, 'my_flower_del/index.html', {'products': products})


# Вход в систему
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
            return redirect('my_flower_del:index')
        else:
            print("Ошибки формы:", form.errors)
    else:
        form = LoginForm()

    return render(request, 'my_flower_del/login.html', {'form': form})


# Вход в систему
def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('my_flower_del:index')  # Перенаправление после логина
        else:
            return render(request, 'registration/login.html', {'error': 'Неверный логин или пароль'})
    return render(request, 'registration/login.html')



# Выход из системы
def logout_view(request):
    logout(request)
    return redirect('my_flower_del:index')  # Перенаправление на главную страницу


# Регистрация
def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            print(f"Создан новый пользователь: {user.username}")
            # Проверяем статус пользователя
            print(f"Пользователь активен: {user.is_active}")
            # Автоматически входим после регистрации
            auth_login(request, user)
            return redirect('my_flower_del:login')
        else:
            # Логируем ошибки формы
            print("Ошибки формы регистрации:", form.errors)
    else:
        form = RegisterForm()
    return render(request, 'my_flower_del/register.html', {'form': form})


# Мой профиль
def account(request):
    user = request.user
    return render(request, 'my_flower_del/account.html')


# Корзина
@login_required
def checkout(request):
    if request.method == 'POST':
        try:
            # Получаем активный заказ пользователя
            order = Order.objects.filter(user=request.user, status='pending').latest('created_at')

            # Обновляем статус заказа
            order.status = 'paid'
            order.save()

            # Формируем более информативное сообщение
            success_message = (
                f'Заказ №{order.id} успешно оформлен! '
                f'Статус заказа: {order.get_status_display()}'
            )
            messages.success(request, success_message)

            return redirect('my_flower_del:index')

        except Order.DoesNotExist:
            messages.error(request, 'Заказ не найден')
            return redirect('my_flower_del:cart')

    return redirect('my_flower_del:cart')



# Добавление товара в корзину
@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    if request.method == 'POST':
        form = AddToCartForm(request.POST)
        if form.is_valid():
            quantity = form.cleaned_data['quantity']

            # Получаем или создаем корзину для пользователя
            cart, _ = Cart.objects.get_or_create(user=request.user)

            # Получаем или создаем элемент корзины
            cart_item, created = CartItem.objects.get_or_create(
                cart=cart,
                product=product,
                defaults={'quantity': quantity}
            )

            if not created:
                cart_item.quantity += quantity
                cart_item.save()

            # Возвращаем JSON-ответ вместо редиректа
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':  # Проверка на AJAX запрос
                return JsonResponse({
                    'success': True,
                    'message': f'Товар "{product.name}" успешно добавлен в корзину!'
                })
            else:
                # Для обычного POST-запроса делаем редирект как раньше
                return redirect('my_flower_del:product_detail', product_id=product_id)
    else:
        form = AddToCartForm()

    return redirect('my_flower_del:product_detail', product_id=product_id)



# views.py
def create_order(request):
    if request.method == 'POST':
        cart = Cart.objects.filter(user=request.user).first()
        if cart and cart.items.exists():
            # Создаем новый заказ
            total_amount = sum(item.quantity * item.product.price for item in cart.items.all())
            order = Order.objects.create(
                user=request.user,
                total_amount=total_amount
            )

            # Создаем элементы заказа
            for cart_item in cart.items.all():
                OrderItem.objects.create(
                    order=order,
                    product=cart_item.product,
                    quantity=cart_item.quantity,
                    price=cart_item.product.price
                )

            # Очищаем корзину
            cart.items.all().delete()

            return redirect('my_flower_del:order_confirmation', order_id=order.id)
    return redirect('my_flower_del:cart')


def order_confirmation(request, order_id):
    try:
        order = Order.objects.get(id=order_id, user=request.user)
        order_items = order.items.all()
        total = sum(item.price * item.quantity for item in order_items)

        context = {
            'cart_items': order_items,  # переименовали для совместимости с шаблоном
            'total': total,
            'order': order
        }
        return render(request, 'my_flower_del/order_confirmation.html', context)
    except Order.DoesNotExist:
        return redirect('my_flower_del:cart')


# Каталог
def catalog(request):
     products = Product.objects.all()  # Выбираем все товары
     return render(request, 'my_flower_del/index.html', {'products': products})  # Используем шаблон index.html


# Детали товара
def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    comments = Comment.objects.filter(product=product)  # Получаем комментарии

    add_to_cart_form = AddToCartForm()
    comment_form = CommentForm()

    if request.method == 'POST':
        if 'add_to_cart' in request.POST:
            add_to_cart_form = AddToCartForm(request.POST)
            if add_to_cart_form.is_valid():
                quantity = add_to_cart_form.cleaned_data['quantity']

                cart, _ = Cart.objects.get_or_create(user=request.user)
                cart_item, created = CartItem.objects.get_or_create(
                    cart=cart,
                    product=product,
                    defaults={'quantity': quantity}
                )

                if not created:
                    cart_item.quantity += quantity
                    cart_item.save()

                return redirect('my_flower_del:product_detail', product_id=product_id)

        elif 'add_comment' in request.POST:
            comment_form = CommentForm(request.POST)
            if comment_form.is_valid():
                comment = comment_form.save(commit=False)
                comment.product = product
                comment.user = request.user
                comment.save()

                return redirect('my_flower_del:product_detail', product_id=product_id)

    return render(
        request,
        'my_flower_del/product_detail.html',
        {
            'product': product,
            'comments': comments,
            'comment_form': comment_form,
            'add_to_cart_form': add_to_cart_form,
        }
    )


# Корзина
def cart(request):
    # Сначала получаем корзину пользователя
    cart = Cart.objects.filter(user=request.user).first()
    cart_items = []
    total_price = 0

    if cart:
        # Получаем все items для этой корзины
        cart_items = cart.items.all()  # используем related_name="items"
        # Подсчитываем общую стоимость
        total_price = sum(item.quantity * item.product.price for item in cart_items)

    return render(request, 'my_flower_del/cart.html', {
        'cart_items': cart_items,
        'total_price': total_price
    })


def remove_from_cart(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
    cart_item.delete()
    return redirect('my_flower_del:cart')


def clear_cart(request):
    cart = Cart.objects.filter(user=request.user).first()
    if cart:
        cart.items.all().delete()
    return redirect('my_flower_del:cart')


# Добавление комментария
def add_comment(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.product = product  # Связываем комментарий с продуктом
            comment.save()
            return redirect('my_flower_del:product_detail', product_id=product_id)
    else:
        return redirect('my_flower_del:product_detail', product_id=product_id)