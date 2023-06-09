from django.contrib import admin
from django.urls import path
from Pizzaria_Mamma_Mia.views import *
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path("", Home.as_view(), name="home"),
    path("cardapio/", Cardapio.as_view(), name="cardapio"),
    path("cardapio/add_to_cart/", add_to_cart, name="add_to_cart"),
    path("montar-pizza/", MontarPizza.as_view(), name="montar-pizza"),
    path("montar-pizza/add_to_cart/", add_to_cart, name="montar-pizza-add-to-cart"),
    path("carrinho/", CarrinhoView.as_view(), name="carrinho"),
    path("carrinho/remove_from_cart/", remove_from_cart, name="remove_from_cart"),
    path("login/", Login.as_view(), name="login"),
    path("conta/", Conta.as_view(), name="conta"),
    path("editar-conta/", editarConta, name="editar-conta"),
    path("dologout/", doLogout, name="dologout"),
    path("dologin/", doLogin, name="dologin"),
    path('admin/', admin.site.urls),
    path('cadastro/', Cadastro.as_view(), name="cadastrar"),
    path('store/', store, name="store"),
    path('pagar/', Pagar.as_view(), name='pagar'),
    path("confirmar_pagamento/", confirmar_pagamento, name="confirmar_pagamento")
] + static (settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
