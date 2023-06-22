from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.views import View
from Pizzaria_Mamma_Mia.models import *
from Pizzaria_Mamma_Mia.views_suport import *   # funções auxiliares do views

"""
CLASSES
"""
# tela do home
class Home(View):
    def get(self, request):
        context = {
            
        }
        return render(request, "home.html", context)

# tela que exibe os cárdapios(Pizzas e bebibas)
class Cardapio(View):
    def get(self, request):
        context = {
            "bebidas": list(Bebida.objects.all()),
            "sabores": dadosSabores(),
        }
        return render(request, "cardapio.html", context) 

# tela que exibe os combos
class Combo(View):
    def get(self, request):
        context = {
            "combos": [],
        }
        return render(request, "combo.html", context) 
    
# tela de login
class Login(View):
    def get(self, request):
        # mensagens de confirmação e erro
        msg=None
        _class=None
        if 'msg' in request.session:
            msg = request.session['msg']
            _class = request.session['class']
            request.session["msg"] = None
            request.session["class"] = None
        return render(request, "login.html", {"msg": msg, "class": _class})

# tela do perfil/conta do usuário  
class Conta(View):
    def get(self, request):
        if request.user.is_authenticated:
            # conteudo
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

            # mensagens de confirmação e erro
            msg=None
            _class=None
            if 'msg' in request.session:
                msg = request.session['msg']
                _class = request.session['class']
                request.session["msg"] = None
                request.session["class"] = None

            # retorna conteudo
            context = {
                "conta": conta,
                "bairros": list(Bairro.objects.all().order_by("nome")),
                "msg": msg,
                "class": _class,
            }
            return render(request, "conta.html", context) 
        else:
            return render(request, "login.html") 

# tela de cadastro
class Cadastro(View):
    def get(self, request):
        # mensagens de confirmação e erro
        msg=None
        _class=None
        if 'msg' in request.session:
            msg = request.session['msg']
            _class = request.session['class']
            request.session["msg"] = None
            request.session["class"] = None

        data = {
            "bairros": list(Bairro.objects.all().order_by("nome")),
            "msg": msg,
            "class": _class,
        }
        return render(request, "cadastro.html", data)

# tela da compra
class Compra(View):
    def get(self, request):
        if request.user.is_authenticated:
            context = {}
            return render(request, "compra.html", context) 
        else:
            return render(request, "login.html") 

# tela do carrinho 
class Carrinho(View):
    def get(self, request):
        if request.user.is_authenticated:
            context = {}
            return render(request, "carrinho.html", context) 
        else:
            return render(request, "login.html") 


"""
FUNÇÕES (executam alguma ação via url, mas não renderizam páginas html)
"""

# ação de cadastro dos usuários no BD
def store(request):
    data = {}
    # verifica a confirmação da senha
    if request.POST["password"] != request.POST["password-conf"]:
        request.session["msg"] = "senhas diferentes"
        request.session["class"] = "alert-danger"
    # verifica se os campos estão preenchidos
    elif campoVazio(request):
        request.session["msg"] = "campo(s) vazio(s)"
        request.session["class"] = "alert-danger"
    # cadastra usuário
    else:
        try:
            cadastrarUser(request)
            # mensagem
            request.session["msg"] = "Cadastrado com Sucesso"
            request.session["class"] = "alert-sucess"
        except:
            request.session["msg"] = "Usúario já existente"
            request.session["class"] = "alert-danger"
    return redirect("cadastrar")

# ações de login de usuário
def doLogin(request):
    user = authenticate(username=request.POST['user'], password=request.POST['password'])
    # login aceito
    if user is not None:
        login(request, user)
        return redirect("home")
    # login incorreto
    else:
        request.session["msg"] = "Senha ou Usúario incorreto"
        request.session["class"] =  "alert-danger"
        return redirect("login")

# ações de logout de usuário
def doLogout(request):
    logout(request)
    return redirect("home")

# ação de atualização do perfil dos usuários no BD
def editarConta(request):
    # verifica a confirmação da senha
    if request.POST["password"] != request.POST["password-conf"] and request.POST["password"] != "":
        request.session['msg'] = "senhas diferentes"
        request.session["class"] = "alert-danger"
    # verifica se os campos estão preenchidos
    elif todosCamposVazios(request):
        request.session['msg'] = "campo(s) vazio(s)"
        request.session["class"] = "alert-danger"
    # edita usuário
    else:
        editarUser(request)
        # mensagem
        request.session['msg'] = "Perfil atualizado"
        request.session["class"] = "alert-sucess"
    return redirect("conta")
