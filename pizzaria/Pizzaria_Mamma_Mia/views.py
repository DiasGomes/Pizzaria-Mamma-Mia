from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
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

class Cardapio(View):
    def get(self, request):
        context = {
            "bebidas": list(Bebida.objects.all()),
            "sabores": dadosSabores(),
        }
        return render(request, "cardapio.html", context) 
    
class Combo(View):
    def get(self, request):
        context = {
            "combos": [],
        }
        return render(request, "combo.html", context) 
    
class Login(View):
    def get(self, request):
        return render(request, "login.html")
    
class Conta(View):
    def get(self, request):
        if request.user.is_authenticated:
            user = User.objects.all().get(email=request.user.email)
            cliente = Cliente.objects.all().get(fk_user=user.id)
            endereco = Endereco.objects.all().get(id=cliente.fk_endereco.id)
            bairro = Bairro.objects.all().get(id=endereco.fk_bairro.id)
            conta = {
                "user": user,
                "telefone": cliente,
                "endereco": endereco,
                "bairro": bairro,
            }
            context = {
                "conta": conta,
                "bairros": list(Bairro.objects.all().order_by("nome"))
            }
            return render(request, "conta.html", context) 
        else:
            return render(request, "login.html") 

# tela de cadastro
class Cadastro(View):
    def get(self, request):
        data = {
            "bairros": list(Bairro.objects.all().order_by("nome"))
        }
        return render(request, "cadastro.html", data)
    
class Compra(View):
    def get(self, request):
        if request.user.is_authenticated:
            context = {}
            return render(request, "compra.html", context) 
        else:
            return render(request, "login.html") 
        
class Carrinho(View):
    def get(self, request):
        if request.user.is_authenticated:
            context = {}
            return render(request, "carrinho.html", context) 
        else:
            return render(request, "login.html") 


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

def doLogin(request):
    data = {}
    user = authenticate(username=request.POST['user'], password=request.POST['password'])
    # login aceito
    if user is not None:
        login(request, user)
        return redirect("home")
    # login incorreto
    else:
        data['msg'] = "Senha ou Usúario incorreto"
        data["class"] = "alert-danger"
        return render(request, "login.html", data)
    
def doLogout(request):
    logout(request)
    return redirect("home")

# ação de cadastro dos usuários no BD
def editarConta(request):
    data = {}
    # verifica a confirmação da senha
    if request.POST["password"] != request.POST["password-conf"] and request.POST["password"] != "":
        data['msg'] = "senhas diferentes"
        data["class"] = "alert-danger"
    # verifica se os campos estão preenchidos
    elif todosCamposVazios(request):
        data['msg'] = "campo(s) vazio(s)"
        data["class"] = "alert-danger"
    # edita usuário
    else:
        editarUser(request)
        # mensagem
        data['msg'] = "Perfil atualizado"
        data["class"] = "alert-sucess"
    return render(request, "conta.html", data)

"""
FUNÇÕES AUXILIARES
"""
# cadastra usuário no BD
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

# atualiza dados do usuário
def editarUser(request):
    # como fazer de uma forma melhor???

    #atualiza usuário
    user = User.objects.all().get(email=request.user.email)
    if request.POST['first_name'] != "":
        user.email = request.POST['first_name']
    if request.POST['email'] != "":
        user.email = request.POST['email']
    if request.POST['first_name'] != "":
        user.email = request.POST['first_name']
    if request.POST['last_name'] != "":
        user.email = request.POST['last_name']
    if request.POST['password'] != "":
        user.set_password(request.POST['password'])
    user.save()

    # atualiza cliente
    cliente = Cliente.objects.all().get(fk_user=user.id)
    if request.POST['telefone'] != "":
        cliente.telefone = request.POST['telefone']
        cliente.save()

    # atualiza endereço
    endereco = Endereco.objects.all().get(id=cliente.fk_endereco.id)
    if request.POST['rua'] != "":
        endereco.rua = request.POST['rua']
    if request.POST['numero'] != "":
        endereco.numero = request.POST['numero']
    if request.POST['complemento'] != "":
        endereco.complemento = request.POST['complemento']
    if request.POST['cep'] != "":
        endereco.CEP = request.POST['cep']
    if request.POST['bairro'] != "":
        endereco.fk_bairro = Bairro.objects.all().get(id=request.POST['bairro'])
    endereco.save()


# testa se o campo do formulário foi todo preenchido
def campoVazio(request):
    campos = ["user", "email", "password", "first_name", "last_name", "telefone", "bairro", "rua", "cep", "numero"]
    for campo in campos:
        if request.POST[campo] == "":
            return True
    return False

# verifica se ao menos um campo está preenchido
def todosCamposVazios(request):
    campos = ["email", "password", "first_name", "last_name", "telefone", "bairro", "rua", "cep", "numero"]
    for campo in campos:
        if request.POST[campo] != "":
            return False
    return True

# manipulação dos dados dos sabores
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

