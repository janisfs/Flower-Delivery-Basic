from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect, get_object_or_404
from .forms import RegisterForm
from .forms import LoginForm, RegisterForm
from django.contrib.auth import authenticate, login as auth_login, logout
from django.contrib.auth.decorators import login_required
from .models import Product, Order, OrderItem, Cart, CartItem, Comment
from .forms import ShippingAddressForm, AddToCartForm, CartForm
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from .forms import CommentForm


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
            return redirect('index')
        else:
            print("Ошибки формы:", form.errors)
    else:
        form = LoginForm()

    return render(request, 'my_flower_del/login.html', {'form': form})


# Выход из системы
def logout_view(request):
    logout(request)
    return redirect('index')


# Регистрация
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


# Корзина
@login_required
def checkout(request):
    cart_items = request.session.get('cart', {})
    if not cart_items:
        return redirect('cart')

    order = Order.objects.create(user=request.user, status='pending', total_amount=0)

    total_amount = 0
    for product_id, quantity in cart_items.items():
        product = Product.objects.get(id=product_id)
        order_item = OrderItem.objects.create(
            order=order,
            product=product,
            quantity=quantity,
            price=product.price
        )
        total_amount += product.price * quantity

    order.total_amount = total_amount
    order.save()

    if request.method == 'POST':
        shipping_form = ShippingAddressForm(request.POST)
        if shipping_form.is_valid():
            shipping_address = shipping_form.save(commit=False)
            shipping_address.order = order
            shipping_address.save()

            # Создаем корзину
            cart = Cart.objects.create(user=request.user)

            return redirect('order_confirmation', order_id=order.id)
    else:
        shipping_form = ShippingAddressForm()

    return render(request, 'my_flower_del/checkout.html', {
        'form': shipping_form,
    })


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

            # Изменено в соответствии с вашей структурой URL
            return redirect('my_flower_del:product_detail', product_id=product_id)
    else:
        form = AddToCartForm()

    # Здесь тоже изменено
    return redirect('my_flower_del:product_detail', product_id=product_id)


# Подтверждение заказа
def order_confirmation(request, order_id):
    order = Order.objects.get(id=order_id, user=request.user)
    return render(request, 'my_flower_del/order_confirmation.html', {'order': order})


# Каталог
def catalog(request):
     products = Product.objects.all()  # Выбираем все товары
     return render(request, 'index.html', {'products': products})  # Используем шаблон index.html


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


# Мой профиль
def account(request):
    user = request.user
    return render(request, 'account.html')


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