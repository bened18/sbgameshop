from django.db import models
from customuser.models import CustomUser


class Category(models.Model):
    # Modelo para categoria de los productos
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Genre(models.Model):
    # Modelo para generos de videojuegos
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Platform(models.Model):
    # Modelo para plataformas del producto (PC, PlayStation, Xbox, Nintendo, etc.)
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Product(models.Model):
    # Main product model
    name = models.CharField(max_length=200)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    platform = models.ForeignKey(Platform, on_delete=models.CASCADE)
    description = models.TextField()
    price = models.FloatField()
    image = models.ImageField(
        upload_to="product_images/",
        default="product_images\The-Witcher-3-Wild-Hunt.jpg"
    )
    genres = models.ManyToManyField(Genre, blank=True)  # For video game genres

    def __str__(self):
        return self.name


class ShoppingCart(models.Model):
    # Model for user shopping carts
    user = models.OneToOneField(
        CustomUser, on_delete=models.CASCADE, related_name='shoppingcart_customuser')
    products = models.ManyToManyField(Product, through='CartItem')
    total_cost = models.FloatField(default=0)

    def calculate_total_cost(self):
        self.total_cost = sum(item.subtotal for item in self.cart_items.all())
        self.save()


class CartItem(models.Model):
    # Model for cart items
    cart = models.ForeignKey(
        ShoppingCart, on_delete=models.CASCADE, related_name='cart_items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    subtotal = models.FloatField()

    def save(self, *args, **kwargs):
        self.subtotal = self.product.price * self.quantity
        super().save(*args, **kwargs)
