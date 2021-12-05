from django.conf import settings
from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.utils.safestring import mark_safe
from django.urls import reverse
from utils import upload_function


class Category(models.Model):
    name = models.CharField(max_length=255, verbose_name='Наименование категории')
    slug = models.SlugField(unique=True)

    def get_absolute_url(self):
        return reverse('category_detail', kwargs={'category_slug': self.slug})

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Product(models.Model):  # каркас продукта
    category = models.ForeignKey(Category, verbose_name='Категория', on_delete=models.CASCADE)
    title = models.CharField(max_length=255, verbose_name='Наименование')
    slug = models.SlugField(unique=True)
    description = models.TextField(verbose_name='Описание', null=True)
    price = models.DecimalField(max_digits=9, decimal_places=2, verbose_name='Цена')

    def get_absolute_url(self):
        return reverse('product_detail', kwargs={'category_slug': self.category.slug, 'product_slug': self.slug})

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'


class ColorField(models.Model):
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, null=True)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    color = models.CharField(max_length=20, verbose_name='Цвет товара', null=True, blank=True)

    def __str__(self):
        return f"Цвет для {self.object_id}, {self.color}"

    class Meta:
        verbose_name = 'Цвет'
        verbose_name_plural = 'Цвета'


class SizeField(models.Model):
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, null=True)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    size = models.CharField(max_length=5, verbose_name='Размер товара', null=True, blank=True)
    in_stock = models.BooleanField(default=True)

    def __str__(self):
        return f"Размер для {self.object_id}, {self.size}"

    class Meta:
        verbose_name = 'Размер'
        verbose_name_plural = 'Размеры'


class ImageGallery(models.Model):
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, null=True)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    image = models.ImageField(upload_to=upload_function, null=True, blank=True)
    is_main = models.BooleanField(default=False)

    def __str__(self):
        return f"Изображение для {self.content_object}"

    def image_url(self):
        return mark_safe(f'<img src ="{self.image.url}" width = "auto" height = "150px">')

    class Meta:
        verbose_name = 'Галерея изображений'
        verbose_name_plural = verbose_name


class CartProduct(models.Model):
    user = models.ForeignKey('Customer', null=True, blank=True, verbose_name='Покупатель', on_delete=models.CASCADE)
    cart = models.ForeignKey('Cart', verbose_name='Корзина', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, verbose_name='Добавленный товар', on_delete=models.CASCADE, null=True,
                                blank=True)

    color = models.ForeignKey(ColorField, verbose_name='Цвет товара', on_delete=models.CASCADE, null=True,
                              blank=True)
    size = models.ForeignKey(SizeField, verbose_name='Цвет товара', on_delete=models.CASCADE, null=True, blank=True)
    qty = models.PositiveIntegerField(default=1)
    final_price = models.DecimalField(max_digits=9, decimal_places=2, verbose_name='Общая цена', null=True, blank=True,
                                      default=0)

    session_key = models.CharField(max_length=1024, null=True, blank=True, verbose_name='Ключ сессии')

    def recalc_product(self, *args, **kwargs):
        self.final_price = self.product.price * int(self.qty)

        super().save(*args, **kwargs)


    def __str__(self):
        return f"Продукт {self.cart.id} корзины: {self.product.title}"

    class Meta:
        verbose_name = 'Продукт корзины'
        verbose_name_plural = 'Продукты корзины'


class Cart(models.Model):
    owner = models.ForeignKey('Customer', null=True, blank=True, verbose_name='Покупатель', on_delete=models.CASCADE)
    products = models.ManyToManyField(CartProduct, blank=True, related_name='related_cart',
                                      verbose_name='Продукты корзины')
    total_products = models.PositiveIntegerField(default=0, verbose_name='Общее кол-во товаров')
    total_price = models.DecimalField(max_digits=9, decimal_places=2, verbose_name='Общая цена', null=True, blank=True)
    in_order = models.BooleanField(default=False)  # для истории заказов
    session_key = models.CharField(max_length=1024, null=True, blank=True, verbose_name='Ключ сессии')

    def __str__(self):
        return str(self.id)

    def recalc(self, *args, **kwargs):
        cart_data = self.products.aggregate(models.Sum('final_price'), models.Count('id'))
        if cart_data.get('final_price__sum'):
            self.total_price = cart_data['final_price__sum']
        else:
            self.total_price = 0
        self.total_products = cart_data['id__count']
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'Корзина'
        verbose_name_plural = 'Корзины'


class Order(models.Model):
    STATUS_NEW = 'Оплата подтверждается'
    STATUS_IN_PROGRESS = 'Оплата подтверждена, товар готовится'
    STATUS_READY = 'Заказ готов'
    STATUS_COMPLETED = 'Заказ завершен'

    STATUS_CHOICES = (
        (STATUS_NEW, 'Оплата в процессе подтвержения'),
        (STATUS_IN_PROGRESS, 'Оплата подтверждена'),
        (STATUS_READY, 'Заказ готов'),
        (STATUS_COMPLETED, 'Заказ получен пользователем')
    )

    customer = models.ForeignKey('Customer', verbose_name='Покупатель', on_delete=models.CASCADE, related_name='orders')
    first_name = models.CharField(max_length=100, verbose_name='Имя')
    second_name = models.CharField(max_length=100, verbose_name='Отчество')
    last_name = models.CharField(max_length=100, verbose_name='Фамилия')
    phone = models.CharField(max_length=20, verbose_name='Телефон')
    cart = models.ForeignKey(Cart, verbose_name='Корзина', null=True, blank=True, on_delete=models.CASCADE)
    address = models.CharField(max_length=1000, verbose_name='Адрес')
    status = models.CharField(max_length=100, verbose_name='Статус заказа', choices=STATUS_CHOICES, default=STATUS_NEW)
    comment = models.TextField(verbose_name='Пожелания к заказу', null=True, blank=True)
    created_at = models.DateField(verbose_name='Дата создания заказа', auto_now=True)

    def __str__(self):
        return str(self.id)


    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'


class Customer(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, verbose_name='Пользователь', on_delete=models.CASCADE)
    customer_orders = models.ManyToManyField(Order, verbose_name='Заказы покупателя', related_name='related_customer',
                                             blank=True)
    phone = models.CharField(max_length=20, verbose_name='Телефон')
    address = models.CharField(max_length=255, verbose_name='Адрес', blank=True)

    def __str__(self):
        return f"{self.user.username}"

    class Meta:
        verbose_name = 'Покупатель'
        verbose_name_plural = 'Покупатели'


class Notification(models.Model):
    recipient = models.ForeignKey(Customer, on_delete=models.CASCADE, verbose_name='Получатель')
    text = models.TextField()

    def __str__(self):
        return f"Уведомение для {self.recipient.user.username} | id={self.id}"

    class Meta:
        verbose_name = 'Уведомление'
        verbose_name_plural = 'Уведомления'
