from pygame import *
import sys

import random

clock = time.Clock()
init()
screen = display.set_mode((800, 600))
running = True
tile_size = 16
tam = 30

# --- imagens ---
# fundos 
bb = transform.scale(image.load('INF1034---Trabalho-G3/background/blue-back.png'), (tile_size, tile_size))
bs = transform.scale(image.load('INF1034---Trabalho-G3/background/blue-stars.png'), (tile_size, tile_size))
bw = transform.scale(image.load('INF1034---Trabalho-G3/background/blue-with-stars.png'), (tile_size, tile_size))

# tile de asteroide 
a2 = transform.scale(image.load('INF1034---Trabalho-G3/background/asteroid-2.png'), (tile_size, tile_size))

# planeta pequeno 
ps = image.load('INF1034---Trabalho-G3/background/prop-planet-small.png')

# planeta grande 
pb = image.load('INF1034---Trabalho-G3/background/prop-planet-big.png')

tiles_img = {
    'bb': bb,   # fundo azul escuro
    'bs': bs,   # fundo com estrelas
    'bw': bw,   # fundo azul com estrelas (mais claro)
    'a2': a2,   # asteroide
    'ps': ps,   # planeta pequeno
}

# mapa de fundo (camada 1) - cobre a tela inteira
mapa = [
    'bb,bb,bb,bb,bb,bb,bb,bb,bb,bb,bb,bb,bb,bb,bb,bb,bb,bb,bb,bb,bb,bb,bb,bb,bb,bb,bb,bb,bb,bb,bb,bb,bb,bb,bb,bb,bb,bb,bb,bb,bb,bb,bb,bb,bb,bb,bb,bb,bb,bb',
    'bb,bs,bb,bb,bs,bb,bb,bb,bs,bb,bb,bb,bb,bs,bb,bb,bb,bb,bb,bs,bb,bb,bb,bs,bb,bb,bb,bb,bs,bb,bb,bb,bb,bb,bs,bb,bb,bb,bs,bb,bb,bb,bb,bs,bb,bb,bb,bb,bb,bb',
    'bb,bb,bb,bs,bb,bb,bb,bb,bb,bb,bs,bb,bb,bb,bb,bb,bs,bb,bb,bb,bb,bb,bb,bb,bb,bs,bb,bb,bb,bb,bb,bs,bb,bb,bb,bb,bb,bb,bb,bs,bb,bb,bb,bb,bb,bb,bs,bb,bb,bb',
    'bb,bb,bb,bb,bb,bw,bb,bb,bb,bb,bb,bb,bb,bb,bw,bb,bb,bb,bb,bb,bb,bw,bb,bb,bb,bb,bb,bb,bb,bb,bw,bb,bb,bb,bb,bb,bb,bw,bb,bb,bb,bb,bb,bb,bb,bw,bb,bb,bb,bb',
    'bb,bs,bb,bb,bb,bb,bb,bb,bs,bb,bb,bb,bb,bs,bb,bb,bb,bb,bb,bb,bs,bb,bb,bb,bb,bb,bb,bs,bb,bb,bb,bb,bb,bs,bb,bb,bb,bb,bb,bb,bb,bs,bb,bb,bb,bb,bb,bb,bs,bb',
    'bb,bb,bb,bb,bb,bb,bb,bb,bb,bb,bb,bs,bb,bb,bb,bb,bb,bb,bb,bb,bb,bb,bb,bs,bb,bb,bb,bb,bb,bb,bb,bb,bb,bb,bb,bs,bb,bb,bb,bb,bb,bb,bb,bb,bb,bs,bb,bb,bb,bb',
    'bw,bb,bb,bs,bb,bb,bb,bw,bb,bb,bb,bb,bb,bb,bb,bw,bb,bb,bs,bb,bb,bb,bb,bb,bb,bb,bw,bb,bb,bb,bs,bb,bb,bb,bb,bb,bw,bb,bb,bb,bb,bb,bb,bw,bb,bb,bb,bb,bb,bb',
    'bb,bb,bb,bb,bb,bs,bb,bb,bb,bb,bb,bb,bb,bs,bb,bb,bb,bb,bb,bb,bb,bb,bs,bb,bb,bb,bb,bb,bb,bs,bb,bb,bb,bb,bb,bb,bb,bb,bb,bs,bb,bb,bb,bb,bb,bb,bb,bb,bs,bb',
    'bb,bb,bw,bb,bb,bb,bb,bb,bb,bw,bb,bb,bb,bb,bb,bb,bb,bw,bb,bb,bb,bb,bb,bb,bw,bb,bb,bb,bb,bb,bb,bb,bw,bb,bb,bb,bb,bb,bw,bb,bb,bb,bb,bb,bb,bw,bb,bb,bb,bb',
    'bb,bs,bb,bb,bb,bb,bb,bb,bb,bb,bb,bb,bs,bb,bb,bb,bb,bb,bb,bb,bb,bs,bb,bb,bb,bb,bb,bb,bb,bs,bb,bb,bb,bb,bb,bb,bb,bs,bb,bb,bb,bb,bb,bb,bb,bb,bb,bs,bb,bb',
    'bb,bb,bb,bb,bw,bb,bb,bb,bs,bb,bb,bb,bb,bb,bb,bw,bb,bb,bb,bs,bb,bb,bb,bb,bb,bw,bb,bb,bb,bb,bb,bs,bb,bb,bb,bb,bw,bb,bb,bb,bb,bs,bb,bb,bb,bb,bb,bb,bw,bb',
    'bb,bb,bb,bb,bb,bb,bb,bb,bb,bb,bb,bs,bb,bb,bb,bb,bb,bb,bb,bb,bb,bb,bb,bs,bb,bb,bb,bb,bb,bb,bb,bb,bb,bb,bb,bs,bb,bb,bb,bb,bb,bb,bb,bb,bb,bs,bb,bb,bb,bb',
    'bs,bb,bb,bb,bb,bb,bb,bs,bb,bb,bb,bb,bb,bb,bs,bb,bb,bb,bb,bb,bb,bb,bb,bb,bb,bs,bb,bb,bb,bb,bb,bb,bs,bb,bb,bb,bb,bb,bb,bb,bs,bb,bb,bb,bb,bb,bb,bb,bb,bs',
    'bb,bb,bw,bb,bb,bb,bb,bb,bb,bb,bw,bb,bb,bb,bb,bb,bb,bw,bb,bb,bb,bb,bw,bb,bb,bb,bb,bb,bb,bw,bb,bb,bb,bb,bb,bw,bb,bb,bb,bb,bb,bb,bw,bb,bb,bb,bb,bb,bb,bb',
    'bb,bb,bb,bb,bs,bb,bb,bb,bb,bb,bb,bb,bb,bs,bb,bb,bb,bb,bb,bb,bb,bb,bb,bb,bb,bb,bb,bs,bb,bb,bb,bb,bb,bb,bb,bb,bb,bb,bb,bs,bb,bb,bb,bb,bb,bb,bb,bs,bb,bb',
    'bb,bb,bb,bb,bb,bb,bb,bb,bb,bb,bb,bb,bb,bb,bb,bb,bb,bb,bb,bb,bb,bb,bb,bb,bb,bb,bb,bb,bb,bb,bb,bb,bb,bb,bb,bb,bb,bb,bb,bb,bb,bb,bb,bb,bb,bb,bb,bb,bb,bb',
    'bb,bs,bb,bb,bb,bb,bs,bb,bb,bb,bb,bb,bs,bb,bb,bb,bb,bb,bs,bb,bb,bb,bb,bb,bs,bb,bb,bb,bb,bb,bs,bb,bb,bb,bb,bb,bs,bb,bb,bb,bb,bb,bs,bb,bb,bb,bb,bb,bb,bs',
    'bb,bb,bb,bw,bb,bb,bb,bb,bb,bw,bb,bb,bb,bb,bb,bb,bw,bb,bb,bb,bb,bb,bw,bb,bb,bb,bb,bb,bw,bb,bb,bb,bb,bb,bb,bw,bb,bb,bb,bb,bw,bb,bb,bb,bb,bb,bw,bb,bb,bb',
    'bb,bb,bb,bb,bb,bb,bb,bb,bb,bb,bb,bb,bb,bb,bb,bb,bb,bb,bb,bb,bb,bb,bb,bb,bb,bb,bb,bb,bb,bb,bb,bb,bb,bb,bb,bb,bb,bb,bb,bb,bb,bb,bb,bb,bb,bb,bb,bb,bb,bb',
    'bb,bb,bs,bb,bb,bb,bb,bb,bs,bb,bb,bb,bb,bb,bs,bb,bb,bb,bb,bb,bs,bb,bb,bb,bb,bb,bs,bb,bb,bb,bb,bb,bs,bb,bb,bb,bb,bb,bs,bb,bb,bb,bb,bb,bs,bb,bb,bb,bb,bb',
    'bb,bb,bb,bb,bb,bw,bb,bb,bb,bb,bb,bw,bb,bb,bb,bb,bb,bw,bb,bb,bb,bb,bb,bw,bb,bb,bb,bb,bb,bw,bb,bb,bb,bb,bb,bw,bb,bb,bb,bb,bb,bw,bb,bb,bb,bb,bb,bw,bb,bb',
    'bb,bb,bb,bb,bb,bb,bb,bb,bb,bb,bb,bb,bb,bb,bb,bb,bb,bb,bb,bb,bb,bb,bb,bb,bb,bb,bb,bb,bb,bb,bb,bb,bb,bb,bb,bb,bb,bb,bb,bb,bb,bb,bb,bb,bb,bb,bb,bb,bb,bb',
    'bb,bs,bb,bb,bb,bb,bb,bb,bs,bb,bb,bb,bb,bs,bb,bb,bb,bb,bb,bb,bs,bb,bb,bb,bb,bb,bb,bs,bb,bb,bb,bb,bb,bs,bb,bb,bb,bb,bb,bb,bb,bs,bb,bb,bb,bb,bb,bb,bs,bb',
    'bb,bb,bb,bw,bb,bb,bb,bb,bb,bb,bw,bb,bb,bb,bb,bb,bw,bb,bb,bb,bb,bb,bb,bb,bw,bb,bb,bb,bb,bb,bw,bb,bb,bb,bb,bb,bb,bw,bb,bb,bb,bb,bb,bb,bw,bb,bb,bb,bb,bb',
    'bb,bb,bb,bb,bb,bb,bb,bs,bb,bb,bb,bb,bb,bb,bb,bb,bb,bb,bs,bb,bb,bb,bb,bb,bb,bb,bb,bb,bb,bs,bb,bb,bb,bb,bb,bb,bb,bb,bb,bb,bs,bb,bb,bb,bb,bb,bb,bb,bb,bb',
    'bb,bb,bb,bb,bb,bb,bb,bb,bb,bb,bb,bb,bb,bb,bb,bb,bb,bb,bb,bb,bb,bb,bb,bb,bb,bb,bb,bb,bb,bb,bb,bb,bb,bb,bb,bb,bb,bb,bb,bb,bb,bb,bb,bb,bb,bb,bb,bb,bb,bb',
    'bb,bs,bb,bb,bb,bs,bb,bb,bb,bb,bb,bs,bb,bb,bb,bb,bb,bb,bb,bs,bb,bb,bb,bb,bs,bb,bb,bb,bb,bb,bb,bs,bb,bb,bb,bb,bs,bb,bb,bb,bb,bb,bs,bb,bb,bb,bb,bb,bb,bs',
    'bb,bb,bb,bb,bw,bb,bb,bb,bb,bw,bb,bb,bb,bb,bb,bw,bb,bb,bb,bb,bb,bb,bw,bb,bb,bb,bb,bb,bw,bb,bb,bb,bb,bb,bw,bb,bb,bb,bb,bb,bw,bb,bb,bb,bb,bb,bb,bw,bb,bb',
    'bb,bb,bb,bb,bb,bb,bb,bb,bb,bb,bb,bb,bb,bb,bb,bb,bb,bb,bb,bb,bb,bb,bb,bb,bb,bb,bb,bb,bb,bb,bb,bb,bb,bb,bb,bb,bb,bb,bb,bb,bb,bb,bb,bb,bb,bb,bb,bb,bb,bb',
    'bs,bb,bb,bb,bb,bb,bb,bs,bb,bb,bb,bb,bb,bs,bb,bb,bb,bb,bb,bb,bb,bb,bs,bb,bb,bb,bb,bb,bb,bb,bs,bb,bb,bb,bb,bb,bb,bb,bs,bb,bb,bb,bb,bb,bb,bb,bs,bb,bb,bb',
    'bb,bb,bb,bw,bb,bb,bb,bb,bb,bb,bw,bb,bb,bb,bb,bw,bb,bb,bb,bb,bb,bw,bb,bb,bb,bb,bb,bb,bb,bw,bb,bb,bb,bb,bw,bb,bb,bb,bb,bb,bw,bb,bb,bb,bb,bb,bb,bb,bw,bb',
    'bb,bb,bb,bb,bb,bb,bb,bb,bb,bb,bb,bb,bb,bb,bb,bb,bb,bb,bb,bb,bb,bb,bb,bb,bb,bb,bb,bb,bb,bb,bb,bb,bb,bb,bb,bb,bb,bb,bb,bb,bb,bb,bb,bb,bb,bb,bb,bb,bb,bb',
    'bb,bs,bb,bb,bb,bb,bb,bb,bs,bb,bb,bb,bb,bb,bb,bs,bb,bb,bb,bb,bb,bb,bb,bs,bb,bb,bb,bb,bb,bb,bb,bs,bb,bb,bb,bb,bb,bb,bb,bs,bb,bb,bb,bb,bb,bb,bb,bs,bb,bb',
    'bb,bb,bb,bb,bb,bw,bb,bb,bb,bb,bb,bw,bb,bb,bb,bb,bb,bb,bw,bb,bb,bb,bb,bb,bw,bb,bb,bb,bb,bb,bw,bb,bb,bb,bb,bb,bw,bb,bb,bb,bb,bb,bw,bb,bb,bb,bb,bb,bw,bb',
    'bb,bb,bb,bb,bb,bb,bb,bb,bb,bb,bb,bb,bb,bb,bb,bb,bb,bb,bb,bb,bb,bb,bb,bb,bb,bb,bb,bb,bb,bb,bb,bb,bb,bb,bb,bb,bb,bb,bb,bb,bb,bb,bb,bb,bb,bb,bb,bb,bb,bb',
    'bs,bb,bb,bb,bb,bb,bs,bb,bb,bb,bb,bb,bb,bs,bb,bb,bb,bb,bb,bs,bb,bb,bb,bb,bb,bb,bs,bb,bb,bb,bb,bb,bs,bb,bb,bb,bb,bb,bb,bs,bb,bb,bb,bb,bb,bs,bb,bb,bb,bb',
    'bb,bb,bb,bw,bb,bb,bb,bb,bb,bw,bb,bb,bb,bb,bb,bw,bb,bb,bb,bb,bb,bw,bb,bb,bb,bb,bb,bb,bw,bb,bb,bb,bb,bw,bb,bb,bb,bb,bb,bw,bb,bb,bb,bb,bb,bw,bb,bb,bb,bb',
]

