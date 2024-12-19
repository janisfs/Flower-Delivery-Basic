from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import (
    User,
    ShippingAddress,
    Product,
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
        initial=1,
        label='Количество',
        widget=forms.NumberInput(attrs={'class': 'form-control'})
    )


class CartForm(forms.ModelForm):
    class Meta:
        model = Cart
        fields = []  # Пустой список, так как Cart только связывает пользователя


class CartItemForm(forms.ModelForm):
    class Meta:
        model = CartItem
        fields = ['product', 'quantity']

