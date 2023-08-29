from django.shortcuts import render

# Create your views here.











































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