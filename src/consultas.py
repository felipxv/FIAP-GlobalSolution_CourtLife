""" Consultas, filtros e formatação das ocorrências para a tela. """

from constantes import NOMES_CATEGORIA, NOMES_STATUS, NOMES_ESPACO


def formatar_numero(valor):
    """ PROTÓTIPO: formatar_numero(valor: float): str
    Uma casa decimal e vírgula, como se escreve no Brasil (6.8 vira '6,8'). """

    return f"{valor:.1f}".replace(".", ",")


def normalizar_codigo(texto):
    """ PROTÓTIPO: normalizar_codigo(texto: str): str
    Aceita '14' ou '014' e devolve '014'. Devolve texto vazio se não forem só números. """

    texto = texto.strip()
    if texto.isdigit():
        return texto.zfill(3)
    return ""


def buscar_por_codigo(indice, codigo):
    """ PROTÓTIPO: buscar_por_codigo(indice: dict, codigo: str): dict | None
    Busca direta no dicionário. Devolve None quando o código não existe. """

    if codigo in indice:
        return indice[codigo]
    return None


def filtrar_ocorrencias(ocorrencias, categoria, status):
    """ PROTÓTIPO: filtrar_ocorrencias(ocorrencias: list, categoria: str, status: str): list
    Devolve as ocorrências que combinam com a categoria E com a situação pedidas.
    Texto vazio em um dos filtros significa 'qualquer valor' naquele campo. """

    resultado = []
    for ocorrencia in ocorrencias:
        passa_categoria = categoria == "" or ocorrencia["categoria"] == categoria
        passa_status = status == "" or ocorrencia["status"] == status
        if passa_categoria and passa_status:
            resultado.append(ocorrencia)
    return resultado


def local_generico(ocorrencia):
    """ PROTÓTIPO: local_generico(ocorrencia: dict): str
    Local sem endereço exato: tipo de espaço e bairro (ex.: 'Quadra - Vila Aurora'). """

    return NOMES_ESPACO[ocorrencia["espaco"]] + " - " + ocorrencia["bairro"]


def formatar_linha(ocorrencia):
    """ PROTÓTIPO: formatar_linha(ocorrencia: dict): str
    Uma linha da listagem: código, categoria, local genérico e situação. """

    categoria = NOMES_CATEGORIA[ocorrencia["categoria"]]
    return f"{ocorrencia['id']} | {categoria:<14} | {local_generico(ocorrencia):<36} | {NOMES_STATUS[ocorrencia['status']]}"


def mostrar_lista(titulo, lista):
    """ PROTÓTIPO: mostrar_lista(titulo: str, lista: list): None
    Imprime a listagem com cabeçalho e o total, ou avisa que nada foi encontrado. """

    print("\n--- " + titulo + " ---")
    if len(lista) == 0:
        print("Nenhuma ocorrência encontrada.")
        return
    print(f"{'COD':<3} | {'CATEGORIA':<14} | {'LOCAL':<36} | SITUAÇÃO")
    for ocorrencia in lista:
        print(formatar_linha(ocorrencia))
    print(f"Total: {len(lista)} ocorrência(s).")
