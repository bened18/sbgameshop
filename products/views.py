from django.db import IntegrityError
from django.shortcuts import redirect, render, get_object_or_404
from django.views import View
from django.views.generic import TemplateView
from .models import Product, ShoppingCart, CartItem
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator


class SingUpView(TemplateView): 
    template_name = "products/singup.html"

    def get(self, request):
        viewData = {
            "form": UserCreationForm
        } 
        return render(request, self.template_name, viewData)

    def post(self, request):
        if request.POST['password1'] == request.POST['password2']:
            try:
                #registrar usuario
                user = User.objects.create_user(username=request.POST['username'], password=request.POST['password1'])
                user.save()
                login(request, user)
                return redirect('home')
            except IntegrityError:
                viewData = {
                    "form": UserCreationForm,
                    "message": "el usuario ya existe"
                } 
                return render(request, self.template_name, viewData)
        viewData = {
                "form": UserCreationForm,
                "message": "las contraseñas no son iguales"
            } 
        return render(request, self.template_name, viewData)

class SingOut(View):
    def get(self, request):
        logout(request)
        return redirect('home')

class SingIn(View):
    template_name = "products/singin.html"

    def get(self, request):
        viewData = {
            "form": AuthenticationForm
        } 
        return render(request, self.template_name, viewData)
    
    def post(self, request):
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if user is None:
            viewData = {
            "form": AuthenticationForm,
            "message": 'Usuario o contraseña incorrecto '
            } 
            return render(request, self.template_name, viewData)
        else:
            login(request,user)
            return redirect('home')

class ProductView(TemplateView): 
    template_name = "products/products.html"

    def get(self, request): 
        viewData = {
            "products": Product.objects.all()
        } 
        return render(request, self.template_name, viewData)

class ProductDetail(View):
    template_name = "products/product_detail.html"

    def get(self, request, product_id):
        product = get_object_or_404(Product, pk=product_id)
        viewData = {
            "product": product
        } 
        return render(request, self.template_name, viewData)