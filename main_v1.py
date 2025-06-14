from abc import ABC, abstractclassmethod, abstractproperty
from datetime import datetime

class Cliente:

    def __init__(self, endereco):
        self.endereco = endereco
        self.contas = []

    def realizar_trasacao(self,conta, transacao):
        transacao.registrar(conta)

    
    def adicionar_conta(self, conta):
        self.contas.append(conta)



class PessoaFisica(Cliente):

    def __init__(self, endereco, cpf, nome, data_nascimento):

        super().__init__(endereco)
        self.cpf = cpf
        self.nome = nome
        self.data_nascimento = data_nascimento


class Conta:

    def __init__(self, numero, cliente):
        self.saldo = 0.0
        self.numero = numero
        self.cliente = cliente
        self.saldo = 0.0
        self.agencia = "0001"
        self.historico = Historico()

    @classmethod
    def nova_conta(cls, cliente, numero):
        return cls(numero, cliente)


    def sacar(self, valor):
        saldo = self.saldo
        excedeu_saldo = valor > saldo

        if excedeu_saldo == True:
            print("\nOperação Recusada! Não há saldo suficiente disponível.")

        elif valor > 0:
            self.saldo -= valor
            print(f"\nSaque de R$ {valor:.2f} realizado com sucesso!")

        else:
            print("\nOperação Recusada! Por gentileza, verifique o valor inserido e tente novamente.")

        return False
    

    def depositar(self, valor):

        if valor > 0:
            self.saldo += valor
            print(f"\nDepósito de R$ {valor:.2f} realizado com sucesso!")

        else:
            print("\nOperação Recusada! Por gentileza, verifique o valor inserido e tente novamente.")
            return False

        return True


class ContaCorrente(Conta):
    
    def __init__(self, numero, cliente, limite_valor_saque = 500, limite_saques_diario = 3):
        super().__init__(numero, cliente)
        self.limite_valor_saque = limite_valor_saque
        self.limite_saques_diario = limite_saques_diario
        

    def sacar(self, valor):
        numero_saques = len(
            [transacao for transacao in self.historico.transacoes 
                if transacao["tipo"] == Saque.__name__])

        excedeu_limite = valor > self.limite_valor_saque
        excedeu_saques = numero_saques >= self.limite_saques_diario

        if excedeu_limite:
            print("\nOperação Recusada! Saque solicitado ultrapassa o limite permitido.")

        elif excedeu_saques:
            print("\nOperação Recusada! Número máximo de saques diários excedido.")

        else:
            return super().sacar(valor)
        
        return False

class Transacao(ABC):

    def valor(self):
        pass

    def registrar(self, conta):
        pass


class Saque(Transacao):
    
    def __init__(self, valor):
        self.valor = valor

    def registrar(self, conta):
        sucesso_transacao = conta.sacar(self.valor)

        if sucesso_transacao:
            conta.historico.adicionar_transacao(self)


class Deposito(Transacao):

    def __init__(self, valor):
        self.valor = valor

    def registrar(self, conta):
        sucesso_transacao = conta.depositar(self.valor)

        if sucesso_transacao:
            conta.historico.adicionar_transacao(self)


class Historico:

    def __init__(self):
        self.transacoes = []
    
    def  adicionar_transacao(self, transacao):
        self.transacoes.append(
            {"tipo": transacao.__class__.__name__,
             "valor": transacao.valor,
             "data": datetime.now().strftime("%d-%m-%Y %H:%M:%s")})
        
