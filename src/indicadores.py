""" Indicadores do CourtLife: totais, proporções, matriz categoria x situação,
 tempos simulados, prioridade e a interpretação dos números. Só usa somas, divisões e laços. """

from constantes import (CATEGORIAS, STATUS, NOMES_CATEGORIA, NOMES_STATUS, NOMES_ESPACO,
                        ESPACOS_CONVIVENCIA, LIMITE_DIAS_URGENTE)
from consultas import formatar_numero


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


def avaliar_prioridade(ocorrencia, dia_atual):
    """ PROTÓTIPO: avaliar_prioridade(ocorrencia: dict, dia_atual: int): tuple[bool, str]
    Decide se a ocorrência é URGENTE e explica o porquê. A expressão booleana é:

        urgente = (convivencia OU acessibilidade) E parada_ha_muito_tempo E NÃO em_andamento

    - convivencia: o espaço é quadra, praça ou pista (onde a vizinhança se encontra);
    - acessibilidade: a categoria é acessibilidade (inclusão);
    - parada_ha_muito_tempo: mais de LIMITE_DIAS_URGENTE dias desde a abertura;
    - em_andamento: já está EM ANÁLISE ou CONCLUÍDA, então alguém já cuida dela. """

    convivencia = ocorrencia["espaco"] in ESPACOS_CONVIVENCIA
    acessibilidade = ocorrencia["categoria"] == "acessibilidade"
    dias = dias_comprometidos(ocorrencia, dia_atual)
    parada = dias > LIMITE_DIAS_URGENTE
    em_andamento = ocorrencia["status"] == "em_analise" or ocorrencia["status"] == "concluida"

    urgente = (convivencia or acessibilidade) and parada and not em_andamento

    if urgente:
        if convivencia and acessibilidade:
            motivos = "espaço de convivência e acessibilidade"
        elif convivencia:
            motivos = "espaço de convivência (" + NOMES_ESPACO[ocorrencia["espaco"]] + ")"
        else:
            motivos = "acessibilidade"
        return True, (motivos + ", aberta há " + str(dias) + " dias (limite " + str(LIMITE_DIAS_URGENTE)
                      + ") e ainda não examinada")

    razoes = []
    if not (convivencia or acessibilidade):
        razoes.append("não é espaço de convivência nem acessibilidade")
    if not parada and ocorrencia["status"] != "concluida":
        razoes.append("só " + str(dias) + " dia(s) de espera (limite " + str(LIMITE_DIAS_URGENTE) + ")")
    if em_andamento:
        razoes.append("já está " + NOMES_STATUS[ocorrencia["status"]])
    return False, "não é urgente: " + "; ".join(razoes)


def listar_urgentes(ocorrencias, dia_atual):
    """ PROTÓTIPO: listar_urgentes(ocorrencias: list, dia_atual: int): list
    Devolve as ocorrências urgentes, em ordem de registro. """

    urgentes = []
    for ocorrencia in ocorrencias:
        urgente, motivo = avaliar_prioridade(ocorrencia, dia_atual)
        if urgente:
            urgentes.append(ocorrencia)
    return urgentes


def categorias_com_mais_pendencias(ocorrencias):
    """ PROTÓTIPO: categorias_com_mais_pendencias(ocorrencias: list): tuple[list[str], int]
    Devolve as categorias (pode haver empate) com o maior número de ocorrências pendentes
    e esse número. Pendente é toda ocorrência que não está concluída. """

    pendentes = {}
    for categoria in CATEGORIAS:
        pendentes[categoria] = 0
    for ocorrencia in ocorrencias:
        if ocorrencia["status"] != "concluida":
            pendentes[ocorrencia["categoria"]] += 1

    maximo = 0
    for categoria in CATEGORIAS:
        if pendentes[categoria] > maximo:
            maximo = pendentes[categoria]

    lideres = []
    for categoria in CATEGORIAS:
        if maximo > 0 and pendentes[categoria] == maximo:
            lideres.append(categoria)
    return lideres, maximo


