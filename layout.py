from pygame import *
import sys
import random

init()

screen = display.set_mode((800, 600))
display.set_caption('Hello world')
clock = time.Clock()
vel_tiro = 3
# fonte do texto
fonte = font.Font('texto.ttf', 15)
blur = True

# imagem de coraçao do lado da vida
vida = image.load('vida.png')
life = 3

botao_rec = Rect(300,300,150,50)

blur_surface = Surface((1000, 600))
blur_surface.set_alpha(150) # Valor de opacidade (0 = invisível, 255 = totalmente opaco)
blur_surface.fill((0, 0, 0)) # Cor do desfoque (preto)

fonteDerrota = font.Font('GTA.otf', 100)

def tiros():
    lista_inimigo = []
    for i in range(4):
        x_inicial = 900
        y_inicial = random.randint(50,550)
        lista_inimigo.append([x_inicial, y_inicial])
    return lista_inimigo

lista = tiros()

current_frame_I = 0
anim_time_I = 0
inimigo_imagem = []
pos_xI = 600
pos_yI = 200
for i in range(6):
    inimigo = image.load(f'inimigo_medio/Left/inimigo{i}.png')
    inimigo = transform.scale(inimigo, (79.5, 40.5))
    inimigo_imagem.append(inimigo)

current_frame_S = 0
anim_time_S = 0
shot_imagem = []
# pos_xS = x_inicial - 10
# pos_yS = y_inicial + 15
for i in range(5):
    shot = image.load(f'inimigo_medio/Shooting/Shot{i}.png')
    shot = transform.scale(shot, (45,15))
    shot_imagem.append(shot)


while True:
    for evento in event.get():
        if evento.type == QUIT:
            quit()
            sys.exit()
        if evento.type == MOUSEBUTTONDOWN:
            if evento.button == 1:
                pos_clique = mouse.get_pos()
            if botao_rec.collidepoint(pos_clique):
                blur = False

    clock.tick(60)
    dt = clock.get_time()

    screen.fill((142, 45, 200))

    # for pos in lista:
    #     pos_xN = 900
    #     screen.blit(inimigo_imagem[current_frame_I], (pos_xN,pos[1]), (0,0,79.5,40.5))
    #     pos[0] = pos[0] - 0.3 * dt
    #     #pos[1] = pos[1] + 15
    #     screen.blit(shot_imagem[current_frame_S], (pos[0], pos[1]+15), (0,0,45,15))
    #     if pos[0] < -100:
    #         pos_xN = pos_xN + 0.2 * dt
    #         lista = tiros()
    


    # #pos_xS += -3
    # anim_time_I += dt
    # anim_time_sec_I = anim_time_I/1000

    # if anim_time_sec_I > 0.5:
    #     current_frame_I += 1
    #     if current_frame_I > 5:
    #         current_frame_I = 0
    #     anim_time_sec_I = 0

    # anim_time_S += dt
    # anim_time_sec_S = anim_time_S/1000

    # if anim_time_sec_S > 0.1:
    #     current_frame_S += 1
    #     #pos_xS -= 200
    #     if current_frame_S > 4:
    #         current_frame_S = 0
    #         #pos_xS = x_inicial + 10
    #     anim_time_S = 0

    
    


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

    
    textoDerrota = fonteDerrota.render('WASTED', True, (255,255,255))
    
    if blur == True:
        screen.blit(blur_surface, (0, 0))
    screen.blit(textoDerrota, (350,100))



    draw.rect(screen, (255,255,255), (300,300,150,50), border_radius = 20)

    texto6 = fonte.render('Jogar de novo', True, (0,0,0))
    screen.blit(texto6, (310,310))



    display.flip()
    display.update()
