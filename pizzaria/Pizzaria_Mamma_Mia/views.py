from django.shortcuts import render
from django.views import View
from Pizzaria_Mamma_Mia.models import *

class Home(View):
    def get(self, request):
        context = {
            "bebidas": list(Bebida.objects.all()),
        }
        return render(request, "home.html", context)
    
class Login(View):
    def get(self, request):
        return render(request, "login.html")
    
def cadastro(request):
    return render(request, "create.html")

def store(request):
    return render(request, "home.html")