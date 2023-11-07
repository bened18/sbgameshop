from django.test import TestCase
from .models import Category, Platform, Product, ShoppingCart, CartItem
from customuser.models import CustomUser

class ProductModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Configura datos de prueba para el modelo Product
        category = Category.objects.create(name='Electronics')
        platform = Platform.objects.create(name='PlayStation')
        product = Product.objects.create(
            name='Product Test',
            category=category,
            platform=platform,
            description='This is a test product.',
            price=19.99,
        )

    def test_name_field(self):
        product = Product.objects.get(id=1)
        field_label = product._meta.get_field('name').verbose_name
        self.assertEqual(field_label, 'name')
        self.assertEqual(product.name, 'Product Test')

    def test_category_field(self):
        product = Product.objects.get(id=1)
        field_label = product._meta.get_field('category').verbose_name
        self.assertEqual(field_label, 'category')
        self.assertEqual(product.category.name, 'Electronics')

    def test_platform_field(self):
        product = Product.objects.get(id=1)
        field_label = product._meta.get_field('platform').verbose_name
        self.assertEqual(field_label, 'platform')
        self.assertEqual(product.platform.name, 'PlayStation')

    def test_description_field(self):
        product = Product.objects.get(id=1)
        field_label = product._meta.get_field('description').verbose_name
        self.assertEqual(field_label, 'description')
        self.assertEqual(product.description, 'This is a test product.')

    def test_price_field(self):
        product = Product.objects.get(id=1)
        field_label = product._meta.get_field('price').verbose_name
        self.assertEqual(field_label, 'price')
        self.assertEqual(product.price, 19.99)


class ShoppingCartModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Configura datos de prueba para el modelo ShoppingCart
        user = CustomUser.objects.create(username='testuser')
        shopping_cart = ShoppingCart.objects.create(user=user, total_cost=0)

    def test_user_field(self):
        shopping_cart = ShoppingCart.objects.get(id=1)
        field_label = shopping_cart._meta.get_field('user').verbose_name
        self.assertEqual(field_label, 'user')
        self.assertEqual(shopping_cart.user.username, 'testuser')

    def test_total_cost_field(self):
        shopping_cart = ShoppingCart.objects.get(id=1)
        field_label = shopping_cart._meta.get_field('total_cost').verbose_name
        self.assertEqual(field_label, 'total cost')
        self.assertEqual(shopping_cart.total_cost, 0)

    def test_calculate_total_cost_method(self):
        shopping_cart = ShoppingCart.objects.get(id=1)
        shopping_cart.calculate_total_cost()
        self.assertEqual(shopping_cart.total_cost, 0)  # No hay productos en el carrito, por lo que el costo debe ser 0
