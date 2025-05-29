#Colocar tudo em funções e adc função de criar usuário
import textwrap

def saque(*, saldo, valor, extrato, limite, numero_saques, limite_saques): # O caractere * em uma definição de função no Python é usado para tornar os argumentos seguintes obrigatórios e somente nomeados (keyword-only arguments). Isso significa que esses argumentos não podem ser passados como argumentos posicionais, mas devem ser especificados pelo nome ao chamar a função.
    '''Operação de saque.
    Restrição: valor do saque deve ser positivo e menor ou igual ao saldo.
    Pametro por nome (keyword only'''

    excedeu_saldo = valor > saldo
    excedeu_limite = valor > limite
    excedeu_saques = numero_saques >= limite_saques

    if excedeu_saldo:
        print("Saldo insuficiente.")
    
    elif excedeu_limite:
        print("O valor excedeu o limite de saque.")

    elif excedeu_saques:
        print("Número máximo de saques diários excedido.")

    elif valor > 0:
        saldo -= valor
        extrato += f"Saque:\t\tR${valor:.2f}\n"
        numero_saques += 1
        print("Saque realizado com sucesso.")
    
    else:
        print("Valor inválido. O valor do saque deve ser positivo.")
    
    return saldo, extrato

def deposito(saldo, valor, extrato, /): # O caractere / em uma definição de função no Python é usado para indicar argumentos posicionais obrigatórios. Isso significa que os argumentos definidos antes do / só podem ser passados para a função por posição, e não por nome.
    '''Operação de depósito. Valor deve ser positivo, menor ou igual
    ao saldo. Permitido no maximo 3 depositos..
    Parametro por posição (positional only)'''
    
    if valor > 0:
        saldo += valor
        extrato += f"Depósito:\tR${valor:.2f}\n"
        print("\nDepósito realizado com sucesso.")
    else:
        print("Valor inválido.")
    return saldo, extrato


def mostrar_extrato(saldo, /, *, extrato):
    '''Exibe o extrato da conta.
    Parametro por nome (keyword only) e por posição (positional only)'''

    
    print("\n========================== EXTRATO ===============================")
    print("Não foram realizadas movimentações." if not extrato else extrato)
    print(f"\nSaldo:\t\tR${saldo:.2f}")
    print("===================================================================")

def filtrar_usuario(cpf, usuarios):
    '''Filtra um usuário pelo CPF.
    Retorna o usuário se encontrado, caso contrário, retorna None.'''
    usuarios_filtrados = [usuario for usuario in usuarios if usuario["cpf"] == cpf]
    return usuarios_filtrados[0] if usuarios_filtrados else None

def criar_usuario(usuarios):
    '''Cria um novo usuário com nome, data de nascimento, CPF e endereço.'''
    cpf = input("Digite o CPF do usuário (apenas números): ")
    usuario = filtrar_usuario(cpf, usuarios)

    if usuario:
        print("Usuário já cadastrado.")
        return
    
    nome = input("Digite o nome completo: ")
    dt_nascimento = input("Digite a data de nascimento (dd-mm-aaaa): ")
    endereco = input("Digite o endereço (logradouro, número - bairro - cidade/UF): ") 

    usuarios.append({"nome": nome, "dt_nascimento": dt_nascimento, "cpf": cpf, "endereco": endereco})

    print("Usuário criado com sucesso!")

def criar_conta_corrente(agencia, numero_conta, usuarios):
    cpf = input("Digite o CPF do usuário: ")
    usuario = filtrar_usuario(cpf, usuarios)
    if usuario:
        print(f"Conta {numero_conta} criada com sucesso para o usuário {usuario['nome']}!")
        return {"agencia": agencia, "numero_conta": numero_conta, "usuario": usuario}
    
    print("Usuário não encontrado!")

def listar_contas(contas):
    '''Lista todas as contas correntes cadastradas.'''
    print("\n========================== CONTAS ===============================")
    for conta in contas:
        linha = f"""\
        Agência:\t{conta['agencia']}
        Conta:\t{conta['numero_conta']}
        Usuário:\t{conta['usuario']['nome']}
        """

        print("=" * 100)
        print(textwrap.dedent(linha))
    
def menu():
    menu = """ \n
    ====================== MENU ============================
    [1]\tSaque
    [2]\tDepósito
    [3]\tExtrato
    [4]\tNovo usuário
    [5]\tNova conta
    [6]\tListar contas
    [7]\tSair
    => """
    return input(textwrap.dedent(menu))

def main():
    '''Função principal que executa o programa.'''
    LIMITE_SAQUES = 3
    AGENCIA = "0001"

    saldo = 0
    limite = 500
    usuarios = []
    contas = []
    extrato = ""
    numeroSaques = 0

    while True:
        opcao = menu()
        if opcao == '1':
            val = float(input("Digite o valor do saque: "))
            saldo, extrato = saque(saldo=saldo, valor=val, extrato=extrato, limite=limite, numero_saques=numeroSaques, limite_saques=LIMITE_SAQUES)
        
        elif opcao == '2':
            val = float(input("Digite o valor do deposito: "))
            saldo, extrato = deposito(saldo, val, extrato)
        
        elif opcao == '3':
            mostrar_extrato(saldo, extrato=extrato)
        
        elif opcao == '4':
            criar_usuario(usuarios)
        
        elif opcao == '5':
            numero_conta = len(contas) + 1
            conta = criar_conta_corrente(AGENCIA, numero_conta, usuarios)
            if conta:
                contas.append(conta)
        
        elif opcao == '6':
            listar_contas(contas)
            
        elif opcao == '7':
            break

main()