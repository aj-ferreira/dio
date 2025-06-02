#Colocar tudo em funções e adc função de criar usuário
import textwrap
from abc import ABC, abstractmethod
from datetime import datetime

#Anotações

#@classmethod
        #Uso: Define um método que recebe a classe (cls) como primeiro argumento, em vez da instância (self).
        #Objetivo: Permite criar métodos que atuam na classe como um todo, podendo acessar/modificar atributos de classe ou criar instâncias alternativas.

#@property
        #Uso: Define um método que pode ser acessado como um atributo, sem precisar de parênteses.
        #Objetivo: Permite encapsular a lógica de acesso a um atributo, tornando-o mais seguro e controlado.
class Cliente:
    #Always use self as the first parameter in instance methods (including __init__).
    #Use self to refer to instance variables and methods inside the class.
    #If you forget self, Python will raise an error because it won't know which object you're referring to. Always include self in instance methods.
    def __init__(self,endereco):
        self.endereco = endereco
        self.contas = []

    def adicionar_conta(self, conta):
        '''Adiciona uma conta à lista de contas do cliente.'''
        self.contas.append(conta)

    def realizar_transacao(self, conta,transacao):
        transacao.registrar(conta)
        
class PessoaFisica(Cliente):
    def __init__(self, nome, dt_nascimento, cpf, endereco):
        super().__init__(endereco)
        self.nome = nome
        self.dt_nascimento = dt_nascimento
        self.cpf = cpf

    @property
    def idade(self):
        '''Calcula a idade do cliente.'''
        nascimento = datetime.strptime(self.dt_nascimento, "%d-%m-%Y")
        hoje = datetime.now()
        return hoje.year - nascimento.year - ((hoje.month, hoje.day) < (nascimento.month, nascimento.day))

class Conta:
    def __init__(self, numero_conta, cliente):
        self._saldo = 0
        self._numero_conta = numero_conta
        self._agencia = "0001"
        self._cliente = cliente
        self._historico = Historico()

    @classmethod
    def criar_conta(cls, numero_conta, cliente):
        '''Método de classe para criar uma nova conta.'''
        return cls(numero_conta, cliente)
    
    @property
    def saldo(self):
        '''Retorna o saldo da conta.'''
        return self._saldo
    
    @property
    def numero_conta(self):
        '''Retorna o número da conta.'''
        return self._numero_conta
    
    @property
    def agencia(self):
        '''Retorna o número da agência.'''
        return self._agencia
    
    @property
    def cliente(self):
        '''Retorna o cliente associado à conta.'''
        return self._cliente
    
    @property
    def historico(self):
        '''Retorna o histórico de transações da conta.'''
        return self._historico
    
    def sacar(self, valor):
        '''Realiza um saque na conta.'''
        saldo = self.saldo
        excedeu_saldo = valor > saldo
        if excedeu_saldo:
            print("Saldo insuficiente para realizar o saque.")
        
        elif valor > 0:
            self._saldo -= valor
            print("Saque realizado com sucesso.")
            return True
        
        else:
            print("Valor inválido. O valor do saque deve ser positivo.")
        
        return False
    
    def depositar(self, valor):
        '''Realiza um depósito na conta.'''
        if valor > 0:
            self._saldo += valor
            print("Depósito realizado com sucesso.")
        
        else:
            print("Valor inválido. O valor do depósito deve ser positivo.")
            return False
    
        return True

class ContaCorrente(Conta):
    def __init__(self, numero_conta, cliente, limite=500, limite_saques=3):
        super().__init__(numero_conta, cliente)
        self._limite = limite
        self._limite_saques = limite_saques

    def sacar(self, valor):
        numero_saques = len([transacao for transacao in self.historico.transacoes if transacao["tipo"] == Saque.__name__])
        excedeu_limite = valor > self._limite
        excedeu_saques = numero_saques >= self._limite_saques

        if excedeu_limite:
            print("O valor excedeu o limite de saque.")

        elif excedeu_saques:
            print("Número máximo de saques diários excedido.")

        else:
            return super().sacar(valor)
        
        return False
    
    def __str__(self):
        return f"""C/C:\t{self.numero_conta} - Agência:\t{self.agencia} - Cliente:\t{self.cliente.nome} - Saldo:\tR${self.saldo:.2f}"""

class Historico:
    def __init__(self):
        self._transacoes = []

    @property
    def transacoes(self):
        '''Retorna as transações do histórico.'''
        return self._transacoes
    
    def adicionar_transacao(self, transacao):
        '''Registra uma transação no histórico.'''
        self._transacoes.append(
            {
                "tipo": transacao.__class__.__name__,
                "valor": transacao.valor,
                "data": datetime.now().strftime("%d-%m-%Y %H:%M:%S")
            }
        )

class Transacao(ABC):
    @property
    @abstractmethod
    def valor(self):
        pass

    @abstractmethod
    def registrar(self, conta):
        pass