# mapa de props (camada 2) — asteroides e planetas pequenos por cima do fundo
mapa2 = [
    ' , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , ',
    ' , , , , , , , , , , , , , , , , , , , , , , , , , , , , ,a2, , , , , , , , , , , , , , , , , , , , ',
    ' , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , ',
    ' , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , ',
    ' , , , , , , , , , , , , , , , , , , , , , ,a2, , , , , , , , , , , , , , , , , , , , , , , , , , , ',
    ' , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , ',
    ' , , , , ,a2, , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , ',
    ' , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , ,a2, , , , , , , , , , , , , , , , , ',
    ' , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , ',
    ' , , , , , , , , , , ,ps, , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , ,ps, , , , ',
    ' , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , ',
    ' , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , ,a2, , , , , , , , , , , , , , , , , ',
    ' , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , ',
    ' ,a2, , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , ,a2, , , , , , , , , ',
    ' , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , ',
    ' , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , ',
    ' , , , , , , , , , , , , , , , , , , , , , , , , , , ,a2, , , , , , , , , , , , , , , , , , , , , , ',
    ' , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , ,ps, , ',
    ' , , , , , , , , , , , , , , ,ps, , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , ',
    ' , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , ',
    ' , , , ,a2, , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , ,a2, , , , , , , , , ',
    ' , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , ',
    ' , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , ',
    ' , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , ',
    ' , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , ,a2, , , , , , , , , , , , , , ',
    ' , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , ',
    ' ,ps, , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , ,a2, , , , , ',
    ' , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , ',
    ' , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , ',
    ' , , , , , , , , , , , , , , , , , ,a2, , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , ',
    ' , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , ',
    ' , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , ',
    ' , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , ',
    ' , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , ,ps, , , , , , , , , , , , , , , , , , ',
    ' , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , ',
    ' , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , ',
    ' , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , ',
]

