from django.db import models

# Create your models here.
class Flower(models.Model):
    title = models.CharField('Название', max_length=100)
    description = models.TextField('Описание', blank=True, null=True)
    image = models.ImageField('Изображение', upload_to='flowers/', blank=True, null=True)


    def __str__(self):
        return self.title


    class Meta:
        verbose_name = 'Цветок'
        verbose_name_plural = 'Цветы'


class Bouquet(models.Model):
    name = models.CharField(max_length=100, verbose_name="Название")
    description = models.TextField(verbose_name="Описание", blank=True)
    image = models.ImageField(upload_to="bouquets/", verbose_name="Картинка", blank=True)
    flowers = models.ManyToManyField(Flower, verbose_name="Цветы", related_name="bouquets")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Цена")

    class Meta:
        verbose_name = "Букет"
        verbose_name_plural = "Букеты"

    def __str__(self):
        return self.name
