import BTree as bt
# #Execução
Ap = None
ApAlfa = None
chave = 1

# Menu
print("Bem-vindo, o que deseja realizar?")
menu = True
while menu:
    cmd = int(input("\nMenu de opções\n\n0 - Sair, 1 - Inserir, 2 - Pesquisar, 3 - Imprimir em-ordem, 4 - Imprimir valores menores que uma chave, 5 - Imprimir valores maiores que uma chave, 6 - Buscar por intervalo.\n\nEscolher:"))
    print("\n")

    if cmd == 0:
        print("Programa finalizado. ")
        menu = False
    elif cmd == 1:
        Ap, ApAlfa, chave = bt.Inserir(Ap, ApAlfa, chave)
    elif cmd == 2:
        reg = bt.Registro()
        reg.Chave = input("\nDigite uma chave maior que zero: ")
        if reg.Chave.isnumeric():
            reg.Chave = int(reg.Chave)
            reg = bt.Pesquisa(reg, Ap)
        else:
            reg = bt.Pesquisa(reg, ApAlfa)
        print(reg.Chave, "-", reg.Elemento)
    elif cmd == 3:
        opcao = int(
            input("\n 1 - Arvore numerica, 2 - Arvore alfabetica.\n\nEscolher:"))
        if opcao == 1:
            bt.Imprime(Ap)
        elif opcao == 2:
            bt.Imprime(ApAlfa)
        else:
            print("Comando inexistente.")
    elif cmd == 4:
        reg = bt.Registro()
        reg.Chave = input("\nDigite uma chave maior que zero: ")
        if reg.Chave.isnumeric():
            reg.Chave = int(reg.Chave)
            bt.ImprimeMenor(reg, Ap)
        else:
            bt.ImprimeMenor(reg, ApAlfa)
    elif cmd == 5:
        reg = bt.Registro()
        reg.Chave = input("\nDigite uma chave maior que zero: ")
        if reg.Chave.isnumeric():
            reg.Chave = int(reg.Chave)
            bt.ImprimeMaior(reg, Ap)
        else:
            bt.ImprimeMaior(reg, ApAlfa)
    elif cmd == 6:
        regX = bt.Registro()
        regY = bt.Registro()
        regX.Chave = input("\nDigite a chave inicial: ")
        regY.Chave = input("\nDigite a chave final: ")
        if regX.Chave.isnumeric() and regY.Chave.isnumeric():
            regX.Chave, regY.Chave = int(regX.Chave), int(regY.Chave)
            bt.ImprimeIntervalo(regX, regY, Ap)
        else:
            bt.ImprimeIntervalo(regX, regY, ApAlfa)
    else:
        print("Comando inexistente.")