# posicionar o mapa no meio da tela
colunas = len(mapa[0].split(','))
linhas = len(mapa)
offset_x = (800 - colunas * tile_size) // 2
offset_y = (600 - linhas * tile_size) // 2

# posições dos planetas grandes (desenhados direto, não são tiles)
planetas_grandes = [
    (120, 80),
    (600, 320),
    (350, 500),
]

# fonte do texto
fonte = font.Font('INF1034---Trabalho-G3/texto.ttf', 10)

# imagem de coraçao do lado da vida
vida = image.load('INF1034---Trabalho-G3/vida.png')
life = 3

current_frame_R = 0
anim_time_R = 0
ship_animation_R = []
for i in range(6):
    imagem_ship_R = image.load(f'INF1034---Trabalho-G3/Right/ship{i}.png')
    imagem_ship_R = transform.scale(imagem_ship_R, (106, 54))
    ship_animation_R.append(imagem_ship_R)
direita = True

current_frame_L = 0
anim_time_L = 0
ship_animation_L = []
for i in range(6):
    imagem_ship_L = image.load(f'INF1034---Trabalho-G3/Left/ship{i}.png')
    imagem_ship_L = transform.scale(imagem_ship_L, (106, 54))
    ship_animation_L.append(imagem_ship_L)
esquerda = False



