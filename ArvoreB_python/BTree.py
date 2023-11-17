import csv

# Declaração das classes e definição do grau da árvore

indexLettersUsed = set()


class Registro:
    def __init__(self):
        self.Chave = None
        self.Elemento = None


class Pagina:
    def __init__(self, ordem):
        self.n = 0
        self.r = [None for i in range(ordem)]
        self.p = [None for i in range(ordem+1)]

# Pesquisa


def Pesquisa(x, Ap):
    i = 1
    if (Ap == None):
        print("Registro não está presente na árvore\n")
        return

    while (i < Ap.n and x.Chave > Ap.r[i - 1].Chave):
        i += 1
    if (x.Chave == Ap.r[i - 1].Chave):
        x = Ap.r[i - 1]
        return x

    if (x.Chave < Ap.r[i - 1].Chave):
        x = Pesquisa(x, Ap.p[i - 1])
    else:
        x = Pesquisa(x, Ap.p[i])

    return x


def PesquisaAlfa(chave, Ap):
    i = 0
    if Ap is None:
        print("Registro não está presente na árvore\n")
        return

    while i < Ap.n:
        if Ap.r[i].Chave.startswith(chave):
            print(Ap.r[i].Chave, "-", Ap.r[i].Elemento)
        elif chave < Ap.r[i].Chave:
            PesquisaAlfa(chave, Ap.p[i])
        i += 1

    PesquisaAlfa(chave, Ap.p[i])

#pesquisas em intervalo
def BuscaPorIntervaloNumerico(Ap, x, y):
    if Ap is None:
        return

    i = 0
    while i < Ap.n and x > Ap.r[i].Chave:
        i += 1

    if Ap.p[i] is not None and x == Ap.r[i].Chave:
        Imprime(Ap.p[i])  
    elif Ap.p[i] is not None and x < Ap.r[i].Chave:
        BuscaPorIntervaloNumerico(Ap.p[i], x, y)

    while i < Ap.n and Ap.r[i].Chave <= y:
        if Ap.r[i].Chave >= x:
            print(Ap.r[i].Chave, "-", Ap.r[i].Elemento)
        i += 1

    if i < Ap.n and Ap.p[i] is not None and y > Ap.r[i - 1].Chave:
        BuscaPorIntervaloNumerico(Ap.p[i], x, y)


def BuscaPorIntervaloAlfa(Ap, x, y):
    if Ap is None:
        return

    i = 0
    while i < Ap.n and x > Ap.r[i].Chave:
        i += 1

    if Ap.p[i] is not None and x.startswith(Ap.r[i].Chave):
        Imprime(Ap.p[i])  
    elif Ap.p[i] is not None and x < Ap.r[i].Chave:
        BuscaPorIntervaloAlfa(Ap.p[i], x, y)

    while i < Ap.n and Ap.r[i].Chave <= y:
        if Ap.r[i].Chave >= x:
            print(Ap.r[i].Chave, "-", Ap.r[i].Elemento)
        i += 1

    if i < Ap.n and Ap.p[i] is not None and y > Ap.r[i - 1].Chave:
        BuscaPorIntervaloAlfa(Ap.p[i], x, y)
# Funções de inserção

# Insere o registro na página escolhida


def _InsereNaPagina(Ap, Reg, ApDir):
    k = Ap.n
    NaoAchouPosicao = (k > 0)
    while (NaoAchouPosicao):
        if (Reg.Chave >= Ap.r[k - 1].Chave):
            NaoAchouPosicao = False
            break
        Ap.r[k] = Ap.r[k - 1]
        Ap.p[k + 1] = Ap.p[k]
        k -= 1
        if (k < 1):
            NaoAchouPosicao = False

    Ap.r[k] = Reg
    Ap.p[k + 1] = ApDir
    Ap.n += 1

# Busca a página onde o registro será inserido e controla a divisão de páginas por Overflow


