from pygame import *
import sys

import random

clock = time.Clock()
init()
screen = display.set_mode((800, 600))
running = True
tempo_inicial = time.get_ticks()
tile_size = 16
tam = 30
modo = 'Fácil'
vel_ast = 2
modo_invencivel = True
tempo_invencivel = 2000
derrota = False

time_sixseven = random.randint(20, 80)
jumpscare_tocado = False
sixseven_gigante = transform.scale(image.load('67.jpg'), (1000, 700))
# -----RESET DO JOGO-----

estado = {
    'life': 3,
    'derrota': False,
    'tempo_decorrido': 0,
    'tempo_inicial': time.get_ticks(),
    'pos_x': 100,
    'pos_y': 200,
    'direita': True,
    'esquerda': False,
    'modo_invencivel': True,
    'tempo_invencivel': 2000,
    'explosoes_ativas': [],
    'lista_asteroides': [],
    'bando_de_naves': [],
    'lista': [],
    'jumpscare_tocado': False
}

def resetar_jogo(estado):
    estado['life'] = 3
    estado['derrota'] = False
    estado['tempo_decorrido'] = 0
    estado['tempo_inicial'] = time.get_ticks()
    estado['pos_x'] = 100
    estado['pos_y'] = 200
    estado['direita'] = True
    estado['esquerda'] = False
    estado['modo_invencivel'] = True
    estado['tempo_invencivel'] = 2000
    estado['explosoes_ativas'] = []
    estado['jumpscare_tocado'] = False
    jumpscare_tocado = False

    novos_asteroides = []
    for i in range(8):
        x_inicial = random.randint(900, 1200)
        y_inicial = random.randint(0, 550)
        novos_asteroides.append([x_inicial, y_inicial])
    estado['lista_asteroides'] = novos_asteroides

    # recria as naves inimigas
    novas_naves = []
    for i in range(10):
        novas_naves.append(naveNPC(800, 0, opcoes_de_cores))
    estado['bando_de_naves'] = novas_naves

    # recria os tiros inimigos
    estado['lista'] = tiros()
# ---TELA DE LOGIN---

# tela de início

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

# estado = 'inicio'
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

#tela de login
fonte = font.Font('texto.ttf', 15)
fundo = image.load('background/blue-back.png')
fundo = transform.scale(fundo, (800, 600))
tela_atual = 'inicio'
texto_nome = ''
campo_ativo = False
caixa_nome = Rect(300, 280, 200, 35)
fonte_login = font.Font('texto.ttf', 15)
fundo_login = transform.scale(image.load('background/blue-back.png'), (800, 600))
nome = ''


def tela_inicio():
    screen.blit(fundo, (0, 0))
    titulo = fonte.render('Insira  seu  nome', True, (255, 255, 255))
    screen.blit(titulo, (335, 200))
    draw.rect(screen, (255, 255, 255), caixa_nome, 2)

    # para escrever seu nome dentro da caixa
    nome = fonte.render(texto_nome, True, (255, 255, 255))
    screen.blit(nome, (caixa_nome.x + 68, caixa_nome.y + 8))



# ---PROCESSO DE RANKING no TXT---


top5 = []
try:
    with open("ranking.txt", "r") as arquivo:
        linhas = arquivo.readlines()
        for linha in linhas:
            partes = linha.strip().split(',')
            if len(partes) == 2:
                top5.append((partes[0], int(partes[1]))) 
except FileNotFoundError:
    pass

top5.sort(key=lambda x: x[1], reverse=True)

while len(top5) < 5:
    top5.append(("---", 0))
top5 = top5[:5]

# ---SONS---
mixer.music.load("drake.mp3")
mixer.music.play(-1)

som_dano = mixer.Sound('mario-power-down.mp3')
som_morte = mixer.Sound('roblox-explosion-sound.mp3')
som_imortal = mixer.Sound('imortal.mp3')
som_repair = mixer.Sound('repair.mp3')
scream = mixer.Sound('scream2.mp3')

#explosao
animacao_explosao = []
for i in range(8):
    img_exp = image.load(f'kaboom/explosion{i+1}.png')
    img_exp = transform.scale(img_exp, (100, 100))
    animacao_explosao.append(img_exp)

explosoes_ativas = []

