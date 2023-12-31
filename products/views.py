from django.db import IntegrityError
from django.shortcuts import redirect, render, get_object_or_404
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import TemplateView, FormView
from django.utils.translation import gettext as _
from django.http import HttpResponse

from .form import AddProductForm
from .models import Product, ShoppingCart, CartItem, Genre
from customuser.models import CustomUser
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from django.http import JsonResponse
from django.core import serializers
import requests


class SingUpView(TemplateView):
    template_name = "products/singup.html"

    # Si el metodo es 'get' se envia el formulario de creación de usuario
    def get(self, request):
        viewData = {
            # formulario de creación de usuario con la clase 'django.contrib.auth.forms'
            "form": UserCreationForm
        }
        return render(request, self.template_name, viewData)

    # si el metodo es 'post' se valida la creación del usuario
    def post(self, request):
        # Validamos que las contraseñas coincidan
        if request.POST['password1'] == request.POST['password2']:
            # tratamos de registrar al usuario en la base de datos
            try:
                # registrar usuario enviando el 'username' y la 'password'
                user = CustomUser.objects.create_user(
                    username=request.POST['username'], password=request.POST['password1'])
                # guardamos el usuario en la base de datos
                user.save()
                # iniciamos sesion automaticamente
                login(request, user)
                # redirigimos a la url de home
                return redirect('home')
            # si no pudimos registrar al usuario es por que ya existe en la base de datos
            except IntegrityError:
                viewData = {
                    # volvemos a enviar el formulario
                    "form": UserCreationForm,
                    # enviamos un mensaje de error
                    "message": "el usuario ya existe" , 
                    "message": _("The user already exists")
                }
                return render(request, self.template_name, viewData)
        # si las contraseñas no son iguales le pedimos que vuelva a intentar
        else:
            viewData = {
                # volvemos a enviar el formulario
                "form": UserCreationForm,
                # enviamos un mensaje de error
                "message": "las contraseñas no son iguales", 
                "message": _("Passwords do not match")
            }
            return render(request, self.template_name, viewData)


class SingOut(View):
    def get(self, request):
        # Se cierra sesion
        logout(request)
        return redirect('home')


class SingIn(View):
    template_name = "products/singin.html"

    # si el metodo es 'get' se envia el formulario para iniciar sesion
    def get(self, request):
        viewData = {
            # formulario de inicio de sesion con la clase 'django.contrib.auth.forms'
            "form": AuthenticationForm
        }
        return render(request, self.template_name, viewData)

    # si el metodo es 'post' se valida el formulario
    def post(self, request):
        # se verifica que el usuario coincida con la base de datos
        user = authenticate(
            request, username=request.POST['username'], password=request.POST['password'])
        # si el usuario no existe
        if user is None:
            viewData = {
                # se vueve a enviar el form
                "form": AuthenticationForm,
                # se envia mensaje de error
                "message": 'Usuario o contraseña incorrecto',
                "message": _('Incorrect username or password')  # Cadena marcada para traducción
            }
            return render(request, self.template_name, viewData)
        # si el usuario si existe
        else:
            # se inicia sesion
            login(request, user)
            return redirect('home')


class ProductView(TemplateView):
    template_name = "products/products.html"

    # Mostrar todos los productos de la base de datos
    def get(self, request):
        # Llamada a la API para obtener la tasa de cambio
        response = requests.get('https://v6.exchangerate-api.com/v6/9db1c20e7f6dbe3b410e777f/latest/USD')
        if response.status_code == 200:
            data = response.json()
            exchange_rate = data['conversion_rates']['COP']

            # Obtenemos todos los productos de la base de datos
            products = Product.objects.all()

            # Agregar el precio en USD a cada producto
            for product in products:
                product.price_usd = (product.price / exchange_rate)*1000
                

            # Enviamos todos los productos a products.html para ser mostrados
            viewData = {
                "products": products
            }
            return render(request, self.template_name, viewData)
        else:
            # Manejar el caso en que la API no responde adecuadamente
            # Aquí puedes decidir cómo manejar este error, por ejemplo, mostrando un mensaje
            # o utilizando una tasa de cambio predeterminada.
            viewData = {
                "error": "No se pudo obtener la tasa de cambio actual."
            }
            return render(request, self.template_name, viewData)


class SearchResultsView(View):
    template_name = "products/search_results.html"

    # Mostrar el producto buscado por la barra de busqueda
    def get(self, request):
        # Obtenemos el string de lo que se esta buscando
        query = request.GET.get('query', '')
        # Filtramos por productos que contengan el query
        products = Product.objects.filter(name__icontains=query)
        viewData = {
            # Enviamos los productos que coincidan
            "products": products,
            # Enviamos el string de búsqueda a la plantilla
            "query": query
        }
        # se envia el diccionario viewData a 'search_results.html'
        return render(request, self.template_name, viewData)


class FilterResultsView(TemplateView):
    template_name = "products/filter_results.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Product.objects.order_by(
            'category').values_list('category', flat=True).distinct()
        context['platforms'] = Product.objects.order_by(
            'platform').values_list('platform', flat=True).distinct()
        # Lógica para filtrar productos por categoría y plataforma
        return context


