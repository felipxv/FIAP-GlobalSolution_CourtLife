<h1 align="center">FIAP - Faculdade de Informática e Administração Paulista</h1>
<p align="center">
<a href="https://www.fiap.com.br/">
  <img src="assets/logo-fiap.png"
       alt="FIAP - Faculdade de Informática e Administração Paulista"
       width="40%">
</a>
</p>

<h1 align="center">CourtLife: Neighborhood Action Dashboard</h1>

## Equipe

**Nome da equipe:** CourtLife

Integrantes (grupo cadastrado no FIAP ON):

- <a href="https://github.com/felipxv">Felipe de Barros Franco</a> RM575777
- <a href="https://github.com/Guilherme-AVVO">Guilherme Santos</a> RM575786

## Descrição

O **CourtLife** é um painel de terminal para registrar e acompanhar ocorrências de infraestrutura e conservação em **espaços de convivência** de um bairro: quadras, praças, pistas de caminhada, calçadas e rotas até a escola.

O bairro é **fictício** e dividido em três localidades genéricas: **Vila Aurora**, **Jardim Estelar** e **Parque Orion**. Todos os dados são inventados, sem nomes, telefones nem endereços reais.

**O problema.** Quando uma quadra tem a tela rasgada ou uma rampa está quebrada, o registro costuma ficar espalhado (grupos de mensagens, papel, conversa) e ninguém sabe o que já foi visto. Além disso, todas as ocorrências parecem ter o mesmo peso, embora um espaço de encontro parado por semanas afaste as pessoas e uma rampa quebrada exclua quem tem dificuldade de locomoção.

**O público beneficiado.** Moradores que precisam acompanhar suas solicitações e quem organiza a manutenção do bairro, com atenção especial a pessoas com mobilidade reduzida e a quem usa os espaços coletivos para esporte e encontro.

### O que o sistema faz

| Funcionalidade                                                                              | Onde                               |
| ------------------------------------------------------------------------------------------- | ---------------------------------- |
| Ler as ocorrências de um arquivo CSV e recusar as linhas com campo ausente ou inconsistente | `src/dados.py`, `src/validacao.py` |
| Listar ocorrências (código, categoria, local genérico e situação)                           | `src/consultas.py`                 |
| Consultar por código, filtrar por categoria e/ou situação                                   | `src/consultas.py`                 |
| Cadastrar nova ocorrência com verificação dos campos obrigatórios                           | `src/acompanhamento.py`            |
| Atualizar a situação e guardar a mudança no histórico                                       | `src/acompanhamento.py`            |
| Examinar a próxima da fila e desfazer a última atualização                                  | `src/acompanhamento.py`            |
| Indicadores, prioridades e interpretação dos números                                        | `src/indicadores.py`               |
| Menu de terminal                                                                            | `src/sistema.py`                   |

### O diferencial: prioridade e impacto no convívio

Em vez de só contar chamados abertos, o CourtLife faz duas coisas a mais:

1. **Regra de prioridade.** Marca como **URGENTE** a ocorrência que afeta um espaço de convivência ou a acessibilidade, está esperando exame há mais de 5 dias e ainda não foi examinada. O sistema explica, em texto, por que cada ocorrência é ou não urgente.
2. **Dias com o espaço comprometido.** Mede por quanto tempo cada lugar ficou (ou está) com o problema, que é o tempo simulado de acompanhamento com um significado para a comunidade.

### Dados de origem

Os dados ficam em `data/` e são lidos de arquivos CSV simples, com **ponto e vírgula** entre os campos.

**`data/ocorrencias.csv`** (16 linhas de dados, 14 válidas e 2 propositalmente inconsistentes):

| Campo           | Obrigatório                    | Valores                                                  |
| --------------- | ------------------------------ | -------------------------------------------------------- |
| `id`            | sim                            | código único de 3 dígitos (`001`, `002`...)              |
| `categoria`     | sim                            | `iluminacao`, `acessibilidade`, `limpeza`, `conservacao` |
| `descricao`     | sim                            | texto curto, sem dado pessoal                            |
| `bairro`        | sim                            | `Vila Aurora`, `Jardim Estelar`, `Parque Orion`          |
| `espaco`        | sim                            | `quadra`, `praca`, `pista`, `rota_escolar`, `calcada`    |
| `dia_abertura`  | sim                            | número do dia simulado (1, 2, 3...)                      |
| `status`        | sim                            | `aberta`, `em_analise`, `concluida`                      |
| `dia_conclusao` | só se `status` for `concluida` | número do dia simulado                                   |

