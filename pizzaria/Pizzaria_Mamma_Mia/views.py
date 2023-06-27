from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.views import View
from Pizzaria_Mamma_Mia.models import *
from Pizzaria_Mamma_Mia.views_suport import *   # funções auxiliares do views
from django.http import JsonResponse
import json
from django.contrib import messages

"""
CLASSES
"""
# tela do home
class Home(View):
    def get(self, request):
        context = {
            'pizza': Sabor.objects.get(id=1),
            'combo': Combo.objects.get(id=1),
        }
        context.update(showQtdItensCarrinho(request))
        return render(request, "home.html", context)

# tela que exibe os cárdapios(Pizzas e bebibas)
class Cardapio(View):
    def get(self, request):
        context = {
            "bebidas": list(Bebida.objects.all()),
            "sabores": dadosSabores(),
            "combos": list(Combo.objects.all()),
            "tamanhos": list(Tamanho.objects.all())
        }
        # concatena informações do carrinho
        context.update(showQtdItensCarrinho(request))
        return render(request, "cardapio.html", context) 
    
# tela de login
class Login(View):
    def get(self, request):
        # mensagens de confirmação e erro
        context=showMsg(request)
        # concatena informações do carrinho
        context.update(showQtdItensCarrinho(request))
        return render(request, "login.html", context)

# tela do perfil/conta do usuário  
class Conta(View):
    def get(self, request):
        # acesso somente para usuário autenticado
        if request.user.is_authenticated:
            # conteudo
            conta = dadosConta(request)

            # mensagens de confirmação e erro
            msg=showMsg(request)

            # retorna conteudo
            context = {
                "conta": conta,
                "bairros": list(Bairro.objects.all().order_by("nome")),
            }

            # concatena dicionários
            context.update(msg)
            # concatena informações do carrinho
            context.update(showQtdItensCarrinho(request))
            return render(request, "conta.html", context) 
        else:
            return redirect('login') 

# tela de cadastro
class Cadastro(View):
    def get(self, request):
        # mensagens de confirmação e erro
        msg=showMsg(request)

        # retorna bairros
        context = {
            "bairros": list(Bairro.objects.all().order_by("nome")),
        }

        # concatena dicionários
        context.update(msg)
        context.update(showQtdItensCarrinho(request))

        return render(request, "cadastro.html", context)

# tela da compra
class MontarPizza(View):
    def get(self, request):
        # acesso somente para usuário autenticado
        if request.user.is_authenticated:
            context = {
                "sabores": list(Sabor.objects.all()),
                "tamanhos": list(Tamanho.objects.all()),
            }
            context.update(showQtdItensCarrinho(request))
            return render(request, "montarPizza2Sabores.html", context) 
        else:
            return redirect('login')  

# tela do carrinho 
class CarrinhoView(View):
    def get(self, request):
        # acesso somente para usuário autenticado
        if request.user.is_authenticated:
            context = showItensCarrinho(request)
            context.update(showQtdItensCarrinho(request))
            return render(request, "carrinho.html", context) 
        else:
            return redirect('login') 
        
# tela de pagamento
class Pagar(View):
    def get(self, request):
        # acesso somente para usuário autenticado
        if request.user.is_authenticated:
            cart_user, created = Carrinho.objects.get_or_create(user=request.user, completo=False)
            if cart_user.quantidade_total > 0:    
                total = cart_user.preco_total
                context = {
                    "total": total,
                }
                context.update(showQtdItensCarrinho(request))
                return render(request, "pagar.html", context) 
            else:
                return redirect('home') 
        else:
            return redirect('login') 


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
    limpaCarrinho(request)
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