def montar_conclusao(sistema):
    """ PROTÓTIPO: montar_conclusao(sistema: dict): list[str]
    Interpreta os números: escolhe as frases conforme o que os dados mostram. """

    ocorrencias = sistema["ocorrencias"]
    dia = sistema["dia_atual"]
    total = len(ocorrencias)
    linhas = []
    if total == 0:
        return ["Não há ocorrências cadastradas; não há o que interpretar."]

    por_status = contar_por_status(ocorrencias)
    pendentes = por_status["aberta"] + por_status["em_analise"]
    linhas.append(f"- {pendentes} de {total} ocorrências ({formatar_numero(proporcao(pendentes, total))}%) ainda estão pendentes.")

    lideres, maximo = categorias_com_mais_pendencias(ocorrencias)
    if len(lideres) > 0:
        texto_nomes = ""
        for i in range(len(lideres)):
            nome = NOMES_CATEGORIA[lideres[i]]
            if i == 0:
                texto_nomes = nome
            elif i == len(lideres) - 1:
                texto_nomes = texto_nomes + " e " + nome
            else:
                texto_nomes = texto_nomes + ", " + nome
        if len(lideres) > 1:
            final = " cada)."
        else:
            final = ")."
        linhas.append("- Mais pendências em: " + texto_nomes + " (" + str(maximo) + final)

    urgentes = listar_urgentes(ocorrencias, dia)
    if len(urgentes) > 0:
        linhas.append(f"- {len(urgentes)} ocorrência(s) urgente(s): espaço de convivência ou acessibilidade esperando exame há mais de {LIMITE_DIAS_URGENTE} dias.")
    else:
        linhas.append("- Nenhuma ocorrência urgente no momento.")

    soma_c, qtd_c = somar_dias(ocorrencias, dia, True, False)
    soma_p, qtd_p = somar_dias(ocorrencias, dia, False, True)
    media_concluidas = media(soma_c, qtd_c)
    media_pendentes = media(soma_p, qtd_p)
    if media_concluidas is not None and media_pendentes is not None:
        if media_pendentes > media_concluidas:
            linhas.append(f"- As pendentes já esperam {formatar_numero(media_pendentes)} dias em média, mais que os {formatar_numero(media_concluidas)} dias das concluídas: o atendimento está ficando mais lento.")
        else:
            linhas.append(f"- As pendentes esperam {formatar_numero(media_pendentes)} dias em média, menos que os {formatar_numero(media_concluidas)} dias das concluídas: o atendimento está em dia.")

    linhas.append("- Lembrete: os dados são simulados; os números mostram o método, não a realidade de um bairro.")
    return linhas


def mostrar_painel(sistema):
    """ PROTÓTIPO: mostrar_painel(sistema: dict): None
    Painel textual: dados de origem, fórmula e resultado de cada indicador, e a conclusão. """

    ocorrencias = sistema["ocorrencias"]
    dia = sistema["dia_atual"]
    total = len(ocorrencias)

    print("\n" + "=" * 64)
    print(f"INDICADORES (dia simulado {dia})")
    print("=" * 64)
    print(f"Dados de origem: {total} ocorrências válidas e {len(sistema['historico'])} eventos no histórico.")

    print("\n1) Categoria x situação (matriz) e proporção por categoria")
    print("   Regra: % = ocorrências da categoria / total de ocorrências x 100")
    print(f"{'Categoria':<16}{'ABERTA':>8}{'EM ANÁLISE':>12}{'CONCLUÍDA':>11}{'Total':>7}{'%':>8}")
    matriz = montar_matriz(ocorrencias)
    for i in range(len(CATEGORIAS)):
        total_linha = 0
        for quantidade in matriz[i]:
            total_linha += quantidade
        print(f"{NOMES_CATEGORIA[CATEGORIAS[i]]:<16}{matriz[i][0]:>8}{matriz[i][1]:>12}{matriz[i][2]:>11}"
              f"{total_linha:>7}{formatar_numero(proporcao(total_linha, total)):>8}")

    print("\n2) Ocorrências por situação")
    print("   Regra: % = ocorrências na situação / total de ocorrências x 100")
    por_status = contar_por_status(ocorrencias)
    for status in STATUS:
        print(f"{NOMES_STATUS[status]:<16}{por_status[status]:>4}  ({formatar_numero(proporcao(por_status[status], total))}%)")
    pendentes = por_status["aberta"] + por_status["em_analise"]
    print(f"Pendências (abertas + em análise) = {por_status['aberta']} + {por_status['em_analise']} = {pendentes}")

    print("\n3) Tempos simulados (em dias)")
    soma_c, qtd_c = somar_dias(ocorrencias, dia, True, False)
    media_c = media(soma_c, qtd_c)
    if media_c is None:
        print("Tempo médio até a conclusão: não há ocorrências concluídas.")
    else:
        print("   Regra: soma(dia de conclusão - dia de abertura) / nº de concluídas")
        print(f"Tempo médio até a conclusão = {soma_c} / {qtd_c} = {formatar_numero(media_c)} dias")

    soma_t, qtd_t = somar_dias(ocorrencias, dia, False, False)
    media_t = media(soma_t, qtd_t)
    if media_t is not None:
        print("   Regra: soma((conclusão ou dia atual) - abertura) / nº de ocorrências")
        print(f"Dias médios com o espaço comprometido = {soma_t} / {qtd_t} = {formatar_numero(media_t)} dias")

    print("\n4) Urgências")
    urgentes = listar_urgentes(ocorrencias, dia)
    print(f"Ocorrências urgentes: {len(urgentes)} (veja a regra e os motivos na opção de prioridades)")

    print("\nCONCLUSÃO")
    for linha in montar_conclusao(sistema):
        print(linha)
