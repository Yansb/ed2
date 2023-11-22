from igraph import Graph, plot
import pandas as pd
import Grafo as gf



def main():
    print("\nMenu:")
    print("1. Adicionar Pessoa")
    print("2. Adicionar Relacionamento")
    print("3. Remover Relacionamento")
    print("4. Buscar Pessoa")
    print("5. Excluir Pessoa da rede")
    print("6. Listar Nomes em Ordem Alfabética")
    print("7. Maior numero de relacionamentos")
    print("8. Menor numero de relacionamentos")
    print("9. Menor distancia entre pessoas")
    print("0. Sair")
    opcao = input("Escolha uma opção (1/2/3/4/5/6/7/8/9/0): ")


    if opcao == "1":
        nome = input("Digite o nome da pessoa: ")
        idade = int(input("Digite a idade: "))
        ocupacao = input("Digite a ocupação: ")
        gf.add_pessoa(nome, idade, ocupacao)
    elif opcao == "2":
        nome = input("Digite o nome da pessoa: ")
        nome_relacionado = input("Digite o nome do relacionamento: ")
        gf.add_relacionamento(nome, nome_relacionado)
    elif opcao == "3":
        nome = input("Digite o nome da pessoa: ")
        nome_relacionado = input("Digite o nome do relacionamento: ")
        gf.remove_relacionamento(nome, nome_relacionado)
    elif opcao == "4":
        nome = input("Digite o nome da pessoa: ")
        gf.buscar_pessoa(nome)
    elif opcao == "5":
        nome = input("Digite o nome da pessoa: ")
        gf.excluir_da_rede(nome)
    elif opcao =="6":
        gf.listar_nomes()
    elif opcao == "7":
        gf.maior_grau()
    elif opcao == "8":
        gf.menor_grau()
    elif opcao == "9":
        x = input("Digite o nome da pessoa 1: ")
        y = input("Digite o nome da pessoa 2: ")
        gf.menor_distancia(x, y)
    elif opcao == "0":
        gf.salvar_rede_social("./rede_social.csv")
        print("Saindo do programa. Obrigado!")
        exit()
    else:
        print("Opção inválida. Tente novamente.")
    main()

gf.criar_grafo("./rede_social.csv")
gf.imprimir_grafo()
main()
