""" CourtLife: painel comunitário de ocorrências em espaços de convivência (terminal).
 Código para interação com usuário: menu, perguntas e mensagens. 
 
 Como executar:  python src/sistema.py """

from constantes import CATEGORIAS, NOMES_CATEGORIA, STATUS, NOMES_STATUS, ESPACOS, NOMES_ESPACO
from dados import carregar_sistema
from consultas import (normalizar_codigo, buscar_por_codigo, filtrar_ocorrencias, mostrar_lista,
                       local_generico)
from acompanhamento import cadastrar_ocorrencia, atualizar_status
from indicadores import avaliar_prioridade, dias_comprometidos


def ler_texto(pergunta, se_acabar=""):
    """ PROTÓTIPO: ler_texto(pergunta: str, se_acabar: str): str
    Faz uma pergunta e devolve a resposta sem espaços nas pontas. Se a entrada acabar
    (execução com dados redirecionados), devolve 'se_acabar' em vez de dar erro. """

    try:
        return input(pergunta).strip()
    except EOFError:
        print()
        return se_acabar


def escolher(pergunta, chaves, nomes):
    """ PROTÓTIPO: escolher(pergunta: str, chaves: list, nomes: dict): str
    Mostra as opções numeradas e devolve a chave escolhida. Aceita o número ou o próprio
    identificador. Se a pessoa deixar em branco ou digitar algo fora da lista, devolve o texto
    como veio, e a validação do sistema explica o que está errado. """

    print(pergunta)
    for i in range(len(chaves)):
        print(f"   {i + 1} - {nomes[chaves[i]]}")
    texto = ler_texto("Escolha (número ou nome; Enter deixa em branco): ")
    if texto.isdigit() and 1 <= int(texto) <= len(chaves):
        return chaves[int(texto) - 1]
    return texto.lower()


def pedir_codigo():
    """ PROTÓTIPO: pedir_codigo(): str
    Pergunta o código e o normaliza ('14' vira '014'). Devolve texto vazio, com aviso,
    se a entrada não for numérica. """

    texto = ler_texto("Código da ocorrência (ex.: 014): ")
    codigo = normalizar_codigo(texto)
    if codigo == "":
        print("ERRO: código inválido. Digite só números, por exemplo 14 ou 014.")
    return codigo


def mostrar_cabecalho(sistema):
    """ PROTÓTIPO: mostrar_cabecalho(sistema: dict): None
    Título do sistema, resumo do carregamento e aviso das linhas recusadas na validação. """

    print("=" * 64)
    print("COURTLIFE - Painel comunitário de ocorrências")
    print("Bairros fictícios: Vila Aurora, Jardim Estelar e Parque Orion")
    print("=" * 64)
    print(f"Dados carregados: {len(sistema['ocorrencias'])} ocorrências válidas, "
          f"{len(sistema['historico'])} eventos no histórico.")
    if len(sistema["rejeitadas"]) > 0:
        print(f"AVISO: {len(sistema['rejeitadas'])} linha(s) do arquivo foram recusadas pela validação:")
        for rejeitada in sistema["rejeitadas"]:
            print(f"   linha {rejeitada['linha']} (código {rejeitada['id']}): " + "; ".join(rejeitada["erros"]))


def mostrar_detalhe(sistema, ocorrencia):
    """ PROTÓTIPO: mostrar_detalhe(sistema: dict, ocorrencia: dict): None
    Mostra todos os dados de uma ocorrência, a avaliação de prioridade e o histórico dela. """

    dia = sistema["dia_atual"]
    print("\n--- OCORRÊNCIA " + ocorrencia["id"] + " ---")
    print("Categoria: " + NOMES_CATEGORIA[ocorrencia["categoria"]])
    print("Descrição: " + ocorrencia["descricao"])
    print("Local: " + local_generico(ocorrencia))
    print(f"Aberta no dia {ocorrencia['dia_abertura']}")
    print("Situação: " + NOMES_STATUS[ocorrencia["status"]])
    if ocorrencia["dia_conclusao"] is not None:
        print(f"Concluída no dia {ocorrencia['dia_conclusao']}")
    print(f"Dias com o espaço comprometido: {dias_comprometidos(ocorrencia, dia)}")
    urgente, motivo = avaliar_prioridade(ocorrencia, dia)
    if urgente:
        print("Prioridade: URGENTE (" + motivo + ")")
    else:
        print("Prioridade: normal (" + motivo + ")")

    print("Histórico desta ocorrência:")
    encontrou = False
    for evento in sistema["historico"]:
        if evento["codigo"] == ocorrencia["id"]:
            print(f"   dia {evento['dia']}: {NOMES_STATUS[evento['de']]} -> {NOMES_STATUS[evento['para']]}")
            encontrou = True
    if not encontrou:
        print("   (sem atualizações de situação)")


def opcao_listar(sistema):
    """ PROTÓTIPO: opcao_listar(sistema: dict): None """

    mostrar_lista("TODAS AS OCORRÊNCIAS", sistema["ocorrencias"])


