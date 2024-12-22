from django import forms
from .models import Order
from datetime import datetime, timedelta
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import (
    User,
    ShippingAddress,
    Comment,
    Cart,
    CartItem  # Добавляем импорт CartItem
)


class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')


class LoginForm(AuthenticationForm):
    pass


class ShippingAddressForm(forms.ModelForm):
    class Meta:
        model = ShippingAddress
        fields = ['first_name', 'last_name', 'email', 'phone', 'address', 'postal_code', 'city', 'country']
        widgets = {
            'address': forms.Textarea(attrs={'rows': 2}),
        }


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['author', 'text']
        widgets = {
            'author': forms.TextInput(attrs={'class': 'form-control'}),
            'text': forms.Textarea(attrs={'class': 'form-control'}),
        }


class AddToCartForm(forms.Form):
    quantity = forms.IntegerField(
        min_value=1,
        widget=forms.NumberInput(attrs={
            'class': 'form-control small-input',
            'style': 'width: 70px;'
        }),
        label='Количество'
    )


class CartForm(forms.ModelForm):
    class Meta:
        model = Cart
        fields = []  # Пустой список, так как Cart только связывает пользователя


class CartItemForm(forms.ModelForm):
    class Meta:
        model = CartItem
        fields = ['product', 'quantity']


class DeliveryForm(forms.ModelForm):
    delivery_date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}),
        label='Дата доставки'
    )
    delivery_time = forms.TimeField(
        widget=forms.TimeInput(attrs={'type': 'time'}),
        label='Время доставки'
    )

    class Meta:
        model = Order
        fields = ['recipient_name', 'phone_number', 'delivery_address',
                  'delivery_date', 'delivery_time', 'delivery_notes']
        labels = {
            'recipient_name': 'Имя получателя',
            'phone_number': 'Номер телефона',
            'delivery_address': 'Адрес доставки',
            'delivery_notes': 'Примечания к доставке'
        }

    def clean_delivery_date(self):
        date = self.cleaned_data['delivery_date']
        today = datetime.now().date()

        if date < today:
            raise forms.ValidationError('Дата доставки не может быть в прошлом')

        if date > today + timedelta(days=14):
            raise forms.ValidationError('Доставка возможна только в течение следующих 14 дней')

        return date

    def clean_delivery_time(self):
        time = self.cleaned_data['delivery_time']

        # Проверка рабочего времени (9:00 - 21:00)
        if time.hour < 9 or time.hour >= 21:
            raise forms.ValidationError('Доставка возможна только с 9:00 до 21:00')

        return time