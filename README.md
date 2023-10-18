# Ferramenta de varredura de tela

## Projeto coletivo da turma da disciplina SCC0281 - Recursos Computacionais de Tecnologia Assistiva

Neste projeto, está sendo desenvolvida uma aplicação com o propósito de realizar uma varredura de tela, com o objetivo de auxiliar pessoas com deficiências a acessarem dispositivos com sistemas operacionais Windows.

### Especificações:

**Programa tem dois usuários:**
- Pessoa com deficiência (PCD);
- Professor.

**Duas opções de execução do programa:**
- Opção 1: Professor inicializa programa de varredura clicando em um icone na barra de tarefas;
- Opção 2: Programa é inicializado automaticamente quando o Windows é iniciado.

**Requisitos para a varredura da Opcao 1**

1. Professor ativa o programa na barra de tarefa do windows para iniciar a varredura
2. PCD seleciona programa desejado com apenas um click, e depois do click deve confirmar que o programa selecionado é o correto; Se não for, recomeça de onde parou
3. Programa apresenta lista de PCDs registrados e pede ao Professor para escolher um deles ou registrar um novo. Ao registrar um usuário, o professor informa o nome e tempo seleção de cada icone durante a varredura (opção padrão: 2 segundos).
4. Uma vez informada a PCD, o programa processa o histórico daquela PCD,  registrado a partir de interações anteriores. Caso aquela pessoa tenha necessitado executar a varredura mais que uma vez até selecionar o programa correto, informar o Professor que pode ser útil ajustar o tempo daquela pessoa e permitir que o Professor ajuste naquele momento. Caso a pessoa sempre selecione o mesmo programa, oferecer a opção de seleção imediata do programa (por exemplo, iniciando a varredura por aquel icone)
5. Durante a execução da varredura, registrar (em um arquivo de log) o histórico das interações da PCD: tempo, programas selecionados, repetições por erro de seleção e outras informações relevante para o processo descrito no item 4.



