""" Indicadores do CourtLife: totais, proporções, matriz categoria x situação e tempos simulados.
 Só usa somas, divisões e laços. """

from constantes import CATEGORIAS, STATUS


def contar_por_categoria(ocorrencias):
    """ PROTÓTIPO: contar_por_categoria(ocorrencias: list): dict
    Total de ocorrências de cada categoria. """

    totais = {}
    for categoria in CATEGORIAS:
        totais[categoria] = 0
    for ocorrencia in ocorrencias:
        totais[ocorrencia["categoria"]] += 1
    return totais


def contar_por_status(ocorrencias):
    """ PROTÓTIPO: contar_por_status(ocorrencias: list): dict
    Total de ocorrências em cada situação. """

    totais = {}
    for status in STATUS:
        totais[status] = 0
    for ocorrencia in ocorrencias:
        totais[ocorrencia["status"]] += 1
    return totais


def montar_matriz(ocorrencias):
    """ PROTÓTIPO: montar_matriz(ocorrencias: list): list[list[int]]
    Matriz (lista de listas): cada linha é uma categoria e cada coluna uma situação, na
    ordem de CATEGORIAS e STATUS. O número em matriz[i][j] é a quantidade de ocorrências
    da categoria i que estão na situação j. """

    matriz = []
    for categoria in CATEGORIAS:
        linha = []
        for status in STATUS:
            quantidade = 0
            for ocorrencia in ocorrencias:
                if ocorrencia["categoria"] == categoria and ocorrencia["status"] == status:
                    quantidade += 1
            linha.append(quantidade)
        matriz.append(linha)
    return matriz


def proporcao(parte, total):
    """ PROTÓTIPO: proporcao(parte: int, total: int): float
    Percentual = parte / total * 100. Devolve 0 quando não há nada cadastrado. """

    if total == 0:
        return 0.0
    return parte * 100 / total


def dias_comprometidos(ocorrencia, dia_atual):
    """ PROTÓTIPO: dias_comprometidos(ocorrencia: dict, dia_atual: int): int
    Quantos dias o espaço ficou (ou está) com o problema: da abertura até a conclusão,
    ou até o dia atual quando ainda não foi concluída. """

    if ocorrencia["dia_conclusao"] is not None:
        return ocorrencia["dia_conclusao"] - ocorrencia["dia_abertura"]
    return dia_atual - ocorrencia["dia_abertura"]


def somar_dias(ocorrencias, dia_atual, somente_concluidas, somente_pendentes):
    """ PROTÓTIPO: somar_dias(ocorrencias: list, dia_atual: int, somente_concluidas: bool, somente_pendentes: bool): tuple[int, int]
    Soma os dias comprometidos e conta quantas ocorrências entraram na soma. Os dois filtros
    escolhem só as concluídas, só as pendentes (abertas e em análise) ou todas. """

    soma = 0
    quantidade = 0
    for ocorrencia in ocorrencias:
        concluida = ocorrencia["status"] == "concluida"
        if somente_concluidas and not concluida:
            continue
        if somente_pendentes and concluida:
            continue
        soma += dias_comprometidos(ocorrencia, dia_atual)
        quantidade += 1
    return soma, quantidade


def media(soma, quantidade):
    """ PROTÓTIPO: media(soma: int, quantidade: int): float | None
    Média simples. Devolve None quando não há ocorrências para calcular. """

    if quantidade == 0:
        return None
    return soma / quantidade
