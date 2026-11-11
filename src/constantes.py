# Categorias de ocorrência
CATEGORIAS = ["iluminacao", "acessibilidade", "limpeza", "conservacao"]
NOMES_CATEGORIA = {
    "iluminacao": "Iluminação",
    "acessibilidade": "Acessibilidade",
    "limpeza": "Limpeza",
    "conservacao": "Conservação",
}

# Situações possíveis de uma ocorrência e o que cada uma significa
STATUS = ["aberta", "em_analise", "concluida"]
NOMES_STATUS = {
    "aberta": "ABERTA",
    "em_analise": "EM ANÁLISE",
    "concluida": "CONCLUÍDA",
}
SIGNIFICADO_STATUS = {
    "aberta": "registrada e ainda não examinada; espera na fila por ordem de registro.",
    "em_analise": "já foi examinada e alguém está avaliando como resolver.",
    "concluida": "problema resolvido (simulado); a ocorrência não muda mais.",
}

# Tipos de espaço coletivo onde a ocorrência acontece
ESPACOS = ["quadra", "praca", "pista", "rota_escolar", "calcada"]
NOMES_ESPACO = {
    "quadra": "Quadra",
    "praca": "Praça",
    "pista": "Pista de caminhada",
    "rota_escolar": "Rota da escola",
    "calcada": "Calçada",
}
# Espaços onde a vizinhança se encontra: um problema neles afasta as pessoas
ESPACOS_CONVIVENCIA = ["quadra", "praca", "pista"]

# Mudanças de situação permitidas: de qual situação para quais
TRANSICOES = {
    "aberta": ["em_analise"],
    "em_analise": ["concluida"],
    "concluida": [],
}

# Uma ocorrência parada há mais dias que isso, sem análise, pode virar urgente
LIMITE_DIAS_URGENTE = 5

# Dia simulado em que o sistema começa (os dados vão do dia 1 ao dia 19)
DIA_INICIAL = 20