def add_to_cart(request):
    data = json.loads(request.body)
    product_id = data["id"] if "id" in data else None
    product_nome = data["nome"] if "nome" in data else None
    tamanho = data["tamanho"] if "tamanho" in data else None
    sabor1 = data["sabor1"] if "sabor1" in data else None
    sabor2 = data["sabor2"] if "sabor2" in data else None
    num_of_item = 0
    # adiciona pizzas ao carrinho
    if product_nome == "pizza":
        if request.user.is_authenticated:
            item = Pizza.objects.get(sabor=product_id, tamanho=tamanho)
            cart, created = Carrinho.objects.get_or_create(user=request.user, completo=False)
            cartitem, created = PedidoPizza.objects.get_or_create(cart=cart, item=item)
            cartitem.quantidade += 1
            cartitem.save()
            num_of_item = cart.quantidade_total
    # adiciona bebidas ao carrinho
    elif product_nome == "bebida":
        if request.user.is_authenticated:
            item = Bebida.objects.get(id=product_id)
            cart, created = Carrinho.objects.get_or_create(user=request.user, completo=False)
            cartitem, created = PedidoBebida.objects.get_or_create(cart=cart, item=item)
            cartitem.quantidade += 1
            cartitem.save()
            num_of_item = cart.quantidade_total
    # adiciona combos ao carrinho
    elif product_nome == "combo":
        if request.user.is_authenticated:
            item = Combo.objects.get(id=product_id)
            cart, created = Carrinho.objects.get_or_create(user=request.user, completo=False)
            cartitem, created = PedidoCombo.objects.get_or_create(cart=cart, item=item)
            cartitem.quantidade += 1
            cartitem.save()
            num_of_item = cart.quantidade_total
    # adiciona pizza de dois sabores ao carrinho
    elif product_nome == "pizza2sabores":
        if request.user.is_authenticated:
            cart, created = Carrinho.objects.get_or_create(user=request.user, completo=False)
            # se o sabor é o mesmo cadastra uma pizza normal
            if sabor1 == sabor2:
                item = Pizza.objects.get(sabor=sabor1, tamanho=tamanho)
                cartitem, created = PedidoPizza.objects.get_or_create(cart=cart, item=item)
                cartitem.quantidade += 1
                cartitem.save()
                num_of_item = cart.quantidade_total
            # sabores diferentes cadastra pizza de dois sabores
            else:
                # tenta pegar a pizza de dois sabores independente da ordem sdos sabores passada
                try:
                    item = Pizza2Sabores.objects.get(primeiro_sabor=sabor1, segundo_sabor=sabor2, tamanho=tamanho)
                    cartitem, created = PedidoPizza2Sabores.objects.get_or_create(cart=cart, item=item)
                    cartitem.quantidade += 1
                    cartitem.save()
                    num_of_item = cart.quantidade_total
                except:
                    try:
                        item = Pizza2Sabores.objects.get(primeiro_sabor=sabor2, segundo_sabor=sabor1, tamanho=tamanho)
                        cartitem, created = PedidoPizza2Sabores.objects.get_or_create(cart=cart, item=item)
                        cartitem.quantidade += 1
                        cartitem.save()
                        num_of_item = cart.quantidade_total
                    except:
                        messages.success(request, "Ops! Ocorreu algo inesperado")

    return JsonResponse(num_of_item, safe=False)

def remove_from_cart(request):
    data = json.loads(request.body)
    product_id = data["id"]
    product_nome = data["nome"]
    if request.user.is_authenticated:
        cart, created = Carrinho.objects.get_or_create(user=request.user, completo=False)
        if product_nome == "pizza":
            item = cart.cartPizzas.get(id=product_id)
        elif product_nome == "bebida":
            item = cart.cartBebidas.get(id=product_id)
        elif product_nome == "combo":
            item = cart.cartCombos.get(id=product_id)
        elif product_nome == "pizza2sabores":
            item = cart.cartPizza2Sabores.get(id=product_id)
        item.delete()
    context = showItensCarrinho(request)
    context.update(showQtdItensCarrinho(request))
    return JsonResponse(context, safe=False)

# executa o pagamento
def confirmar_pagamento(request):
    # acesso somente para usuário autenticado
    if request.user.is_authenticated:
        cart, created = Carrinho.objects.get_or_create(user=request.user, completo=False)
        cart.completo = True
        cart.save()
        messages.success(request, "Pagamento realizado com sucesso!")
        return redirect("home")
    
    