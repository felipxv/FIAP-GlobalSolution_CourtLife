""" Regras de validação do CourtLife.
 Cada função devolve a lista os erros encontrados.
 Lista vazia ou texto vazio, quer dizer que está tudo certo. """

from constantes import CATEGORIAS, ESPACOS, STATUS, NOMES_STATUS, TRANSICOES


def parece_dado_pessoal(texto):
    """ PROTÓTIPO: parece_dado_pessoal(texto: str): bool
    Privacidade: o sistema não deve guardar e-mail nem telefone. Considera que há dado
    pessoal quando o texto tem '@' ou oito ou mais dígitos no total. """

    quantidade_digitos = 0
    for letra in texto:
        if letra.isdigit():
            quantidade_digitos += 1
    return "@" in texto or quantidade_digitos >= 8


def validar_campos(dados):
    """ PROTÓTIPO: validar_campos(dados: dict): list[str]
    Valida os campos que o morador informa ao cadastrar: categoria, descrição, bairro e espaço.
    Todos são obrigatórios; categoria e espaço precisam ter um valor padronizado. """

    erros = []

    if dados["categoria"] == "":
        erros.append("categoria ausente (campo obrigatório)")
    elif dados["categoria"] not in CATEGORIAS:
        erros.append("categoria desconhecida: '" + dados["categoria"] + "' (use: " + ", ".join(CATEGORIAS) + ")")

    if dados["descricao"] == "":
        erros.append("descrição ausente (campo obrigatório)")
    elif parece_dado_pessoal(dados["descricao"]):
        erros.append("descrição parece ter dado pessoal (e-mail ou telefone); descreva só o problema")

    if dados["bairro"] == "":
        erros.append("bairro ausente (campo obrigatório)")

    if dados["espaco"] == "":
        erros.append("espaço ausente (campo obrigatório)")
    elif dados["espaco"] not in ESPACOS:
        erros.append("espaço desconhecido: '" + dados["espaco"] + "' (use: " + ", ".join(ESPACOS) + ")")

    return erros


def validar_registro_arquivo(dados, indice):
    """ PROTÓTIPO: validar_registro_arquivo(dados: dict, indice: dict): list[str]
    Valida uma linha lida do CSV (todos os valores chegam como texto). Além dos campos do
    cadastro, confere id, dia de abertura, situação e a coerência do dia de conclusão. """

    erros = validar_campos(dados)

    codigo = dados["id"]
    if codigo == "" or not codigo.isdigit():
        erros.append("id ausente ou não numérico")
    elif codigo in indice:
        erros.append("id repetido: " + codigo)

    abertura_ok = dados["dia_abertura"].isdigit()
    if not abertura_ok:
        erros.append("dia de abertura ausente ou inválido")

    if dados["status"] not in STATUS:
        erros.append("situação desconhecida: '" + dados["status"] + "'")
        return erros

    conclusao = dados["dia_conclusao"]
    if dados["status"] == "concluida" and conclusao == "":
        erros.append("ocorrência concluída sem dia de conclusão")
    if dados["status"] != "concluida" and conclusao != "":
        erros.append("dia de conclusão em ocorrência que não está concluída")
    if conclusao != "" and not conclusao.isdigit():
        erros.append("dia de conclusão inválido")
    elif conclusao != "" and abertura_ok and int(conclusao) < int(dados["dia_abertura"]):
        erros.append("dia de conclusão (" + conclusao + ") anterior ao dia de abertura (" + dados["dia_abertura"] + ")")

    return erros


def validar_transicao(atual, novo):
    """ PROTÓTIPO: validar_transicao(atual: str, novo: str): str
    Confere se a ocorrência pode ir da situação atual para a nova. Devolve o motivo da
    recusa, ou texto vazio quando a mudança é permitida. """

    if novo not in STATUS:
        return "situação desconhecida: '" + novo + "'"
    if novo == atual:
        return "a ocorrência já está " + NOMES_STATUS[atual]
    if novo not in TRANSICOES[atual]:
        if len(TRANSICOES[atual]) == 0:
            return "ocorrência " + NOMES_STATUS[atual] + " não muda mais de situação"
        permitidas = []
        for destino in TRANSICOES[atual]:
            permitidas.append(NOMES_STATUS[destino])
        return "de " + NOMES_STATUS[atual] + " só é permitido ir para " + ", ".join(permitidas)
    return ""
