from django.db import models

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

class Pizza(models.Model):
    nome = models.CharField(max_length=50)
    preco = models.DecimalField(max_digits=5, decimal_places=2)
    imagem = models.ImageField(null=True)
    tamanho = models.ForeignKey(Tamanho, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f"Nome: {self.nome}, Preço: R${self.preco}"

    def __repr__(self) -> str:
        return str(self)

class Ingredientes(models.Model):
    nome = models.CharField(max_length=50)

    def __str__(self) -> str:
        return f"Nome: {self.nome}"

    def __repr__(self) -> str:
        return str(self)

# conecta pizzas a ingredientes (relação N por N)
class composicao(models.Model):
    fk_pizza = models.ForeignKey(Pizza, on_delete=models.CASCADE)
    fk_ingredientes = models.ForeignKey(Ingredientes, on_delete=models.CASCADE)

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

class Bebida(models.Model):
    nome = models.CharField(max_length=50)
    tipo = models.ForeignKey(TipoBebida, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f"Nome: {self.nome}"

    def __repr__(self) -> str:
        return str(self)

class Pedido(models.Model):
    codigo = models.CharField(max_length=10)
    data = models.DateTimeField()
    total = models.DecimalField(max_digits=8, decimal_places=2)
    fk_pizza = models.ForeignKey(Pizza, on_delete=models.CASCADE)
    fk_bebida = models.ForeignKey(Bebida, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f"Código: {self.codigo} Data: {self.data} Total: R${self.total}"

    def __repr__(self) -> str:
        return str(self)

class Endereco(models.Model):
    bairro = models.CharField(max_length=50)
    rua = models.CharField(max_length=50)
    numero = models.IntegerField()
    complemento = models.CharField(max_length=20, null=True)
    CEP = models.CharField(max_length=8)

    def __str__(self) -> str:
        return f"Bairro: {self.bairro} Rua: {self.rua}"

    def __repr__(self) -> str:
        return str(self)
    
class Cliente(models.Model):
    nome = models.CharField(max_length=50)
    telefone = models.CharField(max_length=13)
    fk_pedidos = models.ForeignKey(Pedido, on_delete=models.CASCADE)
    fk_endereco = models.ForeignKey(Endereco, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f"Nome: {self.nome} Telefone: {self.telefone}"

    def __repr__(self) -> str:
        return str(self)