def _Ins(Reg, Ap, Cresceu, RegRetorno, ApRetorno, Ordem):
    i = 1
    J = None
    if (Ap == None):
        Cresceu = True
        RegRetorno = Reg
        ApRetorno = None
        return Cresceu, RegRetorno, ApRetorno

    while (i < Ap.n and Reg.Chave > Ap.r[i - 1].Chave):
        i += 1

    if (Reg.Chave == Ap.r[i - 1].Chave):
        print(" Erro: Registro já está presente\n")
        Cresceu = False
        return Cresceu, RegRetorno, ApRetorno

    if (Reg.Chave < Ap.r[i - 1].Chave):
        i -= 1

    Cresceu, RegRetorno, ApRetorno = _Ins(
        Reg, Ap.p[i], Cresceu, RegRetorno, ApRetorno, Ordem)

    if (not Cresceu):
        return Cresceu, RegRetorno, ApRetorno
    if (Ap.n < Ordem):  # Página tem espaco
        _InsereNaPagina(Ap, RegRetorno, ApRetorno)
        Cresceu = False
        return Cresceu, RegRetorno, ApRetorno

    # Overflow: Página tem que ser dividida /
    ApTemp = Pagina(Ordem)
    ApTemp.n = 0
    ApTemp.p[0] = None
    if (i < (Ordem//2) + 1):
        _InsereNaPagina(ApTemp, Ap.r[Ordem - 1], Ap.p[Ordem])
        Ap.n -= 1
        _InsereNaPagina(Ap, RegRetorno, ApRetorno)
    else:
        _InsereNaPagina(ApTemp, RegRetorno, ApRetorno)
    for J in range((Ordem//2) + 2, Ordem + 1):
        _InsereNaPagina(ApTemp, Ap.r[J - 1], Ap.p[J])
    Ap.n = (Ordem//2)
    ApTemp.p[0] = Ap.p[(Ordem//2) + 1]
    RegRetorno = Ap.r[(Ordem//2)]
    ApRetorno = ApTemp
    return Cresceu, RegRetorno, ApRetorno

# Cria página da nova raiz caso a árvore cresça em altura


def _Insere(Reg, Ap, Ordem):
    Cresceu = False
    RegRetorno = Registro()
    ApRetorno = Pagina(Ordem)
    Cresceu, RegRetorno, ApRetorno = _Ins(
        Reg, Ap, Cresceu, RegRetorno, ApRetorno, Ordem)
    if (Cresceu):
        ApTemp = Pagina(Ordem)
        ApTemp.n = 1
        ApTemp.r[0] = RegRetorno
        ApTemp.p[1] = ApRetorno
        ApTemp.p[0] = Ap
        Ap = ApTemp
    return Ap

# Insere elementos do arquivo


def _InserirElementos(Ap, ordem, dataframe, chave):
    tam_lin = len(dataframe)
    for i in range(tam_lin):
        reg = Registro()
        reg.Chave = chave
        reg.Elemento = dataframe[i]
        Ap = _Insere(reg, Ap, ordem)
        chave += 1
    return Ap, chave


def _pegarLetrasIndice(dataframe, i, indiceNaPalavra=1):
    if i < len(dataframe) and len(dataframe[i]) > 1:
        palavra = dataframe[i][0].lower()
        if palavra[:indiceNaPalavra] in indexLettersUsed:
            return _pegarLetrasIndice(dataframe, i, indiceNaPalavra+1)
        return palavra[:indiceNaPalavra]
    return ""


def _InserirElementosAlfa(Ap, ordem, dataframe, chave):
    tam_lin = len(dataframe)
    for i in range(tam_lin):
        reg = Registro()
        reg.Chave = _pegarLetrasIndice(dataframe, i)
        if reg.Chave == "":
            continue
        indexLettersUsed.add(reg.Chave)

        reg.Elemento = dataframe[i]
        Ap = _Insere(reg, Ap, ordem)
    return Ap


def _loadCSVContent(filename):
    data = []
    with open(filename, 'r') as csvfile:
        data = csv.reader(csvfile, delimiter=';')
        data = list(data)
    return data


def Inserir(Ap, ApAlfa, chave):
    ordem = int(input("Digite a ordem da árvore:"))
    arq = input("Digite o nome do arquivo:")
    if arq.lower().endswith(".csv"):
        dataframe = _loadCSVContent(arq)
    else:
        print("Arquivo incompatível.")
    Ap, chave = _InserirElementos(Ap, ordem, dataframe, chave)
    ApAlfa = _InserirElementosAlfa(ApAlfa, ordem, dataframe, chave)
    return Ap, ApAlfa, chave

# Impressão


def Imprime(Ap):
    if (Ap != None):
        i = 0
        while i < Ap.n:
            Imprime(Ap.p[i])
            print(Ap.r[i].Chave, "-", Ap.r[i].Elemento)
            i += 1
        Imprime(Ap.p[i])


def ImprimeMenor(x, Ap):
    if (Ap != None):
        i = 0
        while i < Ap.n:
            ImprimeMenor(x, Ap.p[i])
            if (Ap.r[i].Chave < x.Chave):
                print(Ap.r[i].Chave, "-", Ap.r[i].Elemento)
            i += 1
        ImprimeMenor(x, Ap.p[i])


def ImprimeMaior(x, Ap):
    if (Ap != None):
        i = 0
        while i < Ap.n:
            ImprimeMaior(x, Ap.p[i])
            if (Ap.r[i].Chave > x.Chave):
                print(Ap.r[i].Chave, "-", Ap.r[i].Elemento)
            i += 1
        ImprimeMaior(x, Ap.p[i])
