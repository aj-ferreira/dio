depositos = []
saques = []
saldo = 0
limite = 500

def saque():
    '''Operação de saque.
    Restrição: valor do saque deve ser positivo e menor ou igual ao saldo.'''
    global saldo
    if len(saques) <= 3:
        valor = float(input("Digite o valor do saque: "))
        if valor <= saldo and valor > 0 and valor <= limite:
            saques.append(valor)
            saldo -= valor
            print("Saque realizado com sucesso.")
        else:
            print("Saldo insuficiente.")
    else:
        print("Limite de saques diários atingido.")
    return

def deposito():
    '''Operação de depósito. Valor deve ser positivo, menor ou igual
    ao saldo. Permitido no maximo 3 depositos..'''
    global saldo
    valor = float(input("Digite o valor do depósito: "))
    if valor >= 0:
        depositos.append(valor)
        saldo += valor
        print("Depósito realizado com sucesso.")
    else:
        print("Valor inválido.")
    return


def extrato():
    '''Exibe o extrato da conta.'''
    if(len(depositos) == 0 and len(saques) == 0):
        print("Nenhuma operação realizada.")
    else:
        print("Depósitos: ")
        for i in depositos:
            print( "+ R$"+str(i).format('%.2f'))
        print("--------------------")

        print("Saques: ")
        for i in saques:
            print("- R$"+str(i).format('%.2f'))
        print("--------------------")

        print("Saldo: R$"+str(saldo).format('%.2f'))
        print()
    return

while True:
    print("1 - Saque")
    print("2 - Depósito")
    print("3 - Extrato")
    print("4 - Sair")
    opcao = int(input("Digite a opção desejada: "))
    if opcao == 1:
        saque()
    elif opcao == 2:
        deposito()
    elif opcao == 3:
        extrato()
    elif opcao == 4:
        break
    else:
        print("Opção inválida, tente novamente.")