# ---IMAGENS---
sixseven = image.load('67.png')
vida_realista = imagem_item_vida = transform.scale(image.load('heart.png'), (30, 30))

itens_vida_ativos = []
timer_spawn_vida = 0

# fundo
imagem_ceu = transform.scale(image.load("background/blue-with-stars.png"), (800, 600))

# tile de asteroide 
a2 = transform.scale(image.load('background/asteroid-2.png'), (tile_size, tile_size))

# planeta pequeno 
ps = image.load('background/prop-planet-small.png')

# planeta grande 
pb = image.load('background/prop-planet-big.png')

#coisa voando
asteroide = transform.scale(image.load('background/asteroid-2.png'), (50, 50))

#asteroides grandoes aleatorios
lista_asteroides = []
for i in range(8):
    x_inicial = random.randint(900, 1200)
    y_inicial = random.randint(0, 550)
    lista_asteroides.append([x_inicial, y_inicial])

tiles_img = {
    'a2': a2,   # asteroide
    'ps': ps,   # planeta pequeno
}

# mapa dos asteroides e planetas pequenos por cima do fundo
mapa = [
    ' , , , , , , , , a2 , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , ',
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

# ---LAYOUT DO JOGO-----

# fonte do texto
fonteLAY = font.Font('texto.ttf', 10)

# imagem de coraçao do lado da vida
vida = image.load('vida.png')
life = 3

# tela de derrota
blur_surface = Surface((1000, 600))
blur_surface.set_alpha(150) # Valor de opacidade (0 = invisível, 255 = totalmente opaco)
blur_surface.fill((0, 0, 0)) # Cor do desfoque (preto)
fonteJ = font.Font('texto.ttf', 15)
botao_rec = Rect(300,300,150,50)


fonteDerrota = font.Font('GTA.otf', 75)

# -----ANIMAÇÃO DO JOGO-----

#nave principal

current_frame_R = 0
anim_time_R = 0
pos_x = 100
pos_y = 200
ship_animation_R = []
for i in range(6):
    imagem_ship_R = image.load(f'Right/ship{i}.png')
    imagem_ship_R = transform.scale(imagem_ship_R, (79.5, 40.5))
    ship_animation_R.append(imagem_ship_R)
direita = True

current_frame_L = 0
anim_time_L = 0
ship_animation_L = []
for i in range(6):
    imagem_ship_L = image.load(f'Left/ship{i}.png')
    imagem_ship_L = transform.scale(imagem_ship_L, (79.5, 40.5))
    ship_animation_L.append(imagem_ship_L)
esquerda = False

#naves inimigas

ship_normal = []
ship_vermelho = []

for i in range(4):
    ship_normal.append(transform.scale(image.load(f"red_ship1/ship0{i+5}.png"), (40, 40)))
    ship_vermelho.append(transform.scale(image.load(f"red_ship2/ship0{i+5}.png"), (40, 40)))

opcoes_de_cores = [ship_normal, ship_vermelho]

class naveNPC:
    def __init__(self, limite_x, chao_y, opcoes_de_cores):
        #posição inicial na tela
        self.x = random.randint(700, 780)
        self.y = random.randint(50, 550)
        # comeca andando para a esquerda (-2) ou direita (2)
        
        self.velocidade_x = random.choice([-3,-2, 2, 3])
        self.velocidade_y = random.choice([-3, -2, 2, 3])


        self.minha_animacao = random.choice(opcoes_de_cores)
        self.frame_atual = random.randint(0,  len(self.minha_animacao) - 1) #cada dinossauro começa em frames diferentes xd
        self.tempo_animacao = 0

        

        self.ship_hitbox = Rect(self.x, self.y, tam+10, tam+10)

    def atualizar_e_desenhar(self, tela, dt, lista_animacao, mult_vel):
        #movimento
        self.x = self.x + (self.velocidade_x * mult_vel)
        self.y = self.y + (self.velocidade_y * mult_vel)

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

bando_de_naves = []

for i in range(10): # Pode colocar 10, 20...
    # Passamos as opções de cores para ele sortear quando nascer
    nova_nave = naveNPC(800, 0, opcoes_de_cores)
    bando_de_naves.append(nova_nave)

#naves inimigas modo médio
def tiros():
    lista_inimigo = []
    for i in range(8):
        x_inicial = 700
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
for i in range(5):
    shot = image.load(f'inimigo_medio/Shooting/Shot{i}.png')
    shot = transform.scale(shot, (45,15))
    shot_imagem.append(shot)

# ---TEMPO---

fonte = font.Font(None, 30)

while running:
    for ev in event.get():
        if ev.type == QUIT:
            quit()
            sys.exit()
        if tela_atual == 'login':
            if ev.type == MOUSEBUTTONDOWN:
                campo_ativo = caixa_nome.collidepoint(ev.pos)

            if ev.type == KEYDOWN and campo_ativo:
                if ev.key == K_RETURN:
                    if 0 < len(texto_nome) <= 6:
                        nome = texto_nome
                        tela_atual = 'jogo'
                        tempo_inicial = time.get_ticks()  
                elif ev.key == K_BACKSPACE:
                    texto_nome = texto_nome[:-1]
                else:
                    if len(texto_nome) < 6:
                        texto_nome += ev.unicode

        elif tela_atual == 'jogo':
            if ev.type == MOUSEBUTTONDOWN:
                if ev.button == 1:
                    pos_clique = mouse.get_pos()
                if botao_rec.collidepoint(pos_clique) and derrota == True:
                    resetar_jogo(estado)
                    derrota = estado['derrota']
                    life = estado['life']
                    tempo_decorrido = estado['tempo_decorrido']
                    tempo_inicial = estado['tempo_inicial']
                    pos_x = estado['pos_x']
                    pos_y = estado['pos_y']
                    direita = estado['direita']
                    esquerda = estado['esquerda']
                    modo_invencivel = estado['modo_invencivel']
                    tempo_invencivel = estado['tempo_invencivel']
                    explosoes_ativas = estado['explosoes_ativas']
                    lista_asteroides = estado['lista_asteroides']
                    bando_de_naves = estado['bando_de_naves']
                    lista = estado['lista']
                    jumpscare_tocado = estado['jumpscare_tocado']
                    time_sixseven = random.randint(20, 80)

        screen.blit(sixseven, (75,160))

        if ev.type == KEYDOWN:
            if tela_atual == 'inicio':
                if ev.key == K_DOWN: opcao_selecionada = (opcao_selecionada + 1) % len(opcoes)
                if ev.key == K_UP:   opcao_selecionada = (opcao_selecionada - 1) % len(opcoes)
                if ev.key == K_RETURN:
                    if opcao_selecionada == 0: tela_atual = 'login'
                    else: quit(); sys.exit()

    clock.tick(60)
    dt = clock.get_time()
    keys = key.get_pressed()

    if tela_atual == 'inicio':
        desenha_texto_sombra('SPACE', fonte_gta_titulo, AMARELO_GTA, centraliza_x('SPACE', fonte_gta_titulo), 100)
        desenha_texto_sombra('WARS', fonte_gta_titulo, BRANCO, centraliza_x('WARS', fonte_gta_titulo), 200)
        
        for i, opt in enumerate(opcoes):
            y = 400 + (i * 50)
            cor = AMARELO_GTA if i == opcao_selecionada else BRANCO
            desenha_texto_sombra(opt, fonte_menu, cor, centraliza_x(opt, fonte_menu), y)

    if tela_atual == 'login':
        tela_inicio()          
    elif tela_atual == 'jogo':
        if derrota == False:
            tempo_atual = time.get_ticks()
            tempo_decorrido = (tempo_atual - tempo_inicial) // 1000
        
        #dificuldade primeiro nivel
        if tempo_decorrido>=30:
            aumento_vel = 1.5
        else:
            aumento_vel = 1

        #coracoes
        if derrota == False:
            timer_spawn_vida += dt
            
            if timer_spawn_vida > 30000:
                novo_coracao = {
                    'x': random.randint(800, 850),
                    'y': random.randint(50, 550),
                    'hitbox': Rect(0, 0, 30, 30)
                }
                itens_vida_ativos.append(novo_coracao)
                timer_spawn_vida = 0

        if keys[K_6]:
            modo_6 = True
        if keys[K_7] and modo_6:
            life = 10000

        if keys[K_g]:
            modo_g = True
        if keys[K_u] and modo_g:
            modo_u = True
        if keys[K_i] and modo_u:
            top5 = [("---", 0), ("---", 0), ("---", 0), ("---", 0), ("---", 0)]
            with open("ranking.txt", "w") as arquivo:
                for jogador, score in top5:
                    arquivo.write(f"{jogador},{score}\n")

        # ---MOVIMENTAÇÃO + ANIMAÇÃO + HITBOXES-----

        #nave principal

        if keys[K_a] and life!=0 and pos_x > 0:
            esquerda = True
            direita = False
            pos_x -= 0.3*dt
        elif keys[K_d] and life!=0 and pos_x < 720:
            direita = True
            esquerda = False
            pos_x += 0.3*dt
        
        if keys[K_w] and life!=0 and pos_y > 0:
            pos_y -= 0.3*dt
        elif keys[K_s] and life!=0 and pos_y < 560:
            pos_y += 0.3*dt

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

        screen.blit(imagem_ceu, (0, 0))

        #inimigos

        hitboxes_inimigas = []

        #vidas
        

        #asteroides
        if tempo_decorrido > 60 and derrota == False:
            for ast in lista_asteroides:
                ast[0] -= vel_ast 
                
                screen.blit(asteroide, (ast[0], ast[1]))
                raio = tam-5
                centro_x = int(ast[0] + raio)
                centro_y = int(ast[1] + raio)
                ast_hitbox = draw.circle(screen, (255, 0, 0), (centro_x, centro_y), raio, 2)
                hitboxes_inimigas.append(ast_hitbox)
                if ast[0] < -150:
                    ast[0] = 800
                    ast[1] = random.randint(0, 550)

            for pos in lista:
                pos_xN = 700
                screen.blit(inimigo_imagem[current_frame_I], (pos_xN,pos[1]), (0,0,79.5,40.5)) #safadin
                nave_laser_hitbox = Rect(pos_xN, pos[1], 79.5, 40.5)
                hitboxes_inimigas.append(nave_laser_hitbox)
                pos[0] = pos[0] - 0.5 * dt
                screen.blit(shot_imagem[current_frame_S], (pos[0]-10, pos[1]+15), (0,0,45,15)) #safadin
                laser_hitbox = Rect(pos[0]-10, pos[1]+15, 45, 15)
                hitboxes_inimigas.append(laser_hitbox)
                if pos[0] < -100:
                    pos_xN = pos_xN + 0.2 * dt
                    lista = tiros()

            anim_time_I += dt
            anim_time_sec_I = anim_time_I/1000

            if anim_time_sec_I > 0.5:
                current_frame_I += 1
                if current_frame_I > 5:
                    current_frame_I = 0
                anim_time_sec_I = 0

            anim_time_S += dt
            anim_time_sec_S = anim_time_S/1000

            if anim_time_sec_S > 0.1:
                current_frame_S += 1
                if current_frame_S > 4:
                    current_frame_S = 0
                anim_time_S = 0


        # planetas grandes como props (igual às árvores no jogo 1)
        for px, py in planetas_grandes:
            screen.blit(pb, (px, py))

        # asteroides e planetas pequenos do fundo
        for i in range(len(mapa)):
            tiles = mapa[i].split(',')
            for j in range(len(tiles)):
                tile = tiles[j].strip()
                if tile in tiles_img:
                    screen.blit(tiles_img[tile], (offset_x + j * tile_size, offset_y + i * tile_size))

        draw.rect(screen, (102, 51, 0), (20, 20, 200, 70), border_radius=20)

        if derrota == False:
            if tempo_decorrido < 60:
                for nave in bando_de_naves:
                    nave.atualizar_e_desenhar(screen, dt, nave.minha_animacao, aumento_vel)
                    hitboxes_inimigas.append(nave.ship_hitbox)

        player_hitbox = Rect(pos_x, pos_y, 79.5, 40.5)

        if player_hitbox.collidelist(hitboxes_inimigas) != -1 and life != 0 and not modo_invencivel:
            life -= 1
            if life == 1 or life == 2:
                som_dano.play()
            if life == 0:
                som_morte.play()
                tempo_morte = time.get_ticks()//1000
                nova_explosao = {
                    'x': pos_x-10,
                    'y': pos_y-20,
                    'frame': 0,
                    'tempo': 0
                }
                explosoes_ativas.append(nova_explosao)
                print(f"{nome}: {tempo_morte:.1f}s")
                
                top5.append((nome, tempo_decorrido))
                top5.sort(key=lambda x: x[1], reverse=True)
                top5 = top5[:5]
                
                with open("ranking.txt", "w") as arquivo:
                    for jogador, score in top5:
                        arquivo.write(f"{jogador},{score}\n")
            modo_invencivel = True
            tempo_invencivel = 3000

        if tempo_decorrido == time_sixseven and derrota == False:
            screen.blit(sixseven_gigante, (-50,0))
            if jumpscare_tocado == False:
                scream.play()
                jumpscare_tocado = True
    
        if modo_invencivel:
            tempo_invencivel -= dt
            if tempo_invencivel <= 0:
                modo_invencivel = False
                som_imortal.play()

        if ((not modo_invencivel) or (modo_invencivel and (tempo_invencivel // 300) % 2 == 0)) and life != 0:
            if direita:
                screen.blit(ship_animation_R[current_frame_R], (pos_x,pos_y), (0,0,79.5,40.5))
            elif esquerda:
                screen.blit(ship_animation_L[current_frame_L], (pos_x,pos_y), (0,0,79.5,40.5))

        # -----LAYOUT DO JOGO-----
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
            derrota = True

        # colocar os textos
        texto1 = fonteLAY.render('A - esquerda', True, (255, 255, 255))
        texto2 = fonteLAY.render('D - direita', True, (255, 255, 255))
        texto3 = fonteLAY.render('w - cima', True, (255, 255, 255))
        texto4 = fonteLAY.render('S - baixo', True, (255, 255, 255))

        screen.blit(texto1, (25, 420))
        screen.blit(texto2, (25, 440))
        screen.blit(texto3, (25, 460))
        screen.blit(texto4, (25, 480))

        texto = fonte.render(f'Tempo: {tempo_decorrido}s', True, (255,255,255))
        screen.blit(texto, (630,20))

        # -----MORTE + GRAVAÇÃO DE RANKING-----

        explosoes_para_remover = [] 

        for exp in explosoes_ativas:
            screen.blit(animacao_explosao[exp['frame']], (exp['x'], exp['y']))
            
            exp['tempo'] += dt
            if exp['tempo'] > 150:  # tempo entre frames da explosão
                exp['frame'] += 1
                exp['tempo'] = 0
                
                if exp['frame'] >= len(animacao_explosao):
                    explosoes_para_remover.append(exp)

        for exp in explosoes_para_remover:
            explosoes_ativas.remove(exp)
        
        texto_titulo_top = fonte.render('Top 5:', True, (255, 255, 0))
        
        if derrota == True:
            screen.blit(blur_surface, (0, 0))
            texto_titulo_top = fonte.render('Top 5:', True, (255, 255, 0))
            screen.blit(texto_titulo_top, (550, 120))
            for i, (jogador, score) in enumerate(top5):
                texto_score = fonte.render(f'{i+1}º - {jogador} - {score}s', True, (200, 200, 200))
                screen.blit(texto_score, (550, 140 + (i * 25)))
            textoDerrota = fonteDerrota.render('WASTED', True, (200,20,20))
            screen.blit(textoDerrota, (200,100))
            draw.rect(screen, (255,255,255), (300,300,150,50), border_radius = 20)
            texto6 = fonte.render('Jogar de novo', True, (0,0,0))
            screen.blit(texto6, (310,310))
    
        if derrota == False:
            coracoes_para_remover = []

            for coracao in itens_vida_ativos:
                coracao['x'] -= 2 
                
                coracao['hitbox'].x = coracao['x']
                coracao['hitbox'].y = coracao['y']
                
                screen.blit(imagem_item_vida, (coracao['x'], coracao['y']))
                
                if player_hitbox.colliderect(coracao['hitbox']):
                    if life < 3 and life > 0: 
                        life += 1
                        som_repair.play()
                    coracoes_para_remover.append(coracao)
                    
                elif coracao['x'] < -50:
                    coracoes_para_remover.append(coracao)

            for coracao in coracoes_para_remover:
                if coracao in itens_vida_ativos:
                    itens_vida_ativos.remove(coracao)
    
    display.update()