#classe de npc
ship_normal = []
ship_vermelho = []

for i in range(4):
    ship_normal.append(transform.scale(image.load(f"INF1034---Trabalho-G3/red_ship1/ship0{i+5}.png"), (40, 40)))
    ship_vermelho.append(transform.scale(image.load(f"INF1034---Trabalho-G3/red_ship2/ship0{i+5}.png"), (40, 40)))

opcoes_de_cores = [ship_normal, ship_vermelho]

class naveNPC:
    def __init__(self, limite_x, chao_y, opcoes_de_cores):
        #posição inicial na tela
        self.x = random.randint(700, 790)
        self.y = random.randint(50, 550)
        # comeca andando para a esquerda (-2) ou direita (2)
        self.velocidade_x = random.choice([-3,-2, 2, 3])
        self.velocidade_y = random.choice([-3, -2, 2, 3])
        
        self.frame_atual = random.randint(0, 10) #cada dinossauro começa em frames diferentes xd
        self.tempo_animacao = 0

        self.minha_animacao = random.choice(opcoes_de_cores)

        self.ship_hitbox = Rect(self.x, self.y, tam+10, tam+10)

    def atualizar_e_desenhar(self, tela, dt, lista_animacao):
        #movimento
        self.x = self.x + self.velocidade_x
        self.y = self.y + self.velocidade_y

        self.ship_hitbox.x = self.x
        self.ship_hitbox.y = self.y

        #bater na parede e virar
        if self.x <= -20 or self.x >= 790:
            self.velocidade_x = self.velocidade_x * -1
        if self.y <= -20 or self.y >= 570:
            self.velocidade_y = self.velocidade_y * -1

        #tempo da Animação
        self.tempo_animacao += dt
        if self.tempo_animacao > 80: # 80 milissegundos para trocar de frame
            self.frame_atual += 1
            if self.frame_atual >= len(lista_animacao):
                self.frame_atual = 0
            self.tempo_animacao = 0

        #desenho
        imagem_atual = lista_animacao[self.frame_atual]
        
        # se velocidade for negativa (esquerda), espelha a imagem
        if self.velocidade_x < 0:
            imagem_atual = transform.flip(imagem_atual, True, False)
            
        tela.blit(imagem_atual, (self.x, self.y))
        draw.rect(tela, (255, 0, 0), self.ship_hitbox, 2)

