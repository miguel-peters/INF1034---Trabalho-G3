from pygame import *
import sys

init()
screen = display.set_mode((800, 600))
display.set_caption("Space Wars - INF1034 (G3)")
clock = time.Clock()

# Cores
PRETO        = (0,   0,   0)
BRANCO       = (255, 255, 255)
AMARELO_GTA  = (255, 200, 0)
VERMELHO     = (200, 20,  20)
VERDE        = (20,  200, 50)

# Fontes 
try:
    fonte_gta_titulo = font.Font('GTA.otf', 90)
    fonte_gta_med    = font.Font('GTA.otf', 65)
    fonte_menu       = font.Font('texto.ttf', 28)
    fonte_padrao     = font.Font('texto.ttf', 20)
except:
    fonte_gta_titulo = font.SysFont('impact', 90)
    fonte_gta_med    = font.SysFont('impact', 65)
    fonte_menu       = font.SysFont('arial', 28)
    fonte_padrao     = font.SysFont('arial', 20)

estado = 'inicio'
opcao_selecionada = 0
opcoes = ['JOGAR', 'SAIR']

# Funções
def desenha_texto_sombra(texto, fonte, cor, x, y):
    sombra = fonte.render(texto, True, PRETO)
    real = fonte.render(texto, True, cor)
    screen.blit(sombra, (x + 3, y + 3))
    screen.blit(real, (x, y))

def centraliza_x(texto, fonte):
    largura = fonte.size(texto)[0]
    return (800 - largura) // 2

# LOOP 
while True:
    clock.tick(60)
    
    for ev in event.get():
        if ev.type == QUIT:
            quit(); sys.exit()
        
        if ev.type == KEYDOWN:
            if estado == 'inicio':
                if ev.key == K_DOWN: opcao_selecionada = (opcao_selecionada + 1) % len(opcoes)
                if ev.key == K_UP:   opcao_selecionada = (opcao_selecionada - 1) % len(opcoes)
                if ev.key == K_RETURN:
                    if opcao_selecionada == 0: estado = 'jogando'
                    else: quit(); sys.exit()
            
            

    screen.fill(PRETO)

    if estado == 'inicio':
        desenha_texto_sombra('SPACE', fonte_gta_titulo, AMARELO_GTA, centraliza_x('SPACE', fonte_gta_titulo), 100)
        desenha_texto_sombra('WARS', fonte_gta_titulo, BRANCO, centraliza_x('WARS', fonte_gta_titulo), 200)
        
        for i, opt in enumerate(opcoes):
            y = 400 + (i * 50)
            cor = AMARELO_GTA if i == opcao_selecionada else BRANCO
            desenha_texto_sombra(opt, fonte_menu, cor, centraliza_x(opt, fonte_menu), y)

    


    display.update()