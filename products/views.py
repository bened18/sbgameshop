from django.shortcuts import render

# Create your views here.









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