from django.db import models
from django.contrib.auth.models import User
    
class Sabor(models.Model):
    nome = models.CharField(max_length=50, unique=True)
    imagem = models.ImageField(null=True)

    def __str__(self) -> str:
        return f"Nome: {self.nome}"

    def __repr__(self) -> str:
        return str(self)
    
class Ingrediente(models.Model):
    nome = models.CharField(max_length=50, unique=True)

    def __str__(self) -> str:
        return f"Nome: {self.nome}"

    def __repr__(self) -> str:
        return str(self)

# conecta sabores a ingredientes (relação N por N)
class Composicao(models.Model):
    fk_sabor = models.ForeignKey(Sabor, on_delete=models.CASCADE)
    fk_ingrediente = models.ForeignKey(Ingrediente, on_delete=models.CASCADE)

class Tamanho(models.Model):
    GIGANTE = "gigante"
    GRANDE = "grande"
    MEDIA = "media"

    TIPO_TAMANHO = [
        (GIGANTE, "gigante"),
        (GRANDE, "grande"),
        (MEDIA, "media"),
    ]

    tamanho = models.CharField(max_length=7, choices=TIPO_TAMANHO)

    def __str__(self) -> str:
        return f"Nome: {self.tamanho}"

    def __repr__(self) -> str:
        return str(self)

