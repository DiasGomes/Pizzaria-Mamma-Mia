from django.shortcuts import render
from django.views import View
from Pizzaria_Mamma_Mia.models import *

"""
CLASSES
"""
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

class Cardapio(View):
    def get(self, request):
        context = {
            "bebidas": list(Bebida.objects.all()),
            "pizzas": dadosPizza(),
        }
        return render(request, "cardapio.html", context) 
    
"""
FUNÇÕES AUXILIARES
"""
def dadosPizza():    
    lst_pizzas = Pizza.objects.all().values("id", "nome", "imagem", "preco", "tamanho__tamanho", "composicao__fk_ingredientes__nome")
    out = []
    lst_id = []
    # manipula produções para retornar autores de uma mesma produção
    for obj in lst_pizzas:
        if obj['id'] in lst_id:
            index = lst_id.index(obj['id'])
            out[index]['ingredientes'].append(obj['composicao__fk_ingredientes__nome'])
        else:
            lst_id.append(obj['id'])
            out.append(
                {
                    'nome': obj['nome'],
                    'preco': obj['preco'],
                    'imagem': obj['imagem'],
                    'tamanho': obj['tamanho__tamanho'],
                    'ingredientes': [obj['composicao__fk_ingredientes__nome']]
                }
            )
    return out