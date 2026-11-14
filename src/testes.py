""" Testes do CourtLife: confere, com 'assert', se cada parte do sistema faz o que deveria.
 Cada teste imprime OK, se estiver tudo certo. Se algo falhar, o Python aponta qual conferência falhou. 

 Executar na pasta do projeto:  python src/testes.py """

from constantes import DIA_INICIAL
from validacao import validar_campos, validar_transicao, parece_dado_pessoal
from dados import carregar_sistema
from consultas import normalizar_codigo, buscar_por_codigo, filtrar_ocorrencias
from acompanhamento import cadastrar_ocorrencia, atualizar_status, examinar_proxima, desfazer_ultima
from indicadores import (montar_matriz, contar_por_status, somar_dias, media, avaliar_prioridade,
                         listar_urgentes, proporcao)


def codigos(lista):
    """ PROTÓTIPO: codigos(lista: list): list[str]
    Só os códigos de uma lista de ocorrências, para comparar nos testes. """

    resultado = []
    for ocorrencia in lista:
        resultado.append(ocorrencia["id"])
    return resultado


def teste_carga_e_validacao_do_arquivo():
    sistema = carregar_sistema()
    assert len(sistema["ocorrencias"]) == 14, "deveria haver 14 ocorrências válidas"
    assert len(sistema["rejeitadas"]) == 2, "deveria haver 2 linhas recusadas"
    assert sistema["rejeitadas"][0]["id"] == "007" and "categoria ausente" in sistema["rejeitadas"][0]["erros"][0]
    assert sistema["rejeitadas"][1]["id"] == "012" and "anterior ao dia de abertura" in sistema["rejeitadas"][1]["erros"][0]
    assert len(sistema["historico"]) == 12 and sistema["eventos_ignorados"] == 0
    print("OK  carga dos arquivos e validação das linhas inconsistentes")


def teste_estruturas():
    sistema = carregar_sistema()
    assert sistema["fila"] == ["010", "011", "013", "014", "015", "016"], "fila em ordem de registro"
    assert sistema["pilha"][-1]["codigo"] == "009", "o último evento fica no topo da pilha"
    assert buscar_por_codigo(sistema["indice"], "014")["descricao"].startswith("Buraco")
    assert buscar_por_codigo(sistema["indice"], "099") is None
    assert sistema["hierarquia"]["Parque Orion"]["acessibilidade"] == ["010", "016"]
    matriz = montar_matriz(sistema["ocorrencias"])
    soma = 0
    for linha in matriz:
        for quantidade in linha:
            soma += quantidade
    assert soma == 14, "a matriz deve somar o total de ocorrências"
    print("OK  lista, dicionário, fila, pilha, hierarquia e matriz")


def teste_consultas():
    sistema = carregar_sistema()
    assert normalizar_codigo("14") == "014" and normalizar_codigo("014") == "014"
    assert normalizar_codigo("abc") == "" and normalizar_codigo("") == ""
    abertas_iluminacao = filtrar_ocorrencias(sistema["ocorrencias"], "iluminacao", "aberta")
    assert codigos(abertas_iluminacao) == ["015"]
    assert len(filtrar_ocorrencias(sistema["ocorrencias"], "", "aberta")) == 6
    assert len(filtrar_ocorrencias(sistema["ocorrencias"], "acessibilidade", "")) == 4
    assert len(filtrar_ocorrencias(sistema["ocorrencias"], "", "")) == 14
    assert filtrar_ocorrencias(sistema["ocorrencias"], "limpeza", "em_analise") == []
    print("OK  busca por código e filtros por categoria e situação")


def teste_cadastro():
    sistema = carregar_sistema()
    ok, erros = cadastrar_ocorrencia(sistema, {"categoria": "", "descricao": "Lixo", "bairro": "Vila Aurora", "espaco": "praca"})
    assert not ok and "categoria ausente" in erros[0]
    ok, erros = cadastrar_ocorrencia(sistema, {"categoria": "agua", "descricao": "Lixo", "bairro": "Vila Aurora", "espaco": "praca"})
    assert not ok and "categoria desconhecida" in erros[0]
    ok, erros = cadastrar_ocorrencia(sistema, {"categoria": "limpeza", "descricao": "ligar 11 99999-8888", "bairro": "Vila Aurora", "espaco": "praca"})
    assert not ok and "dado pessoal" in erros[0]
    assert len(sistema["ocorrencias"]) == 14, "cadastro inválido não pode salvar nada"
    ok, nova = cadastrar_ocorrencia(sistema, {"categoria": "limpeza", "descricao": "Mato alto", "bairro": "Vila Aurora", "espaco": "praca"})
    assert ok and nova["id"] == "017", "o código novo vem depois do maior já usado"
    assert nova["status"] == "aberta" and nova["dia_abertura"] == DIA_INICIAL
    assert sistema["fila"][-1] == "017" and "017" in sistema["hierarquia"]["Vila Aurora"]["limpeza"]
    assert parece_dado_pessoal("escreva para ana@email.com") and not parece_dado_pessoal("Poste apagado")
    print("OK  cadastro com validação (categoria, privacidade) e código único")