class ProductDetail(View):
    template_name = "products/product_detail.html"

    def get(self, request, product_id):
        # miramos si el producto existe en la base de datos
        product = get_object_or_404(Product, pk=product_id)
        viewData = {
            # enviamos la informacion del producto obtenido
            "product": product
        }
        return render(request, self.template_name, viewData)


class CartView(View):
    template_name = "products/cart.html"

    # verificamos que el usuario este logeado
    @method_decorator(login_required)
    def get(self, request):
        user = self.request.user
        # traemos la información del carrito de compras de ese usuario
        cart, created = ShoppingCart.objects.get_or_create(user=user)
        # obtenemos cada uno de los productos del carrito
        cart_items = cart.cart_items.all()
        viewData = {
            'cart': cart,
            'cart_items': cart_items
        }
        return render(request, self.template_name, viewData)


class AddToCart(View):
    # el usuario debe estar logeado
    @method_decorator(login_required)
    def post(self, request, product_id):
        # buscamos el producto que quiere agregar al carrito en la base de datos
        product = get_object_or_404(Product, pk=product_id)
        # obtenemos el carrito de compras del usuario
        cart, _ = ShoppingCart.objects.get_or_create(user=request.user)
        cart_item, item_created = CartItem.objects.get_or_create(
            cart=cart, product=product)
        # si no existia ese producto en el carrito de suma 1 a la cantidad
        if not item_created:
            cart_item.quantity += 1
            # guardamos el producto
            cart_item.save()
        # Se actualiza el costo total del carrito
        cart.calculate_total_cost()
        return redirect('view_cart')


class DeleteCartItem(View):
    # el usuario debe estar logeado
    @method_decorator(login_required)
    def post(self, request, cart_item_id):
        cart_item = CartItem.objects.get(id=cart_item_id)
        cart = cart_item.cart
        # Eliminar el artículo del carrito
        cart_item.delete()
        # Recalcular el costo total del carrito
        cart.calculate_total_cost()
        # Redirigir de vuelta a la vista del carrito
        return redirect('view_cart')

@method_decorator(login_required, name='dispatch')
class AddProductView(FormView):
    template_name = "products/add_product_form.html"
    form_class = AddProductForm
    success_url = reverse_lazy('home')

    def dispatch(self, request, *args, **kwargs):
        user = CustomUser.objects.get(id=request.user.id)
        if not request.user.is_authenticated or not user.is_editor:
            return redirect('home')
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        # Crear un nuevo producto utilizando los datos del formulario
        product = Product(
            name=form.cleaned_data['name'],
            category=form.cleaned_data['category'],
            platform=form.cleaned_data['platform'],
            description=form.cleaned_data['description'],
            price=form.cleaned_data['price'],
            image=form.cleaned_data['image'],
        )
        product.save()
        product.genres.set(form.cleaned_data['genres'])

        return super().form_valid(form)
    
@method_decorator(login_required, name='dispatch')
class DeleteProductView(View):

    def dispatch(self, request, *args, **kwargs):
        user = CustomUser.objects.get(id=request.user.id)
        if not request.user.is_authenticated or not user.is_editor:
            return redirect('home')
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, product_id):
        # Obtiene el producto que se va a eliminar.
        product = Product.objects.get(pk=product_id)
        # Elimina el producto.
        product.delete()
        return redirect('home')  # Cambia 'product_list' a la URL adecuada.

class ProductosJsonView(View):

    def get(self, request):
        productos = Product.objects.all()
    
        # Crea una lista para almacenar los productos de forma ordenada
        productos_list = []
    
        for producto in productos:
            producto_dict = {
                'id': producto.pk,
                'name': producto.name,
                'category': producto.category.name,
                'platform': producto.platform.name,
                'description': producto.description,
                'price': producto.price,
                'image': producto.image.url,
                'genres': [genre.name for genre in producto.genres.all()]
            }
            productos_list.append(producto_dict)

        # Devuelve la lista de productos en formato JSON
        return JsonResponse({'productos': productos_list}, safe=False)
    
class ObtenerProductosExternosView(View):

    def get(self, request):
        template_name = "products/productos_externos.html"
        # URL de la API externa
        url_api_externa = "http://34.136.78.13:8000/api/products/"

        try:
            # Realiza una solicitud GET a la API externa
            response = requests.get(url_api_externa)

            # Verifica si la solicitud fue exitosa (código de estado 200)
            if response.status_code == 200:
                # Convierte la respuesta JSON en una lista de productos
                productos_externos = response.json()
                # Itera sobre los productos externos y actualiza la URL de la imagen
                for producto_externo in productos_externos:
                    # Obtiene la URL de la imagen original
                    imagen_original_url = producto_externo['product_image']
        
                    # Reemplaza la parte de la URL que deseas cambiar
                    nueva_url = imagen_original_url.replace("http://34.136.78.13:8000/product_image/", "http://34.136.78.13:8000/static/product_image/")

                    # Actualiza la URL en el diccionario del producto
                    producto_externo['product_image'] = nueva_url
                # Renderiza el template con los productos externos como contexto
                return render(request, template_name, {'productos_externos': productos_externos})

            else:
                # Si la solicitud no fue exitosa, devuelve un mensaje de error
                return JsonResponse({'error': 'No se pudo obtener la información de la API externa.'}, status=500)

        except requests.exceptions.RequestException as e:
            # Maneja posibles errores de conexión
            return JsonResponse({'error': 'Error de conexión a la API externa: ' + str(e)}, status=500)