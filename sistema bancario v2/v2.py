from datetime import datetime, timedelta, date

depositos = []
saques = []
saldo = 0
limite = 500
hoje = date.today() # + timedelta(days=0) para simular outro dia
contadorDeOperacoes = 0
maxOperacoes = 10
mascara_ptbr = "%d/%m/%Y %a"

def saque():
    '''Operação de saque.
    Restrição: valor do saque deve ser positivo e menor ou igual ao saldo.'''
    global saldo
    global contadorDeOperacoes
    global hoje
    if len(saques) <= 3 and contadorDeOperacoes < maxOperacoes and hoje == date.today():
        valor = float(input("Digite o valor do saque: "))
        if valor <= saldo and valor > 0 and valor <= limite:
            saques.append([valor, (datetime.today().strftime(mascara_ptbr))])
            saldo -= valor
            contadorDeOperacoes += 1
            print("Saque realizado com sucesso.")
        else:
            print("Saldo insuficiente.")
    else:
        print("Limite de saques diários atingido.")
    return

def deposito():
    '''Operação de depósito. Valor deve ser positivo, menor ou igual
    ao saldo.'''
    global saldo
    global contadorDeOperacoes
    global hoje
    if contadorDeOperacoes < maxOperacoes and hoje == date.today():
        valor = float(input("Digite o valor do depósito: "))
        if valor >= 0:
            depositos.append([valor,(datetime.today().strftime(mascara_ptbr))])
            saldo += valor
            contadorDeOperacoes += 1
            print("Depósito realizado com sucesso.")
        else:
            print("Valor inválido.")
    else:
        print("Limite de operações diárias atingido.")
    return


def extrato():
    '''Exibe o extrato da conta.'''
    print("=========================================================")
    print("                  Extrato Bancário                       ")
    print("=========================================================")
    if(len(depositos) == 0 and len(saques) == 0):
        print()
        print("Nenhuma operação realizada.")
    else:
        print("\nDepósitos: ")
        for val,date in depositos:
            print( "+ R$"+str(val).format('%.2f') + " em " + date)
        print("--------------------")

        print("\nSaques: ")
        for val,date in saques:
            print("- R$"+str(val).format('%.2f') + " em " + date)
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