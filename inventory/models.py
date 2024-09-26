from django.db import models
from django.core.validators import MinValueValidator
from accounts.models import CustomUser as User

# Create your models here.


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    image = models.ImageField(
        upload_to='categories_images/', blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Categories'


class Product(models.Model):
    code = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=200)
    description = description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, validators=[
                                MinValueValidator(0.01)])
    stock = models.PositiveIntegerField(default=0)
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, null=True, related_name='products')
    favorites = models.ManyToManyField(
        User, related_name='favorite_products', blank=True)

    def get_first_image_url(self):
        first_image = self.images.first()
        if first_image:
            return first_image.image.url
        return '/static/images/default-product.jpg'

    def __str__(self):
        return f"{self.code} - {self.name}"


class ProductImage(models.Model):
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='products_images/')

    def __str__(self):
        return f"Imagen for {self.product.name} - {self.id}"
