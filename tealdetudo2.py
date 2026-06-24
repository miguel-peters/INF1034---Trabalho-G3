from pygame import *
import sys

init()
screen = display.set_mode((800, 600))
display.set_caption("Space Wars - INF1034 (G3)")
clock = time.Clock()

# --- CORES E FONTES ---
PRETO, BRANCO = (0, 0, 0), (255, 255, 255)
AMARELO_GTA = (255, 200, 0)

try:
    f_gta_tit = font.Font('GTA.otf', 90)
    f_menu    = font.Font('texto.ttf', 28)
    f_input   = font.Font('texto.ttf', 20)
except:
    f_gta_tit = font.SysFont('impact', 90)
    f_menu    = font.SysFont('arial', 28)
    f_input   = font.SysFont('arial', 20)

# --- VARIÁVEIS DE ESTADO ---
estado = 'login' # login, inicio, jogando
texto_nome = ''
campo_ativo = False
caixa_nome = Rect(300, 300, 200, 40)
opcao_selecionada = 0
opcoes = ['JOGAR', 'SAIR']

def centraliza_x(texto, fonte):
    return (800 - fonte.size(texto)[0]) // 2

def desenha_texto_sombra(texto, fonte, cor, x, y):
    sombra = fonte.render(texto, True, PRETO)
    real = fonte.render(texto, True, cor)
    screen.blit(sombra, (x + 3, y + 3))
    screen.blit(real, (x, y))

# --- LOOP PRINCIPAL ---
while True:
    clock.tick(60)
    
    for ev in event.get():
        if ev.type == QUIT:
            quit(); sys.exit()
        
        # Lógica do Login
        if estado == 'login':
            if ev.type == MOUSEBUTTONDOWN:
                campo_ativo = caixa_nome.collidepoint(ev.pos)
            if ev.type == KEYDOWN and campo_ativo:
                if ev.key == K_RETURN:
                    if 0 < len(texto_nome) <= 6: estado = 'inicio'
                elif ev.key == K_BACKSPACE:
                    texto_nome = texto_nome[:-1]
                else:
                    if len(texto_nome) < 6: texto_nome += ev.unicode
        
        # Lógica do Menu
        elif estado == 'inicio':
            if ev.type == KEYDOWN:
                if ev.key == K_DOWN: opcao_selecionada = (opcao_selecionada + 1) % len(opcoes)
                if ev.key == K_UP:   opcao_selecionada = (opcao_selecionada - 1) % len(opcoes)
                if ev.key == K_RETURN:
                    if opcao_selecionada == 0: estado = 'jogando'
                    else: quit(); sys.exit()

    # --- DESENHO ---
    screen.fill(PRETO)

    if estado == 'login':
        desenha_texto_sombra('NOME DO JOGADOR', f_menu, BRANCO, centraliza_x('NOME DO JOGADOR', f_menu), 250)
        draw.rect(screen, BRANCO, caixa_nome, 2)
        txt_surf = f_input.render(texto_nome, True, BRANCO)
        screen.blit(txt_surf, (caixa_nome.x + 10, caixa_nome.y + 10))

    elif estado == 'inicio':
        desenha_texto_sombra('SPACE', f_gta_tit, AMARELO_GTA, centraliza_x('SPACE', f_gta_tit), 100)
        desenha_texto_sombra('WARS', f_gta_tit, BRANCO, centraliza_x('WARS', f_gta_tit), 200)
        for i in range(len(opcoes)):
            cor = AMARELO_GTA if i == opcao_selecionada else BRANCO
            desenha_texto_sombra(opcoes[i], f_menu, cor, centraliza_x(opcoes[i], f_menu), 400 + (i * 50))   