A data é **simulada**: um número de dia, e o sistema começa no **dia 20**. O local genérico mostrado na tela junta o tipo de espaço com o bairro (por exemplo, "Quadra - Vila Aurora").

**Significado das situações:**

| Situação     | Significado                                                         |
| ------------ | ------------------------------------------------------------------- |
| `aberta`     | registrada, mas não examinada; espera na fila por ordem de registro |
| `em_analise` | examinada e alguém está avaliando como resolver                     |
| `concluida`  | problema resolvido (simulado); não muda mais                        |

Mudanças permitidas: `aberta` → `em_analise` → `concluida`, sempre nessa ordem.

**`data/historico.csv`** (12 eventos): cada linha registra uma mudança de situação (`codigo;dia;de;para`).

**As duas linhas inconsistentes** (tratadas pela validação ao carregar):

| Linha | Código | Problema                                         | Mensagem do sistema                                    |
| ----- | ------ | ------------------------------------------------ | ------------------------------------------------------ |
| 8     | 007    | `categoria` vazia                                | `categoria ausente (campo obrigatório)`                |
| 13    | 012    | concluída no dia 3, antes de ser aberta no dia 9 | `dia de conclusão (3) anterior ao dia de abertura (9)` |

## Estrutura de pastas

- **`data/`** Bases de dados fictícias: `ocorrencias.csv` e `historico.csv`.

- **`docs/`** Documentação do projeto:
  - `uso_ia.md`: registro do uso de inteligência artificial;
  - `CourtLife-Contexto-do-Projeto.pdf`: documento técnico com a regra de prioridade em circuito lógico, as estruturas de dados e o capítulo das fases em que cada uma foi vista, a situação de cada requisito e os valores esperados na tela.

- **`src/`** Código-fonte em Python:
  - `sistema.py`: menu e conversa com o usuário (arquivo executável);
  - `constantes.py`: categorias, situações, espaços e limites padronizados;
  - `validacao.py`: regras de validação;
  - `dados.py`: leitura dos arquivos e montagem das estruturas de dados;
  - `consultas.py`: busca, filtros e formatação das listagens;
  - `acompanhamento.py`: cadastro, mudança de situação, fila e pilha;
  - `indicadores.py`: totais, proporções, matriz, tempos e prioridade;
  - `testes.py`: testes automáticos.

- **`assets/`** Logo da FIAP usada neste README.

- **`README.md`** Este arquivo.

## Estruturas de dados e justificativa

| Estrutura                                        | Onde está                | Por que foi escolhida                                                                                              |
| ------------------------------------------------ | ------------------------ | ------------------------------------------------------------------------------------------------------------------ |
| **Lista** de dicionários                         | `sistema["ocorrencias"]` | guarda todas as ocorrências em ordem de registro e permite percorrer para listar, filtrar e calcular               |
| **Dicionário** `{código: ocorrência}`            | `sistema["indice"]`      | acha uma ocorrência direto pelo código, sem percorrer a lista inteira                                              |
| **Fila** (primeiro a entrar, primeiro a sair)    | `sistema["fila"]`        | organiza as ocorrências ABERTAS por ordem de registro: a mais antiga é a primeira a ser examinada                  |
| **Pilha** (último a entrar, primeiro a sair)     | `sistema["pilha"]`       | guarda as últimas atualizações: o evento mais recente fica no topo, para consultar os recentes e desfazer a última |
| **Lista** de eventos                             | `sistema["historico"]`   | registro completo e em ordem de todas as mudanças de situação                                                      |
| **Hierarquia** (dicionário dentro de dicionário) | `sistema["hierarquia"]`  | bairro → categoria → códigos; mostra o que cada bairro tem, por tipo de problema                                   |
| **Matriz** (lista de listas)                     | `montar_matriz()`        | resume a quantidade por categoria (linhas) e por situação (colunas)                                                |

A hierarquia ajuda a organizar as informações porque separa os problemas por localidade e por tipo, que é como quem cuida do bairro costuma pensar (por exemplo, "o que está pendente de iluminação no Jardim Estelar?"). A fila é quem decide qual ocorrência a opção 6 examina e a pilha é quem a opção 8 usa para desfazer.