class Saque(Transacao):
    def __init__(self, valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor

    def registrar(self, conta):
        sucesso_transacao = conta.sacar(self.valor)

        if sucesso_transacao:
            conta.historico.adicionar_transacao(self)

class Deposito(Transacao):
    def __init__(self, valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor

    def registrar(self, conta):
        sucesso_transacao = conta.depositar(self.valor)

        if sucesso_transacao:
            conta.historico.adicionar_transacao(self)

def sacar(clientes):
    '''Operação de saque.
    Restrição: valor do saque deve ser positivo e menor ou igual ao saldo.
    Pametro por nome (keyword only'''

    cpf = input("Digite o CPF do usuário: ")
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print("Cliente não encontrado.")
        return
    
    valor = float(input("Digite o valor do saque: R$"))
    transacao = Saque(valor)

    conta = recuperar_conta_cliente(cliente)
    if not conta:
        print("Conta não encontrada para o cliente.")
        return
    
    cliente.realizar_transacao(conta, transacao)

def recuperar_conta_cliente(cliente):
    '''Recupera a conta do cliente.'''
    if not cliente.contas:
        print("Cliente não possui contas cadastradas.")
        return
    
    # FIXME: não permitir que o cliente escolha uma conta
    return cliente.contas[0]  # Retorna a primeira conta do cliente

def depositar(clientes): 
    '''Operação de depósito. Valor deve ser positivo, menor ou igual
    ao saldo. Permitido no maximo 3 depositos..
    Parametro por posição (positional only)'''
    cpf = input("Digite o CPF do usuário: ")
    cliente = filtrar_cliente(cpf, clientes)
    
    if not cliente:
        print("Cliente não encontrado.")
        return
    
    valor = float(input("Digite o valor do depósito: R$"))
    transacao = Deposito(valor)

    conta = recuperar_conta_cliente(cliente)

    if not conta:
        print("Conta não encontrada para o cliente.")
        return

    cliente.realizar_transacao(conta, transacao)

def mostrar_extrato(clientes):
    cpf = input("Digite o CPF do usuário: ")
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print("Cliente não encontrado.")
        return
    
    conta = recuperar_conta_cliente(cliente)
    if not conta:
        print("Conta não encontrada para o cliente.")
        return  
    
    print("\n========================== EXTRATO ===============================")
    transações = conta.historico.transacoes

    extrato = ""
    if not transações:
        extrato = "Não foram realizadas movimentações."
    else:
        for transacao in transações:
            extrato += f"{transacao['tipo']}:\tR${transacao['valor']:.2f} - Data: {transacao['data']}\n"

    print(extrato)
    print(f"\nSaldo:\t\tR${conta.saldo:.2f}")
    print("===================================================================")
    

def filtrar_cliente(cpf, clientes):
    '''Filtra um usuário pelo CPF.
    Retorna o usuário se encontrado, caso contrário, retorna None.'''
    clientes_filtrados = [cliente for cliente in clientes if cliente.cpf == cpf]
    return clientes_filtrados[0] if clientes_filtrados else None

def criar_cliente(clientes):
    '''Cria um novo usuário com nome, data de nascimento, CPF e endereço.'''
    cpf = input("Digite o CPF do usuário (apenas números): ")
    cliente = filtrar_cliente(cpf, clientes)

    if cliente:
        print("cliente já cadastrado nesse cpf.")
        return
    
    nome = input("Digite o nome completo: ")
    dt_nascimento = input("Digite a data de nascimento (dd-mm-aaaa): ")
    endereco = input("Digite o endereço (logradouro, número - bairro - cidade/UF): ") 

    cliente = PessoaFisica(nome = nome, dt_nascimento = dt_nascimento, cpf = cpf, endereco = endereco)
    clientes.append(cliente)
    print("Usuário criado com sucesso!")

def criar_conta_corrente( numero_conta, clientes, contas):
    cpf = input("Digite o CPF do cliente: ")
    cliente = filtrar_cliente(cpf, clientes)
    
    if not cliente:
        print("Cliente não encontrado.")
        return 
    
    conta = ContaCorrente.criar_conta(cliente = cliente, numero_conta = numero_conta)
    contas.append(conta)
    cliente.contas.append(conta)

    print(f"Conta {numero_conta} criada com sucesso para o cliente {cliente.nome}!")

def listar_contas(contas):
    '''Lista todas as contas correntes cadastradas.'''
    print("\n========================== CONTAS ===============================")
    for conta in contas:
        print("=" * 100)
        print(textwrap.dedent(str(conta)))
    
def menu():
    menu = """ \n
    ====================== MENU ============================
    [s]\tSaque
    [d]\tDepósito
    [e]\tExtrato
    [nu]\tNovo usuário
    [nc]\tNova conta
    [lc]\tListar contas
    [q]\tSair
    => """
    return input(textwrap.dedent(menu))

def main():
    '''Função principal que executa o programa.'''
    clientes = []
    contas = []


    while True:
        opcao = menu()
        if opcao == 's':
            sacar(clientes)
        
        elif opcao == 'd':
            depositar(clientes)
        
        elif opcao == 'e':
            mostrar_extrato(clientes)
        
        elif opcao == 'nu':
            criar_cliente(clientes)
        
        elif opcao == 'nc':
            numero_conta = len(contas) + 1
            criar_conta_corrente( numero_conta, clientes, contas)
        
        elif opcao == 'lc':
            listar_contas(contas)
            
        elif opcao == 'q':
            break

main()