from django.shortcuts import render
from django.views import View
from Pizzaria_Mamma_Mia.models import *

"""
CLASSES
"""
class Home(View):
    def get(self, request):
        context = {
            
        }
        return render(request, "home.html", context)
    
class Login(View):
    def get(self, request):
        return render(request, "login.html")

class Cardapio(View):
    def get(self, request):
        context = {
            "bebidas": list(Bebida.objects.all()),
            "sabores": dadosSabores(),
        }
        return render(request, "cardapio.html", context) 
    
def cadastro(request):
    return render(request, "create.html")

def store(request):
    return render(request, "home.html")
    
"""
FUNÇÕES AUXILIARES
"""
def dadosSabores():    
    lst_sabores = Sabor.objects.all().values("id", "nome", "imagem", "composicao__fk_ingrediente__nome")
    out = []
    lst_id = []
    # manipula produções para retornar autores de uma mesma produção
    for obj in lst_sabores:
        if obj['id'] in lst_id:
            index = lst_id.index(obj['id'])
            out[index]['ingredientes'].append(obj['composicao__fk_ingrediente__nome'])
        else:
            lst_id.append(obj['id'])
            out.append(
                {
                    'nome': obj['nome'],
                    'imagem': obj['imagem'],
                    'ingredientes': [obj['composicao__fk_ingrediente__nome']]
                }
            )
    return out