## Regras lógicas principais

**Validação do cadastro** (`validar_campos`): categoria, descrição, bairro e tipo de espaço são obrigatórios; categoria e espaço precisam ser um dos valores padronizados; a descrição não pode conter e-mail nem telefone.

**Mudança de situação** (`validar_transicao`): só são permitidas `aberta → em_analise` e `em_analise → concluida`. O sistema recusa situação desconhecida, repetir a situação atual, pular a análise e alterar uma ocorrência já concluída.

**Consulta** (`filtrar_ocorrencias`): uma ocorrência aparece no resultado se combinar com a categoria **e** com a situação pedidas; um filtro em branco vale para qualquer valor.

### Expressões booleanas usadas

| Onde               | Expressão                                                                                                           | Operadores   |
| ------------------ | ------------------------------------------------------------------------------------------------------------------- | ------------ |
| Filtro             | `passa_categoria = categoria == "" or ocorrencia["categoria"] == categoria` e `if passa_categoria and passa_status` | OR, AND      |
| Privacidade        | `"@" in texto or quantidade_digitos >= 8`                                                                           | OR           |
| Conclusão sem data | `status == "concluida" and conclusao == ""`                                                                         | AND          |
| Volta à fila       | `abriu_antes or (mesmo_dia and codigo_menor)`                                                                       | OR, AND      |
| Prioridade         | `urgente = (convivencia or acessibilidade) and parada and not em_andamento`                                         | OR, AND, NOT |

**A expressão de prioridade, em detalhe** (`avaliar_prioridade`):

```python
convivencia   = ocorrencia["espaco"] in ESPACOS_CONVIVENCIA          # quadra, praça ou pista
acessibilidade = ocorrencia["categoria"] == "acessibilidade"
parada        = dias_desde_a_abertura > LIMITE_DIAS_URGENTE           # mais de 5 dias
em_andamento  = ocorrencia["status"] == "em_analise" or ocorrencia["status"] == "concluida"

urgente = (convivencia or acessibilidade) and parada and not em_andamento
```

**Por que cada resultado acontece**, no dia 20, com os dados iniciais:

| Ocorrência                                | convivência ou acessibilidade | parada (> 5 dias) | não em andamento        | Resultado   |
| ----------------------------------------- | ----------------------------- | ----------------- | ----------------------- | ----------- |
| 010 (acessibilidade, aberta há 9 dias)    | sim                           | sim               | sim                     | **URGENTE** |
| 011 (limpeza em quadra, aberta há 7 dias) | sim                           | sim               | sim                     | **URGENTE** |
| 006 (acessibilidade, há 13 dias)          | sim                           | sim               | **não** (já em análise) | normal      |
| 016 (acessibilidade em praça, há 1 dia)   | sim                           | **não**           | sim                     | normal      |
| 013 (limpeza em calçada, há 5 dias)       | **não**                       | não               | sim                     | normal      |

O sistema mostra esse raciocínio na tela (opções 2 e 10), com frases como `não é urgente: só 1 dia(s) de espera (limite 5)`.

## Indicadores, fórmulas e interpretação

Os indicadores usam apenas somas, divisões e laços. Resultado com os dados iniciais (dia 20):

| Indicador                             | Fórmula                                                         | Resultado                                                                                |
| ------------------------------------- | --------------------------------------------------------------- | ---------------------------------------------------------------------------------------- |
| Total por categoria e proporção       | `% = total da categoria / total de ocorrências × 100`           | Iluminação 4 (28,6%), Acessibilidade 4 (28,6%), Limpeza 3 (21,4%), Conservação 3 (21,4%) |
| Total por situação e proporção        | `% = total na situação / total de ocorrências × 100`            | Abertas 6 (42,9%), Em análise 4 (28,6%), Concluídas 4 (28,6%)                            |
| Pendências                            | `abertas + em análise`                                          | 6 + 4 = 10                                                                               |
| Tempo médio até a conclusão           | `soma(dia de conclusão − dia de abertura) / nº de concluídas`   | 20 / 4 = 5,0 dias                                                                        |
| Dias médios com o espaço comprometido | `soma((conclusão ou dia atual) − abertura) / nº de ocorrências` | 95 / 14 = 6,8 dias                                                                       |
| Matriz categoria × situação           | contagem em dois laços                                          | tabela no painel (opção 9)                                                               |

