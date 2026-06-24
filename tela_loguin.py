from pygame import *
import sys

init()
screen = display.set_mode((1000, 600))
clock = time.Clock()

fonte = font.Font('texto.ttf', 15)
fundo = image.load('background/blue-back.png')
fundo = transform.scale(fundo, (1000, 600))


tela_atual = 'loguin'
texto_nome = ''
campo_ativo = False
caixa_nome = Rect(387, 280, 200, 35)


def tela_inicio():
    screen.blit(fundo, (0, 0))
    titulo = fonte.render('Insira  seu  nome', True, (255, 255, 255))
    screen.blit(titulo, (420, 200))
    draw.rect(screen, (255, 255, 255), caixa_nome, 2)

    # para escrever seu nome dentro da caixa
    nome = fonte.render(texto_nome, True, (255, 255, 255))
    screen.blit(nome, (caixa_nome.x + 68, caixa_nome.y + 8))


while True:
    for evento in event.get():
        if evento.type == QUIT:
            quit()
            sys.exit()
        if tela_atual == 'loguin':
            if evento.type == MOUSEBUTTONDOWN:
                campo_ativo = caixa_nome.collidepoint(evento.pos)

            if evento.type == KEYDOWN and campo_ativo:
                if evento.key == K_RETURN:
                    if 0 < len(texto_nome) <= 6:
                        tela_atual = 'jogo'
                elif evento.key == K_BACKSPACE:
                    texto_nome = texto_nome[:-1]
                else:
                    if len(texto_nome) < 6:
                        texto_nome += evento.unicode
    clock.tick(60)
    dt = clock.get_time()

    if tela_atual == 'loguin':
        tela_inicio()
    elif tela_atual == 'jogo':
        screen.fill((0, 0, 0))

    display.update()
