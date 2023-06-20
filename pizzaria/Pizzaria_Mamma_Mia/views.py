from django.contrib.auth.models import User
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

# tela de cadastro
class Cadastro(View):
    def get(self, request):
        data = {
            "bairros": list(Bairro.objects.all().order_by("nome"))
        }
        return render(request, "cadastro.html", data)

# ação de cadastro dos usuários no BD
def store(request):
    data = {}
    # verifica a confirmação da senha
    if request.POST["password"] != request.POST["password-conf"]:
        data['msg'] = "senhas diferentes"
        data["class"] = "alert-danger"
    # verifica se os campos estão preenchidos
    elif campoVazio(request):
        data['msg'] = "campo(s) vazio(s)"
        data["class"] = "alert-danger"
    # cadastra usuário
    else:
        try:
            cadastrarUser(request)
            # mensagem
            data['msg'] = "Cadastrado com Sucesso"
            data["class"] = "alert-sucess"
        except:
            data['msg'] = "Usúario já existente"
            data["class"] = "alert-danger"
    return render(request, "cadastro.html", data)
    
"""
FUNÇÕES AUXILIARES
"""
def cadastrarUser(request):
    # cria o usuário
    user = User.objects.create_user(request.POST['user'], request.POST['email'], request.POST['password'])
    user.first_name = request.POST['first_name']
    user.last_name = request.POST['last_name']
    user.save()

    # cria o endereço
    _bairro = Bairro.objects.get(id=request.POST['bairro'])
    _endereco = Endereco.objects.create(
        rua = request.POST['rua'],
        numero = request.POST['numero'],
        complemento = request.POST['complemento'],
        CEP = request.POST['cep'],
        fk_bairro = _bairro
    )
    _endereco.save()

    # cria o cliente
    cliente = Cliente.objects.create(
        telefone = request.POST['telefone'],
        fk_endereco = _endereco,
        fk_user = user
    )
    cliente.save()



def campoVazio(request):
    campos = ["user", "email", "password", "first_name", "last_name", "telefone", "bairro", "rua", "cep", "numero"]
    for campo in campos:
        if request.POST[campo] == "":
            return True
    return False

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