**Interpretação.** No conjunto simulado, 10 das 14 ocorrências (71,4%) ainda estão pendentes. Iluminação e acessibilidade têm o maior número de pendências (3 cada). As ocorrências pendentes esperam em média 7,5 dias, mais que os 5,0 dias que as concluídas levaram, o que sugere que o atendimento está ficando mais lento e que a fila precisa andar. Duas ocorrências são urgentes (010, de acessibilidade, e 011, de uma quadra). Como os dados são inventados, os números mostram o método de análise por hora, não a realidade de um bairro.

## Como executar o código

**Pré-requisito:** Python 3. Foi testado com o Python 3.13 e usa só recursos básicos da linguagem (nenhuma biblioteca instalada à parte).

```bash
git clone https://github.com/felipxv/FIAP-GlobalSolution_CourtLife.git
cd FIAP-GlobalSolution_CourtLife
python src/sistema.py
```

Para rodar os testes automáticos:

```bash
python src/testes.py
```

Em alguns sistemas o comando é `python3` em vez de `python`.

### Menu

```
 1 - Listar todas as ocorrências           8 - Desfazer a última atualização
 2 - Consultar uma ocorrência pelo código  9 - Ver indicadores
 3 - Filtrar por categoria e/ou situação  10 - Ver prioridades (urgentes)
 4 - Cadastrar nova ocorrência            11 - Ver a hierarquia bairro > categoria
 5 - Atualizar a situação                 12 - Avançar o dia simulado
 6 - Examinar a próxima da fila           13 - Ajuda: significado das situações
 7 - Ver eventos recentes (pilha)          0 - Sair
```

### Exemplo de uso

O que a pessoa digita aparece depois dos dois pontos. Os dados são os do arquivo inicial.

**Abertura e validação dos dados**

```
Dados carregados: 14 ocorrências válidas, 12 eventos no histórico.
AVISO: 2 linha(s) do arquivo foram recusadas pela validação:
   linha 8 (código 007): categoria ausente (campo obrigatório)
   linha 13 (código 012): dia de conclusão (3) anterior ao dia de abertura (9)
```

**Consulta:** ocorrências abertas de iluminação (opção 3, categoria 1, situação 1)

```
--- RESULTADO DO FILTRO ---
COD | CATEGORIA      | LOCAL                                | SITUAÇÃO
015 | Iluminação     | Rota da escola - Jardim Estelar      | ABERTA
Total: 1 ocorrência(s).
```

**Cadastro** (opção 4: iluminação, "Poste apagado perto da quadra", "Vila Aurora", quadra)

```
OK: ocorrência 017 cadastrada como ABERTA no dia 20 e colocada no fim da fila.
```

**Cadastro recusado** (categoria em branco)

```
ERRO: a ocorrência NÃO foi cadastrada. Corrija:
   - categoria ausente (campo obrigatório)
```

**Alteração de status** (opção 5, código 17, nova situação 2)

```
OK: Ocorrência 017: ABERTA -> EM ANÁLISE (dia 20).
```

**Mudança recusada** (tentar concluir uma ocorrência que ainda está aberta)

```
ERRO: Mudança recusada: de ABERTA só é permitido ir para EM ANÁLISE.
```

**Indicadores** (opção 9, depois do cadastro e da alteração acima)

```
Categoria         ABERTA  EM ANÁLISE  CONCLUÍDA  Total       %
Iluminação             1           3          1      5    33,3
Acessibilidade         2           1          1      4    26,7
Limpeza                2           0          1      3    20,0
Conservação            1           1          1      3    20,0

Tempo médio até a conclusão = 20 / 4 = 5,0 dias
Dias médios com o espaço comprometido = 95 / 15 = 6,3 dias

CONCLUSÃO
- 11 de 15 ocorrências (73,3%) ainda estão pendentes.
- Mais pendências em: Iluminação (4).
- 2 ocorrência(s) urgente(s): espaço de convivência ou acessibilidade esperando exame há mais de 5 dias.
```

**Saída** (opção 0)

```
Até logo! Os dados simulados voltam ao início na próxima execução.
```