class Pizza(models.Model):
    nome = models.CharField(max_length=50)
    preco = models.DecimalField(max_digits=5, decimal_places=2)
    tamanho = models.ForeignKey(Tamanho, on_delete=models.CASCADE)
    sabor = models.ForeignKey(Sabor, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f"Nome: {self.nome} Preço: R${self.preco} Tamanho: {self.tamanho.tamanho}"

    def __repr__(self) -> str:
        return str(self)
    
class Pizza2Sabores(models.Model):
    nome = models.CharField(max_length=100)
    preco = models.DecimalField(max_digits=5, decimal_places=2)
    tamanho = models.ForeignKey(Tamanho, on_delete=models.CASCADE)
    primeiro_sabor = models.ForeignKey(Sabor, on_delete=models.CASCADE, related_name="primeiro_sabor")
    segundo_sabor = models.ForeignKey(Sabor, on_delete=models.CASCADE, related_name="segundo_sabor")

    def __str__(self) -> str:
        return f"Nome: {self.nome} Preço: R${self.preco} Tamanho: {self.tamanho.tamanho}"

    def __repr__(self) -> str:
        return str(self)

class TipoBebida(models.Model):
    REFRIGERANTE = "Refrigerante"
    SUCO = "suco"
    AGUA = "água"

    TIPO_BEBIDAS = [
        (REFRIGERANTE, "Refrigerante"),
        (SUCO, "suco"),
        (AGUA, "água"),
    ]

    name = models.CharField(max_length=12, choices=TIPO_BEBIDAS)

    def __str__(self) -> str:
        return f"Nome: {self.name}"

    def __repr__(self) -> str:
        return str(self)

class Bebida(models.Model):
    nome = models.CharField(max_length=50, unique=True)
    imagem = models.ImageField(null=True)
    preco = models.DecimalField(max_digits=5, decimal_places=2)
    tipo = models.ForeignKey(TipoBebida, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f"Nome: {self.nome}  Preço: R${self.preco}"

    def __repr__(self) -> str:
        return str(self)
    
class Combo(models.Model):
    descricao = models.CharField(max_length=100, unique=True)
    preco = models.DecimalField(max_digits=5, decimal_places=2)
    imagem = models.ImageField(null=True)
    fk_pizza_1 = models.ForeignKey(Pizza, on_delete=models.CASCADE, null=True, related_name="pizza_1")
    fk_pizza_2 = models.ForeignKey(Pizza, on_delete=models.CASCADE, null=True, related_name="pizza_2")
    fk_bebida = models.ForeignKey(Bebida, on_delete=models.CASCADE, null=True)

class Bairro(models.Model):
    nome = models.CharField(max_length=50, unique=True)

    def __str__(self) -> str:
        return f"Nome: {self.nome}"

    def __repr__(self) -> str:
        return str(self)

class Endereco(models.Model):
    rua = models.CharField(max_length=50)
    numero = models.IntegerField()
    complemento = models.CharField(max_length=20, null=True)
    CEP = models.CharField(max_length=8)
    fk_bairro = models.ForeignKey(Bairro, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f"Rua: {self.rua} numero: {self.numero} complemento: {self.complemento} CEP: {self.CEP}"

    def __repr__(self) -> str:
        return str(self)
    
class Cliente(models.Model):
    telefone = models.CharField(max_length=13)
    fk_endereco = models.ForeignKey(Endereco, on_delete=models.CASCADE)
    fk_user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f"Telefone: {self.telefone}"

    def __repr__(self) -> str:
        return str(self)
    
class Carrinho(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    completo = models.BooleanField(default=False)
    
    @property
    def quantidade_total(self):
        cartPizzas = self.cartPizzas.all()
        cartBebidas = self.cartBebidas.all()
        cartPizza2Sabores = self.cartPizza2Sabores.all()
        cartCombos = self.cartCombos.all()
        quantidade = 0
        quantidade += sum([item.quantidade for item in cartPizzas])
        quantidade += sum([item.quantidade for item in cartBebidas])
        quantidade += sum([item.preco for item in cartCombos])
        quantidade += sum([item.preco for item in cartPizza2Sabores])
        return quantidade
    
    @property
    def preco_total(self):
        cartPizzas = self.cartPizzas.all()
        cartBebidas = self.cartBebidas.all()
        cartPizza2Sabores = self.cartPizza2Sabores.all()
        cartCombos = self.cartCombos.all()
        total = 0
        total += sum([item.preco for item in cartPizzas])
        total += sum([item.preco for item in cartBebidas])
        total += sum([item.preco for item in cartCombos])
        total += sum([item.preco for item in cartPizza2Sabores])
        return total
    
    def __str__(self) -> str:
        return f"{self.id} usuário: {self.user} {self.completo}"

    def __repr__(self) -> str:
        return str(self)
    

class PedidoPizza(models.Model):
    item = models.ForeignKey(Pizza, on_delete=models.CASCADE, null=True)
    cart = models.ForeignKey(Carrinho, on_delete= models.CASCADE, related_name="cartPizzas")
    quantidade = models.IntegerField(default=0)
    
    def __str__(self):
        return self.item.nome
    
    @property
    def preco(self):
        novo_preco = self.item.preco * self.quantidade
        return novo_preco
    
class PedidoBebida(models.Model):
    item = models.ForeignKey(Bebida, on_delete=models.CASCADE, null=True)
    cart = models.ForeignKey(Carrinho, on_delete= models.CASCADE, related_name="cartBebidas")
    quantidade = models.IntegerField(default=0)
    
    def __str__(self):
        return self.item.nome
    
    @property
    def preco(self):
        novo_preco = self.item.preco * self.quantidade
        return novo_preco
    
class PedidoCombo(models.Model):
    item = models.ForeignKey(Combo, on_delete=models.CASCADE, null=True)
    cart = models.ForeignKey(Carrinho, on_delete= models.CASCADE, related_name="cartCombos")
    quantidade = models.IntegerField(default=0)
    
    def __str__(self):
        return self.item.descricao
    
    @property
    def preco(self):
        novo_preco = self.item.preco * self.quantidade
        return novo_preco
    
class PedidoPizza2Sabores(models.Model):
    item = models.ForeignKey(Pizza2Sabores, on_delete=models.CASCADE, null=True)
    cart = models.ForeignKey(Carrinho, on_delete= models.CASCADE, related_name="cartPizza2Sabores")
    quantidade = models.IntegerField(default=0)
    
    def __str__(self):
        return self.item.nome
    
    @property
    def preco(self):
        novo_preco = self.item.preco * self.quantidade
        return novo_preco
    


