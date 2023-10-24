# Amanda Kasat - 13727210
import pyautogui
import time
import keyboard
import tkinter as tk
import threading

# Lista para armazenar as coordenadas dos ícones
desktop_icones = []

# Valor baseado na minha tela, pode ser alterado dependendo da disposição dos ícones na tela
num_atalhos_hor = 3
num_atalhos_ver = 8

# inicinado o item como 0, por ser o primeiro elemento do vetor
item = 0

# Função para calcular as coordendas e colocar todas no vetor
for i in range(num_atalhos_hor):
    # "a" representa os pixels da horizontal e fazem parte da Progressão Aritmética (50, 150, 250, ...)
    a = 50 + i * 100

    for j in range(num_atalhos_ver):
        # "b" representa os pixels da vertical e fazem parte da Progressão Aritmética (50, 170, 290, ...)
        b = 50 + j * 120

        # Incluindo a coordenada no nosso vetor
        coordenada = (a, b)
        desktop_icones.append(coordenada)

# Função principal para varrer ícones na área de trabalho. Caso nenhum valor seja passado como parâmetro,
# Será assumido o valor 0
def varrer_area_de_trabalho(item_atual = 0):
    x, y = desktop_icones[item_atual]

    # clicando no ícone pelas coordenadas
    pyautogui.click(x, y)
    print(f"Ícone {item_atual}/{len(desktop_icones)} concluído.")

    # time sleep curtinho para permitir que o usuário clique com calma, está comentado pois não sei se é realmente necessário e qual
    #o melhor valor
    # time.sleep(.4)

# Função para verificar o tempo de pressionamento de uma tecla, importante para o "enter adaptado"
def tempo_pressionamento():
    # Tempos de início e fim, inícia como zero (None)
    tempo_inicio = None
    tempo_fim = None

    while True:
        try:
            # Lê a tecla pressionada pelo usuário
            event = keyboard.read_event()
            # Tanto faz se o usuário apertar a seta direita ou esquerda, ele verifica apenas o tempo de início. Pra ele não resetar
            #o tempo de início sempre, ele verifica se o tempo de início é None
            if event.event_type == keyboard.KEY_DOWN and (event.name == "right") and tempo_inicio == None:
                tempo_inicio = time.time()
            # Quando a tecla deixar de ser pressionada, o tempo também é contado
            if event.event_type == keyboard.KEY_UP and (event.name == "right"):
                tempo_fim = time.time()
                # Se o tempo foi significante, retornar a diferença, que seria o tempo total de pressionamento
                if tempo_inicio is not None:
                    return float(tempo_fim - tempo_inicio)
                # Caso contrário, retorna 0
                else:
                    return 0.0
        # Se o usuário quiser desistir, também retornar 0
        except KeyboardInterrupt:
            return 0.0

def abrir_aplicativo():
    x, y = desktop_icones[item]
    # faz dois cliques, pois nas minhas configurações os aplicativos abrem com dois cliques 
    pyautogui.click(x, y)
    pyautogui.click(x, y)
    fechar_janela()
    exit(0) # saiu com sucesso

def reinicia_varredura():
    global item
    item = 0
    fechar_janela()

def fechar_janela():
    janela.destroy()

# vetor com as coordendas dos botões da janela para poder fazer a varredura
janela_coordendas = [(250, 200), (250, 250), (250, 300)]

def varredura_janela():
    botao_atual = 0
    # interação para que a janela apareça
    pyautogui.click(250, 150)
    # por python não possuir do-while, fiz um while true com verificação
    while True:
        # verificação pra não dar segmentation fault
        if (botao_atual>2):
            # reiniciando o ciclo
            botao_atual=0
        # pegando as coordenadas atuais e movendo o cursos para ela
        x, y = janela_coordendas[botao_atual]
        pyautogui.moveTo(x,y)

        # Se a tecla for pressionada por mais de 2 segundos, será feito um outro clique com a intenção de
        # clicar em um botão
        tempo_total = tempo_pressionamento()
        # definimos o tempo de pressionamento para 2 segundos
        if(tempo_total > 2):
            # sai da varredura
            pyautogui.click(x, y)
            break
        else:
            botao_atual += 1
        
def janela_interacao():
    # Iniciar a varredura em segundo plano
    varredura_thread = threading.Thread(target=varredura_janela)
    varredura_thread.daemon = True
    varredura_thread.start()

    # configurações iniciais da janela
    janela.title("Confirmação de aplicativo")
    janela.geometry("300x200+100+100")

    text_orientacao = tk.Label(janela, text="Você deseja entrar nesse aplicativo?")
    text_orientacao.grid(column = 0, row = 0, padx = 10, pady = 10)
    botao_aceito = tk.Button(janela, text="Sim", command=abrir_aplicativo)
    botao_reiniciar = tk.Button(janela, text="Não, quero voltar ao início da varredura", command=reinicia_varredura)
    botao_continuar = tk.Button(janela, text="Não, quero seguir com a varredura", command=fechar_janela)
    botao_aceito.grid(column = 0, row = 1, padx = 10, pady = 5)
    botao_reiniciar.grid(column = 0, row = 2, padx = 10, pady = 5)
    botao_continuar.grid(column = 0, row = 3, padx = 10, pady = 5)
    janela.mainloop()

def varredura_completa():
    # chama a função para varrer a área de trabalho. Usando global pr aindicar que vamos alterar a variável global
    global item
    varrer_area_de_trabalho(item)

    # como o usuário tem a opção de voltar na varredura, precisamos verificar qual tecla foi acionada.
    # Caso foi a seta esquerda, ele vai voltar, caso foi a direita, vai avançar.
    event = keyboard.read_event(suppress=True)

    # Se a tecla for pressionada por mais de 2 segundos, será feito um outro clique com a intenção de
    #abrir o aplicativo
    tempo_total = tempo_pressionamento()
    print (tempo_total)
    # definimos o tempo de pressionamento para 2 segundos
    if(tempo_total > 2):
        print("pressed more then 2s")
        # Cria uma janela
        global janela
        janela = tk.Tk()
        janela_interacao()
    else:
        if(keyboard.KEY_DOWN and event.name == 'right'):
            item = item + 1
        # caso uma tecla inválida for teclada, retonrar exit pois é um erro
        else:
            exit()


if __name__ == "__main__":
    # para que o ícone seja acessado, ele deve ter uma posição válida no vetor, ou seja, maior ou igual a 0 e
    # menor que o tamanho do vetor de coordenadas
    while(item >= 0 and item < len(desktop_icones)):
        # fica esperando uma interação do usuário até que o usuário queira parar e nehuma condição for quebrada
        try:
            varredura_completa()
        # para quando o usuário fazer "Control + C" poder sair
        except KeyboardInterrupt:
            exit()