""" Cadastro e acompanhamento das ocorrências: cadastrar, mudar a situação (com histórico),
 examinar a próxima da fila e desfazer a última atualização. Todas as funções recebem o
 'sistema' (o dicionário montado em dados.py) e o alteram. """

from constantes import NOMES_STATUS
from validacao import validar_campos, validar_transicao
from dados import adicionar_na_hierarquia


def proximo_codigo(sistema):
    """ PROTÓTIPO: proximo_codigo(sistema: dict): str
    Gera o código único da próxima ocorrência: o maior código já usado mais um. Os códigos
    das linhas recusadas na leitura também contam, para não reaproveitar um número. """

    maior = 0
    for ocorrencia in sistema["ocorrencias"]:
        if int(ocorrencia["id"]) > maior:
            maior = int(ocorrencia["id"])
    for rejeitada in sistema["rejeitadas"]:
        if rejeitada["id"].isdigit() and int(rejeitada["id"]) > maior:
            maior = int(rejeitada["id"])
    return str(maior + 1).zfill(3)


def cadastrar_ocorrencia(sistema, dados):
    """ PROTÓTIPO: cadastrar_ocorrencia(sistema: dict, dados: dict): tuple[bool, list | dict]
    Valida os campos informados. Se houver erro, devolve (False, lista de erros) e nada é
    cadastrado. Se estiver tudo certo, cria a ocorrência ABERTA no dia simulado atual, coloca
    no fim da fila (ordem de registro) e na hierarquia, e devolve (True, ocorrência). """

    erros = validar_campos(dados)
    if len(erros) > 0:
        return False, erros

    ocorrencia = {
        "id": proximo_codigo(sistema),
        "categoria": dados["categoria"],
        "descricao": dados["descricao"],
        "bairro": dados["bairro"],
        "espaco": dados["espaco"],
        "dia_abertura": sistema["dia_atual"],
        "status": "aberta",
        "dia_conclusao": None,
    }
    sistema["ocorrencias"].append(ocorrencia)
    sistema["indice"][ocorrencia["id"]] = ocorrencia
    sistema["fila"].append(ocorrencia["id"])
    adicionar_na_hierarquia(sistema["hierarquia"], ocorrencia)
    return True, ocorrencia


def registrar_evento(sistema, codigo, de, para):
    """ PROTÓTIPO: registrar_evento(sistema: dict, codigo: str, de: str, para: str): None
    Guarda a mudança de situação no histórico (lista, com tudo) e empilha na pilha, onde o
    último evento fica no topo. """

    evento = {"codigo": codigo, "dia": sistema["dia_atual"], "de": de, "para": para}
    sistema["historico"].append(evento)
    sistema["pilha"].append(evento)


def atualizar_status(sistema, codigo, novo_status):
    """ PROTÓTIPO: atualizar_status(sistema: dict, codigo: str, novo_status: str): tuple[bool, str]
    Muda a situação de uma ocorrência existente, se a mudança for permitida, e registra no
    histórico. Quando sai de ABERTA, a ocorrência deixa a fila; quando conclui, guarda o dia
    de conclusão. Devolve (True/False, mensagem explicando o resultado). """

    if codigo not in sistema["indice"]:
        return False, "Ocorrência " + codigo + " não encontrada."

    ocorrencia = sistema["indice"][codigo]
    motivo = validar_transicao(ocorrencia["status"], novo_status)
    if motivo != "":
        return False, "Mudança recusada: " + motivo + "."

    antiga = ocorrencia["status"]
    ocorrencia["status"] = novo_status
    if novo_status == "concluida":
        ocorrencia["dia_conclusao"] = sistema["dia_atual"]
    if antiga == "aberta":
        sistema["fila"].remove(codigo)
    registrar_evento(sistema, codigo, antiga, novo_status)

    return True, ("Ocorrência " + codigo + ": " + NOMES_STATUS[antiga] + " -> " + NOMES_STATUS[novo_status]
                  + " (dia " + str(sistema["dia_atual"]) + ").")


def examinar_proxima(sistema):
    """ PROTÓTIPO: examinar_proxima(sistema: dict): tuple[bool, str]
    Tira a primeira da fila (a aberta há mais tempo) e a coloca EM ANÁLISE. Se a fila
    estiver vazia, avisa que não há demandas esperando. """

    if len(sistema["fila"]) == 0:
        return False, "A fila está vazia: não há ocorrências aguardando exame."
    return atualizar_status(sistema, sistema["fila"][0], "em_analise")


def inserir_na_fila(sistema, ocorrencia):
    """ PROTÓTIPO: inserir_na_fila(sistema: dict, ocorrencia: dict): None
    Devolve uma ocorrência à fila no lugar certo (por dia de abertura e, em empate, por
    código), para a ordem de registro continuar valendo. """

    fila = sistema["fila"]
    posicao = len(fila)
    for i in range(len(fila)):
        outra = sistema["indice"][fila[i]]
        abriu_antes = ocorrencia["dia_abertura"] < outra["dia_abertura"]
        mesmo_dia = ocorrencia["dia_abertura"] == outra["dia_abertura"]
        codigo_menor = int(ocorrencia["id"]) < int(outra["id"])
        if abriu_antes or (mesmo_dia and codigo_menor):
            posicao = i
            break
    fila.insert(posicao, ocorrencia["id"])


def desfazer_ultima(sistema):
    """ PROTÓTIPO: desfazer_ultima(sistema: dict): tuple[bool, str]
    Usa a pilha: tira o evento do topo (a última atualização) e volta a ocorrência para a
    situação anterior. Também apaga o evento do histórico e, se a ocorrência voltou a ser
    ABERTA, devolve ela à fila. """

    if len(sistema["pilha"]) == 0:
        return False, "Não há atualizações para desfazer."

    evento = sistema["pilha"].pop()
    sistema["historico"].pop()

    ocorrencia = sistema["indice"][evento["codigo"]]
    ocorrencia["status"] = evento["de"]
    if evento["para"] == "concluida":
        ocorrencia["dia_conclusao"] = None
    if evento["de"] == "aberta":
        inserir_na_fila(sistema, ocorrencia)

    return True, ("Atualização desfeita: ocorrência " + evento["codigo"] + " voltou de "
                  + NOMES_STATUS[evento["para"]] + " para " + NOMES_STATUS[evento["de"]] + ".")
