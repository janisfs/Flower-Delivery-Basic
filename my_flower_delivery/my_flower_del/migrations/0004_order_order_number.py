# Generated by Django 5.1.4 on 2024-12-25 20:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("my_flower_del", "0003_alter_order_status_flowerorder"),
    ]

    operations = [
        migrations.AddField(
            model_name="order",
            name="order_number",
            field=models.CharField(blank=True, default=None, max_length=50, null=True),
        ),
    ]