def opcao_consultar(sistema):
    """ PROTÓTIPO: opcao_consultar(sistema: dict): None
    Busca pelo código, direto no dicionário. """

    codigo = pedir_codigo()
    if codigo == "":
        return
    ocorrencia = buscar_por_codigo(sistema["indice"], codigo)
    if ocorrencia is None:
        print("Ocorrência " + codigo + " não encontrada. Use a opção 1 para ver os códigos existentes.")
    else:
        mostrar_detalhe(sistema, ocorrencia)


def opcao_filtrar(sistema):
    """ PROTÓTIPO: opcao_filtrar(sistema: dict): None
    Filtra por categoria e/ou situação. Em branco, o filtro não é aplicado. """

    print("\n--- FILTRAR OCORRÊNCIAS (Enter deixa o filtro em branco) ---")
    categoria = escolher("Categoria:", CATEGORIAS, NOMES_CATEGORIA)
    status = escolher("Situação:", STATUS, NOMES_STATUS)
    if categoria != "" and categoria not in CATEGORIAS:
        print("ERRO: categoria desconhecida: '" + categoria + "'.")
        return
    if status != "" and status not in STATUS:
        print("ERRO: situação desconhecida: '" + status + "'.")
        return
    mostrar_lista("RESULTADO DO FILTRO", filtrar_ocorrencias(sistema["ocorrencias"], categoria, status))


def opcao_cadastrar(sistema):
    """ PROTÓTIPO: opcao_cadastrar(sistema: dict): None
    Pergunta os campos, valida e cadastra a ocorrência nova. """

    print("\n--- CADASTRAR NOVA OCORRÊNCIA ---")
    print("Privacidade: não escreva nomes, telefones, e-mails nem endereço exato.")
    dados = {}
    dados["categoria"] = escolher("Categoria:", CATEGORIAS, NOMES_CATEGORIA)
    dados["descricao"] = ler_texto("Descrição breve do problema: ")
    dados["bairro"] = ler_texto("Bairro (ex.: Vila Aurora): ")
    dados["espaco"] = escolher("Tipo de espaço:", ESPACOS, NOMES_ESPACO)

    cadastrou, resultado = cadastrar_ocorrencia(sistema, dados)
    if cadastrou:
        print(f"OK: ocorrência {resultado['id']} cadastrada como ABERTA no dia {resultado['dia_abertura']} "
              f"e colocada no fim da fila.")
    else:
        print("ERRO: a ocorrência NÃO foi cadastrada. Corrija:")
        for erro in resultado:
            print("   - " + erro)


def opcao_atualizar(sistema):
    """ PROTÓTIPO: opcao_atualizar(sistema: dict): None
    Muda a situação de uma ocorrência e registra no histórico. """

    print("\n--- ATUALIZAR SITUAÇÃO ---")
    codigo = pedir_codigo()
    if codigo == "":
        return
    if buscar_por_codigo(sistema["indice"], codigo) is None:
        print("Ocorrência " + codigo + " não encontrada. Use a opção 1 para ver os códigos existentes.")
        return
    atual = sistema["indice"][codigo]["status"]
    print("Situação atual: " + NOMES_STATUS[atual])
    novo = escolher("Nova situação:", STATUS, NOMES_STATUS)
    atualizou, mensagem = atualizar_status(sistema, codigo, novo)
    if atualizou:
        print("OK: " + mensagem)
    else:
        print("ERRO: " + mensagem)


# Cada opção do menu é um dicionário: número, texto na tela e a função que executa
OPCOES = [
    {"numero": "1", "texto": "Listar todas as ocorrências", "funcao": opcao_listar},
    {"numero": "2", "texto": "Consultar uma ocorrência pelo código", "funcao": opcao_consultar},
    {"numero": "3", "texto": "Filtrar por categoria e/ou situação", "funcao": opcao_filtrar},
    {"numero": "4", "texto": "Cadastrar nova ocorrência", "funcao": opcao_cadastrar},
    {"numero": "5", "texto": "Atualizar a situação de uma ocorrência", "funcao": opcao_atualizar},
]


def mostrar_menu(sistema):
    """ PROTÓTIPO: mostrar_menu(sistema: dict): None """

    print("\n" + "-" * 64)
    print(f"MENU | dia simulado {sistema['dia_atual']} | fila de espera: {len(sistema['fila'])}")
    for opcao in OPCOES:
        print(f"{opcao['numero']:>3} - {opcao['texto']}")
    print("  0 - Sair")


def main():
    """ PROTÓTIPO: main(): None
    Carrega os dados e repete o menu até a pessoa escolher sair. """

    sistema = carregar_sistema()
    if sistema is None:
        print("ERRO: arquivos de dados não encontrados na pasta data/ (ocorrencias.csv e historico.csv).")
        return

    mostrar_cabecalho(sistema)
    while True:
        mostrar_menu(sistema)
        escolha = ler_texto("Escolha uma opção: ", "0")
        if escolha == "0":
            print("Até logo! Os dados simulados voltam ao início na próxima execução.")
            break
        executada = False
        for opcao in OPCOES:
            if escolha == opcao["numero"]:
                opcao["funcao"](sistema)
                executada = True
        if not executada:
            print("Opção inválida: digite um número do menu, de 0 a " + str(len(OPCOES)) + ".")


if __name__ == "__main__":
    main()
