""" Leitura dos arquivos e montagem das estruturas de dados do CourtLife.
 Cada estrutura existe por um motivo:
   lista       -> ocorrencias: guarda todas e permite percorrer;
   dicionário  -> indice: acha uma ocorrência direto pelo código;
   fila        -> fila: ocorrências ABERTAS, a mais antiga na frente (primeira a entrar, primeira a sair);
   pilha       -> pilha: últimas atualizações, a mais recente no topo (última a entrar, primeira a sair);
   hierarquia  -> dicionário dentro de dicionário: bairro -> categoria -> códigos;
   matriz      -> lista de listas, montada em indicadores.py (categoria x situação). """

import os
from constantes import DIA_INICIAL, STATUS
from validacao import validar_registro_arquivo

# Caminhos calculados a partir deste arquivo, para o sistema rodar de qualquer pasta
RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CAMINHO_OCORRENCIAS = os.path.join(RAIZ, "data", "ocorrencias.csv")
CAMINHO_HISTORICO = os.path.join(RAIZ, "data", "historico.csv")

# Campos de cada linha do ocorrencias.csv, na ordem em que aparecem (separados por ponto e vírgula)
CAMPOS = ["id", "categoria", "descricao", "bairro", "espaco", "dia_abertura", "status", "dia_conclusao"]


def ler_linhas(caminho):
    """ PROTÓTIPO: ler_linhas(caminho: str): list[str]
    Lê um arquivo de texto e devolve uma lista com uma string por linha. """

    with open(caminho, encoding="utf-8") as arquivo:
        return arquivo.read().splitlines()


def carregar_ocorrencias(caminho):
    """ PROTÓTIPO: carregar_ocorrencias(caminho: str): tuple[list, dict, list]
    Lê o CSV de ocorrências. Cada linha passa pela validação: as válidas entram na lista e
    no dicionário; as que têm campo ausente ou inconsistente são recusadas e devolvidas à
    parte, com o motivo, para o sistema avisar. """

    linhas = ler_linhas(caminho)
    ocorrencias = []
    indice = {}
    rejeitadas = []

    for posicao in range(1, len(linhas)):  # a linha 0 é o cabeçalho
        linha = linhas[posicao]
        if linha.strip() == "":
            continue

        campos = linha.split(";")
        if len(campos) != len(CAMPOS):
            rejeitadas.append({"linha": posicao + 1, "id": "?", "erros": ["quantidade de campos incorreta"]})
            continue

        dados = {}
        for i in range(len(CAMPOS)):
            dados[CAMPOS[i]] = campos[i].strip()

        erros = validar_registro_arquivo(dados, indice)
        if len(erros) > 0:
            rejeitadas.append({"linha": posicao + 1, "id": dados["id"], "erros": erros})
            continue

        dia_conclusao = None
        if dados["dia_conclusao"] != "":
            dia_conclusao = int(dados["dia_conclusao"])
        ocorrencia = {
            "id": dados["id"],
            "categoria": dados["categoria"],
            "descricao": dados["descricao"],
            "bairro": dados["bairro"],
            "espaco": dados["espaco"],
            "dia_abertura": int(dados["dia_abertura"]),
            "status": dados["status"],
            "dia_conclusao": dia_conclusao,
        }
        ocorrencias.append(ocorrencia)
        indice[ocorrencia["id"]] = ocorrencia

    return ocorrencias, indice, rejeitadas


def carregar_historico(caminho, indice):
    """ PROTÓTIPO: carregar_historico(caminho: str, indice: dict): tuple[list, int]
    Lê o CSV do histórico (um evento por linha, já em ordem de data). Ignora, contando,
    os eventos de ocorrência inexistente ou com situação desconhecida. """

    linhas = ler_linhas(caminho)
    eventos = []
    ignorados = 0

    for posicao in range(1, len(linhas)):
        if linhas[posicao].strip() == "":
            continue
        campos = linhas[posicao].split(";")
        valido = len(campos) == 4 and campos[0] in indice and campos[1].isdigit()
        if valido and campos[2] in STATUS and campos[3] in STATUS:
            eventos.append({"codigo": campos[0], "dia": int(campos[1]), "de": campos[2], "para": campos[3]})
        else:
            ignorados += 1

    return eventos, ignorados


def construir_fila(ocorrencias):
    """ PROTÓTIPO: construir_fila(ocorrencias: list): list[str]
    Monta a fila com os códigos das ocorrências abertas. Como a lista já está em ordem de
    registro, a mais antiga fica na frente. """

    fila = []
    for ocorrencia in ocorrencias:
        if ocorrencia["status"] == "aberta":
            fila.append(ocorrencia["id"])
    return fila


def construir_pilha(eventos):
    """ PROTÓTIPO: construir_pilha(eventos: list): list[dict]
    Monta a pilha de atualizações: empilha os eventos em ordem, então o último fica no topo. """

    pilha = []
    for evento in eventos:
        pilha.append(evento)
    return pilha


def adicionar_na_hierarquia(hierarquia, ocorrencia):
    """ PROTÓTIPO: adicionar_na_hierarquia(hierarquia: dict, ocorrencia: dict): None
    Coloca o código da ocorrência no caminho bairro -> categoria, criando os níveis que
    ainda não existem. """

    bairro = ocorrencia["bairro"]
    categoria = ocorrencia["categoria"]
    if bairro not in hierarquia:
        hierarquia[bairro] = {}
    if categoria not in hierarquia[bairro]:
        hierarquia[bairro][categoria] = []
    hierarquia[bairro][categoria].append(ocorrencia["id"])


def construir_hierarquia(ocorrencias):
    """ PROTÓTIPO: construir_hierarquia(ocorrencias: list): dict
    Monta a hierarquia bairro -> categoria -> lista de códigos. """

    hierarquia = {}
    for ocorrencia in ocorrencias:
        adicionar_na_hierarquia(hierarquia, ocorrencia)
    return hierarquia


def carregar_sistema():
    """ PROTÓTIPO: carregar_sistema(): dict
    Lê os dois arquivos e devolve o 'sistema': um dicionário que reúne todas as estruturas
    e o dia simulado atual. É ele que as outras funções recebem e atualizam.
    Devolve None se os arquivos de dados não forem encontrados. """

    if not os.path.exists(CAMINHO_OCORRENCIAS) or not os.path.exists(CAMINHO_HISTORICO):
        return None

    ocorrencias, indice, rejeitadas = carregar_ocorrencias(CAMINHO_OCORRENCIAS)
    eventos, ignorados = carregar_historico(CAMINHO_HISTORICO, indice)
    return {
        "ocorrencias": ocorrencias,
        "indice": indice,
        "rejeitadas": rejeitadas,
        "historico": eventos,
        "eventos_ignorados": ignorados,
        "pilha": construir_pilha(eventos),
        "fila": construir_fila(ocorrencias),
        "hierarquia": construir_hierarquia(ocorrencias),
        "dia_atual": DIA_INICIAL,
    }
