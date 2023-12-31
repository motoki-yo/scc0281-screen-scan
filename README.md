# Ferramenta de varredura de tela

## Projeto coletivo da turma da disciplina SCC0281 - Recursos Computacionais de Tecnologia Assistiva

Neste projeto, está sendo desenvolvida uma aplicação com o propósito de realizar uma varredura de tela, com o objetivo de auxiliar pessoas com deficiências a acessarem dispositivos com sistemas operacionais Windows.

## Especificações:

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

## Nosso Programa

**Lógica do programa:**
Usei a biblioteca autoGui pois foi a melhor que encontrei que fizesse interações com a tela, como não conseguir uma forma de automatizar a posição do ponteiro para que ele acerte cada um dos aplicativos, o máximo que consegui foi que ele reconhecesse ícones que vem default, como o Explorador de Arquivos e a Lixeira, fiz uma continha usando os pixels para poder guiar o ponteiro. Os valores encontrados foram encontrados empiricamente. Uma opção para autiomzatizar seria a partir do reconhecimento de imagens. Como só possuímos dois botões, pensei em manter qualquer um dos dois pressionado por 3 segundos ou mais para funcionar como o Enter. Cada clique faz uma ação na varredura, ela não faz por tempo e sim por clique. Criei um executável para facilitar o uso pelo usuário, pois ele pode ser facilmente configurado para abrir sempre que o usuário abrir o Windows, por enquanto ele não retorna mensagens ao usuário por pop-up, as mensagens só aparecem usando o código por um IDLE.

**Teclas importantes:**
-> (seta direita): avança na varredura dos ícones
<- (seta esqeurda): retorna na varredura dos ícones
<- ou -> (por mais de 3 segundos): faz outro clique, coma a ideia de abrir o aplicativo

**Observações importantes:**
- foi utlizado a biblioteca Keyboard para pegar a informação da tecla que foi pressionada, pois sem ela, era necessário ficar escrevendo no terminal e agora ela entende só clicando na tela.

## Gitflow Workflow
![image](https://i.imgur.com/uyGhvSh.png)

Esse é o padrão que iremos utilizar em nossos repositórios com o objetivo de facilitar e melhorar a organização da base de código do sistema desenvolvido.

### Grupos de Branches
Os grupos de branches são main, develop, release, feature e hotfix. Abaixo uma breve descrição sobre cada um.

#### Main
O branch main contém o histórico das versões lançadas em produção e modificações de novas features não devem ser adicionadas a essa branch.

#### Develop
O branch develop é o branch em que toda a evolução do repositório deve acontecer, ele será o agragador de novas features e novas versões de produção surgirão a partir dele.

#### Release
O branch release será utilizado quando existirem features suficientes em develop para que seja deployada uma nova versão funcional ou se alguma data de deploy esteja se aproximando. Esse branch não deve receber atualizações, somente correção de bugs, documentação e tarefas relacionadas ao release em sí.

#### Feature
O branch feature contempla cada nova feature a ser desenvolvida que, posteriomente, será adicionada à branch develop.

#### Hotfix
O branch hotfix é basicamente um branch de correções de versões de produção, isto é, vão para esse branch somente correções necessarias em uma versão lançada no branch main.

##

### Começando com o padrão

Os braches main e develop são criados por padrão e é comum o branch de desenvolvimento estar à frente em relação aos commits do branch principal, portanto após clonar o repositório mude para o branch develop e traga as alterações por garantia:

```
git checkout develop
``` 
```
git pull origin develop
```


Após a mudança para o branch de desenvolvimento o próximo passo para começar a desenvolver uma nova feature é criar a branch da feature em questão a partir da develop. Assumindo que você já está na branch develop execute:

```
git checkout -b feature/<new-feature
```


Estando nesse branch exclusivo da nova feature que será implementada você tem a liberdade de fazer commits e após encerrar a implementação pode dar push para o repo remoto. Se o branch remoto não existe ainda pode ser necessário cria-lo assim que der push, para isso:

```
git push --set-upstream origin feature/<new-feature>
```


Para nossos projetos será necessário abrir um PR (Pull Request) para realizar o merge do branch de feature que acabou de ser implementado e TESTADO EM DEV para o branch develop tal como merges do branch release para o branch main. 

##

