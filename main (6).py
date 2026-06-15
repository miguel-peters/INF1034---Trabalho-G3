import pygame
import sys
from pygame.locals import QUIT

pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption('Mapa Espacial')
clock = pygame.time.Clock()
tile_size = 16

# --- imagens ---
# fundos (272x160) escalados para 16x16 como tiles de fundo
bb = pygame.transform.scale(pygame.image.load('background/blue-back.png'), (tile_size, tile_size))
bs = pygame.transform.scale(pygame.image.load('background/blue-stars.png'), (tile_size, tile_size))
bw = pygame.transform.scale(pygame.image.load('background/blue-with-stars.png'), (tile_size, tile_size))

# tile de asteroide (21x17 -> 16x16)
a2 = pygame.transform.scale(pygame.image.load('background/asteroid-2.png'), (tile_size, tile_size))

# planeta pequeno (16x16, tamanho exato)
ps = pygame.image.load('background/prop-planet-small.png')

# planeta grande (43x43) — desenhado por cima como prop
pb = pygame.image.load('background/prop-planet-big.png')

tiles_img = {
    'bb': bb,   # fundo azul escuro
    'bs': bs,   # fundo com estrelas
    'bw': bw,   # fundo azul com estrelas (mais claro)
    'a2': a2,   # asteroide
    'ps': ps,   # planeta pequeno
}

# mapa de fundo (camada 1) — cobre a tela inteira (50x37 tiles de 16px = 800x592)
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

while True:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    clock.tick(60)
    dt = clock.get_time()
    screen.fill((10, 10, 30))

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

    pygame.display.update()