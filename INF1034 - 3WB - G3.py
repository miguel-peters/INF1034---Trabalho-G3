from pygame import *
import sys

clock = time.Clock()
init()
screen = display.set_mode((1200,800))
running = True

vida = image.load('INF1034---Trabalho-G3/Vida.png')

current_frame_R = 0
anim_time_R = 0
ship_animation_R = []
for i in range(6):
    imagem_ship_R = image.load(f'INF1034---Trabalho-G3/Right/ship{i}.png')
    imagem_ship_R = transform.scale(imagem_ship_R, (106, 54))
    ship_animation_R.append(imagem_ship_R)

current_frame_L = 0
anim_time_L = 0
ship_animation_L = []
for i in range(6):
    imagem_ship_L = image.load(f'INF1034---Trabalho-G3/Left/ship{i}.png')
    imagem_ship_L = transform.scale(imagem_ship_L, (106, 54))
    ship_animation_L.append(imagem_ship_L)

while running:
    for ev in event.get():
        if ev.type == QUIT:
            quit()
            sys.exit()
    
    clock.tick(60)
    dt = clock.get_time()

    anim_time_R += dt
    anim_time_sec_R = anim_time_R/1000

    if anim_time_sec_R > 0.5:
        current_frame_R += 1
        if current_frame_R > 5:
            current_frame_R = 0
        anim_time_sec_R = 0

    anim_time_L += dt
    anim_time_sec_L = anim_time_L/1000

    if anim_time_sec_L > 0.5:
        current_frame_L += 1
        if current_frame_L > 5:
            current_frame_L = 0
        anim_time_sec_L = 0


    screen.fill((255,255,255))

    screen.blit(ship_animation_R[current_frame_R], (100,200), (0,0,106,54))
    screen.blit(ship_animation_L[current_frame_L], (300,200), (0,0,106,54))

    #Vidas
    vida = transform.scale(vida, (200,100))
    screen.blit(vida, ((900,20)))
    display.update()