bando_de_naves = []
#range = quantas naves tem

for i in range(10): # Pode colocar 10, 20...
    # Passamos as opções de cores para ele sortear quando nascer
    nova_nave = naveNPC(800, 0, opcoes_de_cores)
    bando_de_naves.append(nova_nave)


while running:
    for ev in event.get():
        if ev.type == QUIT:
            quit()
            sys.exit()
    
    clock.tick(60)
    dt = clock.get_time()
    keys = key.get_pressed()

    if keys[K_a]:
        esquerda = True
        direita = False
    elif keys[K_d]:
        direita = True
        esquerda = False

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

    screen.fill((10,10,30))

    # camada 1 — fundo de espaço
    for i in range(len(mapa)):
        tiles = mapa[i].split(',')
        for j in range(len(tiles)):
            tile = tiles[j]
            if tile in tiles_img:
                screen.blit(tiles_img[tile], (offset_x + j * tile_size, offset_y + i * tile_size))

    # planetas grandes como props (igual às árvores no jogo 1)
    for px, py in planetas_grandes:
        screen.blit(pb, (px, py))

    # camada 2 — asteroides e planetas pequenos
    for i in range(len(mapa2)):
        tiles = mapa2[i].split(',')
        for j in range(len(tiles)):
            tile = tiles[j].strip()
            if tile in tiles_img:
                screen.blit(tiles_img[tile], (offset_x + j * tile_size, offset_y + i * tile_size))

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

    for nave in bando_de_naves:
        nave.atualizar_e_desenhar(screen, dt, nave.minha_animacao)
    if direita:
        screen.blit(ship_animation_R[current_frame_R], (100,200), (0,0,106,54))
    elif esquerda:
        screen.blit(ship_animation_L[current_frame_L], (300,200), (0,0,106,54))

    display.update()
