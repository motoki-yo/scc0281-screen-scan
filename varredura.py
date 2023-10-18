# Amanda Kasat - 13727210
import pyautogui
import time
import keyboard

# Lista para armazenar as coordenadas dos ícones
desktop_icones = []

# Valor baseado na minha tela, pode ser alterado dependendo da disposição dos ícones na tela
num_atalhos_hor = 2
num_atalhos_ver = 8

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
            if event.event_type == keyboard.KEY_DOWN and (event.name == "right" or event.name == "left") and tempo_inicio == None:
                tempo_inicio = time.time()
            # Quando a tecla deixar de ser pressionada, o tempo também é contado
            if event.event_type == keyboard.KEY_UP and (event.name == "right" or event.name == "left"):
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

if __name__ == "__main__":
    # inicinado o item como 0, por ser o primeiro elemento do vetor
    item = 0

    # para que o ícone seja acessado, ele deve ter uma posição válida no vetor, ou seja, maior ou igual a 0 e
    # menor que o tamanho do vetor de coordenadas
    while(item >= 0 and item < len(desktop_icones)):
        # fica esperando uma interação do usuário até que o usuário queira parar e nehuma condição for quebrada
        try:
            # chama a função para varrer a área de trabalho
            varrer_area_de_trabalho(item)

            # como o usuário tem a opção de voltar na varredura, precisamos verificar qual tecla foi acionada.
            # Caso foi a seta esquerda, ele vai voltar, caso foi a direita, vai avançar.
            event = keyboard.read_event(suppress=True)

            # Se a tecla for pressionada por mais de 3 segundos, será feito um outro clique com a intenção de
            #abrir o aplicativo
            tempo_total = tempo_pressionamento()
            print (tempo_total)
            # definimos o tempo de pressionamento para 3 segundos, mas isso pode ser alterado
            if(tempo_total > 3):
                print("pressed more then 3s")
                x, y = desktop_icones[item]
                # faz dois cliques, pois nas minhas configurações os aplicativos abrem com dois cliques 
                pyautogui.click(x, y)
                pyautogui.click(x, y)
            else:
                if(keyboard.KEY_DOWN and event.name == 'right'):
                    item = item + 1
                elif(keyboard.KEY_DOWN and event.name == 'left'):
                    item = item - 1
                # caso uma tecla inválida for teclada, retonrar exit pois é um erro
                else:
                    exit()
        # para quando o usuário fazer "Control + C" poder sair
        except KeyboardInterrupt:
            exit()