from Pizzaria_Mamma_Mia.models import *

"""
FUNÇÕES AUXILIARES DO VIEWS
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
    campos = ["email", "password", "first_name", "last_name", "telefone", "bairro", "rua", "cep", "numero", "complemento"]
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
                    'id': obj['id'],
                    'nome': obj['nome'],
                    'imagem': obj['imagem'],
                    'ingredientes': [obj['composicao__fk_ingrediente__nome']]
                }
            )
    return out

# mostra dados da conta do usuário
def dadosConta(request):
    user = User.objects.all().get(email=request.user.email)
    cliente = Cliente.objects.all().get(fk_user=user.id)
    endereco = Endereco.objects.all().get(id=cliente.fk_endereco.id)
    bairro = Bairro.objects.all().get(id=endereco.fk_bairro.id)
    return {
        "user": user,
        "telefone": cliente,
        "endereco": endereco,
        "bairro": bairro,
    }

# mostra menssagens de alerta e confirmação
def showMsg(request):
    msg=None
    _class=None
    if 'msg' in request.session:
        msg = request.session['msg']
        _class = request.session['class']
        request.session["msg"] = None
        request.session["class"] = None
    return {"msg": msg, "class": _class}

# mostra quantos itens estão do carrinho no icone do carrinho
def showQtdItensCarrinho(request):
    cart = {
        "num_of_items": 0
    }
    if request.user.is_authenticated:
        cart_user, created = Carrinho.objects.get_or_create(user=request.user, completo=False)
        cart['num_of_items'] = cart_user.quantidade_total
        
    return {"cart": cart}

# mostra os produtos que estão no carrinho
def showItensCarrinho(request):
    lst_itens = []
    total = None

    # pega o usuário
    if request.user.is_authenticated:
        cart_user, created = Carrinho.objects.get_or_create(user=1, completo=False)
        total = cart_user.preco_total

        # adiciona as bebidas ao carrinho
        for item in list(cart_user.cartBebidas.all()):
            lst_itens.append({
                "nome": item.item.nome,
                "qtd": item.quantidade,
                "preco": item.item.preco,
            })

        # adiciona as pizzas
        for item in list(cart_user.cartPizzas.all()):
            lst_itens.append({
                "nome": item.item.nome,
                "qtd": item.quantidade,
                "preco": item.item.preco,
                "tamanho": item.item.tamanho.tamanho,
            })

        # adiciona as pizzas 2 sabores
        for item in list(cart_user.cartPizza2Sabores.all()):
            lst_itens.append({
                "nome": item.item.nome,
                "qtd": item.quantidade,
            })

        # adiciona os combos
        for item in list(cart_user.cartCombos.all()):
            lst_itens.append({
                "nome": item.item.descricao,
                "qtd": item.quantidade,
            })
        
    return {"itens": lst_itens, "total": total}