def teste_atualizacao_e_historico():
    sistema = carregar_sistema()
    ok, mensagem = atualizar_status(sistema, "999", "em_analise")
    assert not ok and "não encontrada" in mensagem
    ok, mensagem = atualizar_status(sistema, "010", "arquivada")
    assert not ok and "desconhecida" in mensagem
    ok, mensagem = atualizar_status(sistema, "010", "concluida")
    assert not ok and "só é permitido ir para EM ANÁLISE" in mensagem, "não pode pular a análise"
    ok, mensagem = atualizar_status(sistema, "001", "aberta")
    assert not ok and "não muda mais" in mensagem
    assert len(sistema["historico"]) == 12, "mudança recusada não entra no histórico"

    ok, mensagem = atualizar_status(sistema, "010", "em_analise")
    assert ok and "010" not in sistema["fila"], "sair de ABERTA tira da fila"
    assert sistema["pilha"][-1] == {"codigo": "010", "dia": 20, "de": "aberta", "para": "em_analise"}
    sistema["dia_atual"] = 23
    ok, mensagem = atualizar_status(sistema, "010", "concluida")
    assert ok and sistema["indice"]["010"]["dia_conclusao"] == 23
    assert len(sistema["historico"]) == 14 and len(sistema["pilha"]) == 14
    print("OK  atualização de situação, regras de mudança e histórico")


def teste_fila_e_desfazer():
    sistema = carregar_sistema()
    ok, mensagem = examinar_proxima(sistema)
    assert ok and sistema["indice"]["010"]["status"] == "em_analise" and sistema["fila"][0] == "011"
    ok, mensagem = desfazer_ultima(sistema)
    assert ok and sistema["indice"]["010"]["status"] == "aberta"
    assert sistema["fila"] == ["010", "011", "013", "014", "015", "016"], "volta ao lugar certo da fila"
    assert len(sistema["historico"]) == 12
    ok, mensagem = atualizar_status(sistema, "005", "concluida")
    assert ok and sistema["indice"]["005"]["dia_conclusao"] == 20
    desfazer_ultima(sistema)
    assert sistema["indice"]["005"]["dia_conclusao"] is None and sistema["indice"]["005"]["status"] == "em_analise"
    for repeticao in range(12):
        desfazer_ultima(sistema)
    ok, mensagem = desfazer_ultima(sistema)
    assert not ok and "Não há atualizações" in mensagem, "pilha vazia é avisada"
    assert len(sistema["fila"]) == 14, "desfeitos todos os eventos, as 14 ocorrências voltam a ser abertas"
    while len(sistema["fila"]) > 0:
        examinar_proxima(sistema)
    ok, mensagem = examinar_proxima(sistema)
    assert not ok and "fila está vazia" in mensagem
    print("OK  fila (examinar próxima) e pilha (desfazer)")


def teste_indicadores():
    sistema = carregar_sistema()
    ocorrencias = sistema["ocorrencias"]
    por_status = contar_por_status(ocorrencias)
    assert por_status == {"aberta": 6, "em_analise": 4, "concluida": 4}
    assert round(proporcao(6, 14), 1) == 42.9 and proporcao(1, 0) == 0.0
    soma, quantidade = somar_dias(ocorrencias, DIA_INICIAL, True, False)
    assert (soma, quantidade) == (20, 4) and media(soma, quantidade) == 5.0
    soma, quantidade = somar_dias(ocorrencias, DIA_INICIAL, False, False)
    assert (soma, quantidade) == (95, 14)
    assert media(0, 0) is None
    print("OK  totais, proporções e tempos médios")


def teste_prioridade():
    sistema = carregar_sistema()
    assert codigos(listar_urgentes(sistema["ocorrencias"], 20)) == ["010", "011"]
    urgente, motivo = avaliar_prioridade(sistema["indice"]["006"], 20)
    assert not urgente and "EM ANÁLISE" in motivo, "NÃO em análise: acessibilidade antiga já examinada não é urgente"
    urgente, motivo = avaliar_prioridade(sistema["indice"]["016"], 20)
    assert not urgente and "dia(s) de espera" in motivo, "acessibilidade nova ainda não passou do limite"
    urgente, motivo = avaliar_prioridade(sistema["indice"]["013"], 20)
    assert not urgente and "nem acessibilidade" in motivo, "limpeza em calçada não é convivência nem acessibilidade"
    urgentes_dia_25 = codigos(listar_urgentes(sistema["ocorrencias"], 25))
    assert "016" in urgentes_dia_25 and "013" not in urgentes_dia_25, "com o passar dos dias, 016 vira urgente"
    print("OK  regra de prioridade (E, OU, NÃO) e suas explicações")


def teste_transicoes():
    assert validar_transicao("aberta", "em_analise") == ""
    assert validar_transicao("em_analise", "concluida") == ""
    assert validar_transicao("aberta", "concluida") != ""
    assert validar_transicao("concluida", "em_analise") != ""
    assert validar_campos({"categoria": "iluminacao", "descricao": "Poste", "bairro": "Parque Orion", "espaco": "quadra"}) == []
    print("OK  mudanças de situação permitidas e recusadas")


def main():
    """ PROTÓTIPO: main(): None
    Roda todos os testes em sequência. """

    teste_carga_e_validacao_do_arquivo()
    teste_estruturas()
    teste_consultas()
    teste_cadastro()
    teste_atualizacao_e_historico()
    teste_fila_e_desfazer()
    teste_indicadores()
    teste_prioridade()
    teste_transicoes()
    print("\nTodos os testes passaram.")


if __name__ == "__main__":
    main()
