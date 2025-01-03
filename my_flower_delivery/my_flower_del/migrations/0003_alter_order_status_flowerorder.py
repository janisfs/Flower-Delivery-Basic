# Generated by Django 5.1.4 on 2024-12-25 10:37

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("my_flower_del", "0002_remove_order_notes_order_delivery_address_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="order",
            name="status",
            field=models.CharField(
                choices=[
                    ("pending", "В обработке"),
                    ("paid", "Оплачен"),
                    ("confirmed", "Подтвержден"),
                    ("shipped", "Отправлен"),
                    ("delivered", "Доставлен"),
                    ("cancelled", "Отменен"),
                ],
                default="pending",
                max_length=20,
            ),
        ),
        migrations.CreateModel(
            name="FlowerOrder",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "order_number",
                    models.CharField(
                        max_length=10, unique=True, verbose_name="Номер заказа"
                    ),
                ),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("new", "Новый заказ"),
                            ("confirmed", "Подтвержден"),
                            ("assembly", "Сборка букета"),
                            ("delivery", "В доставке"),
                            ("completed", "Доставлен"),
                            ("cancelled", "Отменён"),
                        ],
                        max_length=20,
                        verbose_name="Статус",
                    ),
                ),
                (
                    "created_at",
                    models.DateTimeField(
                        auto_now_add=True, verbose_name="Дата создания"
                    ),
                ),
                (
                    "delivery_datetime",
                    models.DateTimeField(verbose_name="Дата и время доставки"),
                ),
                ("delivery_address", models.TextField(verbose_name="Адрес доставки")),
                (
                    "recipient_name",
                    models.CharField(max_length=100, verbose_name="Имя получателя"),
                ),
                (
                    "recipient_phone",
                    models.CharField(max_length=20, verbose_name="Телефон получателя"),
                ),
                (
                    "total_amount",
                    models.DecimalField(
                        decimal_places=2, max_digits=10, verbose_name="Сумма заказа"
                    ),
                ),
                (
                    "comment",
                    models.TextField(
                        blank=True, null=True, verbose_name="Комментарий к заказу"
                    ),
                ),
                (
                    "customer",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="Клиент",
                    ),
                ),
            ],
            options={
                "verbose_name": "Заказ",
                "verbose_name_plural": "Заказы",
                "ordering": ["-created_at"],
            },
        ),
    ]