## Acessibilidade, inclusão e privacidade

**Acessibilidade e inclusão**

- A acessibilidade urbana (rampas, pisos táteis, corrimãos, rebaixamentos) é uma categoria que entra na regra de prioridade: uma ocorrência dela com mais de 5 dias de espera, sem exame, vira urgente mesmo fora de um espaço de convivência.
- A interface é só texto, com menu numerado e mensagens que dizem o que aconteceu e o que fazer. Não depende de cor, de símbolo, de som nem de mouse. Por ser texto puro, tende a funcionar bem com leitores de tela (não foi testado com um).
- As mensagens de erro explicam o motivo e como corrigir; o sistema aceita `14` ou `014` como código; as situações aparecem por extenso.

**Privacidade**

- Todos os dados são fictícios; não há nome, telefone, e-mail nem endereço exato, só bairro e tipo de espaço.
- No cadastro, o sistema avisa para não escrever dados pessoais e **recusa** descrições com `@` ou com 8 ou mais dígitos (como um telefone).
- Os dados ficam só na memória durante a execução e não são enviados a lugar nenhum.

## Vídeo de apresentação

- **[Vídeo no YouTube (não listado)](https://youtu.be/bUUkLBlnqu4)** - Apresentação do CourtLife em funcionamento.

## Links e Observações

### Decisões Técnicas

> Arquivos CSV com ponto e vírgula, lidos com `open()` e `split(";")`: o formato é simples de explicar e permite editar os dados em qualquer editor de texto.
>
> A data é um número de dia simulado, o que dispensa bibliotecas de datas e deixa o cálculo de tempo uma subtração.
>
> O programa é dividido em módulos pequenos (dados, validação, consultas, acompanhamento, indicadores e menu), cada um com um papel, para ser fácil de testar e de explicar.
>
> O estado do sistema fica em um dicionário (`sistema`) que as funções recebem e alteram, sem variáveis globais que mudam.
>
> Só foram usados Python básico, funções, condicionais, laços, listas, dicionários e leitura simples de arquivo, como pede o enunciado. O único módulo importado é o `os`, para achar os arquivos de dados a partir do caminho do próprio programa.

### Observações Gerais

- **Participação na Competição:** Global Solution 2026.2 da FIAP, desafio CitizenTech (case Neighborhood Action Dashboard).
- **Uso de IA:** a inteligência artificial apoiou o desenvolvimento; o registro de como os resultados foram verificados está em [`docs/uso_ia.md`](docs/uso_ia.md).

## Conclusões, limitações e aprendizados

**Conclusões.** O protótipo cumpre o ciclo pedido: cadastrar, validar, consultar, filtrar, atualizar a situação com histórico e calcular indicadores, com uma regra de prioridade que explica as próprias decisões.

**Limitações**

- Os dados são simulados e voltam ao início a cada execução (o cadastro e as atualizações não são gravados nos arquivos).
- Não há integração com órgãos públicos, login nem promessa de atendimento das demandas.
- A proteção de privacidade é simples: na descrição, recusa `@` (e-mail) e 8 ou mais dígitos no total (telefone); um texto com muitos números legítimos também seria recusado.
- Os limites da prioridade (5 dias, quais espaços são de convivência) são escolhas da equipe e não vêm de uma norma.
- A interface é só de terminal e não foi testada por pessoas que usam leitor de tela.

**Trabalhos futuros.** Gravar as alterações nos arquivos, ter perfis de morador e de gestor, usar inteligência artificial para sugerir a categoria de uma descrição e fazer uma versão com banco de dados e interface web.

**Aprendizados.** Aprendemos que escolher a estrutura de dados certa muda o jeito de pensar o problema: a fila deixa claro quem deve ser atendido primeiro, a pilha torna simples desfazer a última atualização e o dicionário acha uma ocorrência pelo código sem percorrer a lista inteira. Também vimos que validar os dados antes de aceitá-los evita erros mais à frente, como as linhas inconsistentes do arquivo, os cadastros sem categoria e as descrições com telefone ou e-mail, e que testar os casos de erro, e não só os que funcionam, foi o que mais mostrou falhas. Por fim, ao revisar o código um do outro, simplificamos trechos para usar só o que vimos nas aulas, o que deixou o programa mais fácil de explicar.

---
