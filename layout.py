from pygame import *
import sys


init()

screen = display.set_mode((1000, 600))
display.set_caption('Hello world')
clock = time.Clock()

# fonte do texto
fonte = font.Font('INF1034---Trabalho-G3/texto.ttf', 10)

# imagem de coraçao do lado da vida
vida = image.load('INF1034---Trabalho-G3/vida.png')
life = 3

while True:
    for evento in event.get():
        if evento.type == QUIT:
            quit()
            sys.exit()

    clock.tick(60)
    dt = clock.get_time()

    screen.fill((0, 0, 0))

    draw.rect(screen, (102, 51, 0), (20, 20, 200, 70), border_radius=20)

    vida = transform.scale(vida, (100, 50))

    if life == 3:
        vida_cheia = screen.blit(vida, (15, 32), (0, 0, 35, 50))
        draw.rect(screen, (0, 0, 0), (54, 45, 150, 20), border_radius=20)
        draw.rect(screen, (204, 0, 0), (54, 45, 150, 20), border_radius=20)

    elif life == 2:
        vida_metade = screen.blit(vida, (20, 32), (33, 0, 30, 50))
        draw.rect(screen, (0, 0, 0), (54, 45, 150, 20), border_radius=20)
        draw.rect(screen, (204, 0, 0), (54, 45, 100, 20), border_radius=20)

    elif life == 1:
        vida_metade = screen.blit(vida, (20, 32), (33, 0, 30, 50))
        draw.rect(screen, (0, 0, 0), (54, 45, 150, 20), border_radius=20)
        draw.rect(screen, (204, 0, 0), (54, 45, 50, 20), border_radius=20)

    elif life == 0:
        vida_vazia = screen.blit(vida, (21, 32), (60, 0, 30, 50))
        draw.rect(screen, (0, 0, 0), (54, 45, 150, 20), border_radius=20)

    # colocar os textos
    texto1 = fonte.render('A - esquerda', True, (255, 255, 255))
    texto2 = fonte.render('D - direita', True, (255, 255, 255))
    texto3 = fonte.render('w - cima', True, (255, 255, 255))
    texto4 = fonte.render('S - baixo', True, (255, 255, 255))
    # botei o espaco para dash mas n sei qual vms usar, ent da pra trocar
    texto5 = fonte.render('SPACE - dash', True, (255, 255, 255))

    screen.blit(texto1, (25, 420))
    screen.blit(texto2, (25, 440))
    screen.blit(texto3, (25, 460))
    screen.blit(texto4, (25, 480))
    screen.blit(texto5, (25, 500))

    display.update()
