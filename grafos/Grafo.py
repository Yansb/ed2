import csv
import time
import csv
from IPython.display import clear_output
from math import *
import pandas as pd
from igraph import Graph, plot

from igraph import plot

rede_social = {} #criando dic da rede social
def inicializar_rede_social():
    pessoas =  pd.read_csv("./rede_social.csv")


def criar_grafo(file_path):
    # carregar dados do CSV
    data = pd.read_csv(file_path)

    G = Graph(directed=False)

    # adicionar nós ao grafo com os dados das pessoas
    for _, person in data.iterrows():
        G.add_vertex(name=person['Nome'], idade=person['Idade'], ocupacao=person['Ocupacao'])
        rede_social[person['Nome']] = {"idade": person['Idade'], "ocupacao": person['Ocupacao'], "lista": []}

    # adicionar arestas ao grafo com os relacionamentos
    arestas_adicionadas = set()

    for _, relationship in data.iterrows():
        if pd.notna(relationship['Relacionamentos']):
            rede_social[relationship['Nome']]['lista'] = relationship['Relacionamentos'].split(',')

            for rel in relationship['Relacionamentos'].split(','):
                rel = rel.strip()
                aresta_atual = (relationship['Nome'], rel)
                aresta_invertida = (rel, relationship['Nome'])

                # Verificar se a aresta já foi adicionada (nos dois sentidos) para evitar duplicatas
                if aresta_atual not in arestas_adicionadas and aresta_invertida not in arestas_adicionadas:
                    G.add_edge(relationship['Nome'], rel)
                    arestas_adicionadas.add(aresta_atual)
                    arestas_adicionadas.add(aresta_invertida)
        else:
            rede_social[relationship['Nome']]['lista'] = []

    return G

def add_pessoa(nome, idade, ocupacao):
    pessoa ={#criando dic de pessoa
        "idade": idade,
        "ocupacao": ocupacao,
        "lista": [] #inicializa com a lista de relacionamentos vazia
    }
    rede_social[nome]=pessoa#inicializa dic com pessoa como chave
    salvar_rede_social("./rede_social.csv")
    imprimir_grafo()

def carregar_dados_csv(nome_arquivo):
  with open(nome_arquivo, mode='r', newline='', encoding='iso-8859-1') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            nome = row["Nome"]
            idade = row["Idade"]
            ocupacao = row["Ocupacao"]
            relacionamentos = row["Relacionamentos"].split(",") if row["Relacionamentos"] else []

            add_pessoa(nome, idade, ocupacao)  # Adiciona a pessoa ao dicionário
            for relacionado in relacionamentos:#no caso de arquivos carregados do csv
                add_relacionamentoimport(nome, relacionado)

def add_relacionamento(nome, nome_relacionado):
    if nome in rede_social and nome_relacionado in rede_social:#teste para ver se a pessoa esta na rede social
        if nome_relacionado not in rede_social[nome]["lista"]:#se relacionamento ja existir
            rede_social[nome]["lista"].append(nome_relacionado)
            rede_social[nome_relacionado]["lista"].append(nome)
            salvar_rede_social("./rede_social.csv")
            imprimir_grafo()
        else:
            print(f"{nome_relacionado} já está na lista de relacionamentos de {nome}")
    else:
        print("ERRO: não é possivel adicionar uma pessoa não cadastrada na rede")

def add_relacionamentoimport(nome, nome_relacionado):
    if nome in rede_social:
        if nome_relacionado not in rede_social:
            # Adiciona a pessoa relacionada à rede social se ainda não estiver cadastrada
            rede_social[nome_relacionado] = {"lista": []}

        if nome_relacionado not in rede_social[nome]["lista"]:
            # Adiciona o relacionamento se ainda não existir
            rede_social[nome]["lista"].append(nome_relacionado)
            rede_social[nome_relacionado]["lista"].append(nome)
        else:
            print(f"{nome_relacionado} já está na lista de relacionamentos de {nome}")

def remove_relacionamento(nome, nome_relacionado):
    if nome in rede_social and nome_relacionado in rede_social:
        if nome_relacionado in rede_social[nome]["lista"]:
            rede_social[nome]["lista"].remove(nome_relacionado)
            rede_social[nome_relacionado]["lista"].remove(nome)
            salvar_rede_social("./rede_social.csv")
            imprimir_grafo()
        else:
            print(f"{nome_relacionado} não está na lista de relacionamentos de {nome}")
    else:
        print("ERRO: não é possível remover uma pessoa não cadastrada na rede")

def buscar_pessoa(nome):
    if nome in rede_social:
        pessoa = rede_social[nome]#buscar pessoa pela chave(nome)
        print("-----------------------------------")
        print(f"Nome: {nome}")
        print(f"Idade: {pessoa['idade']}")
        print(f"Ocupação: {pessoa['ocupacao']}")
        print("Relacionamentos:")
        for relacionado in pessoa['lista']:
            print(f"- {relacionado}")
        print("-----------------------------------")
    else:
        print(f"{nome} não foi encontrado na rede social.")

def excluir_da_rede(nome):
    if nome in rede_social:
        remover_rel = rede_social[nome]["lista"]
        for pessoa in remover_rel:
          if pessoa in rede_social:
            rede_social[pessoa]["lista"].remove(nome)
        del rede_social[nome]
        salvar_rede_social("./rede_social.csv")
        imprimir_grafo()
    else:
         print(f"{nome} não foi encontrado na rede social.")

def listar_nomes():
    nomes_ord = sorted(rede_social.keys())
    for nome in nomes_ord:
        print(nome)

def salvar_rede_social(nome_arquivo):
  # Abrir o arquivo CSV em modo de escrita
    with open(nome_arquivo, 'w', newline='') as csvfile:
        campos = ["Nome", "Idade", "Ocupacao", "Relacionamentos"]
        escritor = csv.DictWriter(csvfile, fieldnames=campos)

        escritor.writeheader()
        for nome, pessoa in rede_social.items():
            escritor.writerow({
                "Nome": nome,
                "Idade": pessoa["idade"],
                "Ocupacao": pessoa["ocupacao"],
                "Relacionamentos": ",".join(pessoa["lista"])
            })

def maior_grau():
    maior = 0
    for pessoa in rede_social:
        if len(rede_social[pessoa]["lista"]) > maior:
            maior = len(rede_social[pessoa]["lista"])
            nome = pessoa
    print(f"{nome} é a pessoa com maior grau de relacionamentos, com {maior} relacionamentos.")

def menor_grau():
    menor = 999
    for pessoa in rede_social:
        if len(rede_social[pessoa]["lista"]) < menor:
            menor = len(rede_social[pessoa]["lista"])
            nome = pessoa
    print(f"{nome} é a pessoa com menor grau de relacionamentos, com {menor} relacionamentos.")

def menor_distancia(x, y):
    g = criar_grafo("./rede_social.csv")
    response = g.get_shortest_paths(x, to=y, weights=None, output="epath")
    g.es["width"] = 0.5
    g.es[response[0]]['width'] = 3
    plot(
        g,
        vertex_label=g.vs["name"],
        vertex_color="lightblue",
        edge_color="black",
        target="./grafo.png"
    )

def imprimir_grafo():
    file_name = './rede_social.csv'
    rede_social = criar_grafo(file_name)
    plot(rede_social, vertex_label=rede_social.vs["name"], vertex_color="lightblue", edge_color="gray", target="./grafo.png")
