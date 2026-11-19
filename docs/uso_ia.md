# Uso de Inteligência Artificial no CourtLife

O enunciado da Global Solution permite usar IA, desde que a equipe compreenda, teste e justifique o que entrega. Este arquivo registra como ela foi usada e como os resultados foram verificados.

## Ferramentas

- **Claude** (Anthropic), em conversa com a equipe, com apoio de ferramentas para escrever e executar código de teste.
- **ElevenLabs** para sintetizar a narração em português brasileiro com a voz Will.
- **Google Flow (Veo 3.1)** para gerar as cenas ilustrativas do bairro.
- **Remotion**, com apoio de IA, para montar a gravação do terminal, os gráficos, os clipes e a narração.

## Como a IA apoiou o desenvolvimento

| Etapa        | Apoio da IA                                                                                                                     | Decisão da equipe                                                                                                                                                                                                                                                                                                                                            |
| ------------ | ------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| Código       | Revisou a primeira versão dos módulos de `src/` (validação, estruturas de dados, consultas, acompanhamento, indicadores e menu) | Revisão das sugestões feitas pela IA e dois ajustes foram aplicados: a conclusão do painel (`indicadores.py`) passou a montar a lista de categorias com laço e `if/elif/else`, sem fatiamento. A reinserção na fila (`acompanhamento.py`) passou a comparar dia e código com `and`/`or`, sem tupla. O menu de `sistema.py` também foi adaptado a esse estilo |
| Dados        | Gerou as ocorrências e o histórico **fictícios** de `data/`, incluindo duas linhas inconsistentes de propósito                  | Conferido que não há dado pessoal e servem para o decorrer do projeto                                                                                                                                                                                                                                                                                        |
| Testes       | Mapeou e sinalizou os cenários de testes para o desenvolvimento de `src/testes.py` e rodou os testes para garantia final        | Alinhado e executado os testes conforme necessário para o objetivo da aplicação                                                                                                                                                                                                                                                                              |
| Documentação | Escreveu o rascunho do `README.md` e `uso_ia.md` após a equipe listar os tópicos e contextualizar o assunto                     | Reescrito tópicos e passado a limpo a versão final                                                                                                                                                                                                                                                                                                           |

## Produção do vídeo de apresentação

A equipe preparou as falas a partir de um rascunho de roteiro sugerido pela IA e gerou os áudios no ElevenLabs, um por bloco. O texto foi definido pela equipe; a voz ouvida no vídeo é sintética.

A demonstração foi gravada com o CourtLife em execução no terminal. As cenas de bairro geradas no Google Flow ilustram os exemplos fictícios. Na montagem do Remotion, os gráficos destacam as estruturas e os indicadores, e os trechos do terminal acompanham os assuntos da narração.

Para conferir a sincronia, comparamos os tempos das falas com os quadros exportados. Na demonstração, cortamos as pausas de digitação para mostrar os resultados do filtro, dos cadastros e do avanço do dia enquanto a narração os explica.

## Como os resultados foram verificados

**Pela IA, durante o desenvolvimento**

- Os 9 testes automáticos de `src/testes.py` passaram (carga e validação, estruturas, consultas, cadastro, atualização, fila e pilha, indicadores, prioridade e mudanças de situação).
- O menu foi executado com 300 sequências de entradas aleatórias (letras, números inválidos, textos longos, campos vazios), a partir de outra pasta, sem nenhum erro do Python.
- Os números do README (totais, proporções, tempos médios e ocorrências urgentes) foram comparados com o cálculo do próprio programa.
- O código foi revisado para usar só o que o enunciado permite: Python básico, funções, condicionais, laços, listas, dicionários e leitura simples de arquivo. Nenhuma biblioteca externa foi usada, só o módulo `os` para achar os arquivos.

**Pela equipe**

- Executado `python src/sistema.py` e percorrido todas as opções do menu.
- Executado `python src/testes.py` e todos os testes passaram.
- Alterado um valor (por exemplo `LIMITE_DIAS_URGENTE` em `constantes.py`) e visto o efeito nas prioridades.
- Conferido o exemplo de uso do README com uma execução real.

## Limites e responsabilidade

- A IA pode errar. Por isso o código foi testado e a equipe revisou o resultado.
- Todos os dados do projeto são fictícios. Nenhum dado pessoal de terceiros foi informado à IA.
- A equipe é responsável pelo código, pelas análises e pelas escolhas descritas no README.
