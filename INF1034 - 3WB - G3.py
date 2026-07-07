from pygame import *
import sys

import random

clock = time.Clock()
init()
mixer.init()
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
vitoria = False
muda_fase = False
musica_fase = ''
boss_tocado = False
atirar = False

# -----BOSS-----

velocidade_boss = 0.8
angulo_boss = 0
velocidade_giro_boss = 0.08
Rhand_y = 380
Lhand_y = 480
velocidade_mao = velocidade_giro_boss*11.5
modo_ataque = False
modo_ataque2 = False
modo_ataque3 = False
modo_rapido = False
qtd_bats = 10
lado_boss = random.choice(['direita', 'esquerda'])
if lado_boss == 'direita':
    boss_x = 900
else:
    boss_x = -400

boss_vida_max = 100
boss_vida = 100

tempo_entre_ataques = 0
ataque_em_andamento = False
boss_x_destino = 480

etapa_boss = 0  # 0: Escondido, 1: Entrando, 2: Atacando, 3: Fugindo
timer_boss = 0

def boss_tomar_dano(dano):
    global boss_vida # esse global serve para avisar pro codigo q e pra ele usar a vida do boss q esta fora dessa funçao
    boss_vida -= dano
    if boss_vida < 0:
        boss_vida = 0

time_sixseven = random.randint(20, 80)
jumpscare_tocado = False
sixseven_gigante = transform.scale(image.load('imagens/67.jpg'), (1000, 700))

# -----RESET DO JOGO-----

estado = {
    'life': 3,
    'derrota': False,
    'vitoria': False,
    'muda_fase': False,
    'musica_fase': '',
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
    'jumpscare_tocado': False,
    'boss_x': 900,
    'boss_vida': 100,
    'boss_vida_max': 100,
    'boss_tocado': False,
    'bando_de_bats': [],
    'atirar': False,
    'pos_xA': 350,
    'pos_yA': 50,
}

def resetar_jogo(estado):
    estado['life'] = 3
    estado['derrota'] = False
    estado['vitoria'] = False
    estado['muda_fase'] = ''
    estado['musica_fase'] = True
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
    estado['boss_x'] = 900
    estado['boss_vida'] = 100
    estado['boss_vida_max'] = 100
    estado['boss_tocado'] = False
    estado['atirar'] = False
    estado['pos_xA'] = 350
    estado['pos_yA'] = 50

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

    # recria os morcegos inimigos
    novos_bats = []
    for i in range(qtd_bats):
        novos_bats.append(batNPC(800, 0, opcoes_de_cores_bat, lado_boss))
    estado['bando_de_bats'] = novos_bats

    # recria os tiros inimigos
    estado['lista'] = tiros()
    estado['lista_boss'] = tiros_boss('direita')
    estado['lado_boss'] = 'direita'
    estado['etapa_boss'] = 0
    estado['timer_boss'] = 0

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
    fonte_gta_titulo = font.Font('textos/GTA.otf', 90)
    fonte_gta_med    = font.Font('textos/GTA.otf', 65)
    fonte_menu       = font.Font('textos/texto.ttf', 28)
    fonte_padrao     = font.Font('textos/texto.ttf', 20)
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
fonte = font.Font('textos/texto.ttf', 15)
fundo = image.load('background/blue-back.png')
fundo = transform.scale(fundo, (800, 600))
tela_atual = 'inicio'
texto_nome = ''
campo_ativo = False
caixa_nome = Rect(300, 280, 200, 35)
fonte_login = font.Font('textos/texto.ttf', 15)
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

top5.sort(key=lambda x: x[1], reverse=False)

while len(top5) < 5:
    top5.append(("---", 9999))
top5 = top5[:5]

# ---SONS---

def tocar_musica(arquivo):
    global musica_fase

    if musica_fase != arquivo:
        mixer.music.stop()
        mixer.music.load(arquivo)
        mixer.music.play(-1)
        mixer.music.set_volume(0.3)
        musica_fase = arquivo
    

vit = mixer.Sound('sons/vitoriaGTA.mp3')
som_dano = mixer.Sound('sons/mario-power-down.mp3')
som_morte = mixer.Sound('sons/roblox-explosion-sound.mp3')
som_imortal = mixer.Sound('sons/imortal.mp3')
som_repair = mixer.Sound('sons/repair.mp3')
scream = mixer.Sound('sons/scream2.mp3')
fase = mixer.Sound('sons/fase.mp3')
boss_song = mixer.Sound('sons/67boss.mp3')
boss_song.set_volume(0.6)

gritos_boss = [
    mixer.Sound('sons/grito1.mp3'), # Troque pelo nome real dos seus arquivos
    mixer.Sound('sons/grito2.mp3'),
    mixer.Sound('sons/grito3.mp3'),
    mixer.Sound('sons/grito4.mp3'),
    mixer.Sound('sons/scream3.mp3')
]

for grito in gritos_boss:
    grito.set_volume(0.4)

vit.set_volume(0.3)
som_dano.set_volume(0.3)
som_morte.set_volume(0.3)
som_imortal.set_volume(0.3)
som_repair.set_volume(0.3)
scream.set_volume(0.3)
fase.set_volume(0.3)

# -----IMAGENS-----

#explosao
animacao_explosao = []
for i in range(8):
    img_exp = image.load(f'kaboom/explosion{i+1}.png')
    img_exp = transform.scale(img_exp, (100, 100))
    animacao_explosao.append(img_exp)

explosoes_ativas = []


#arma
valor_opacidade = 0
arma = transform.scale(image.load('imagens/armas.png'), (100,100))
pos_xA = 350
pos_yA = 50

#boss
sixseven = image.load('imagens/67.png')
vida_realista = imagem_item_vida = transform.scale(image.load('imagens/heart.png'), (30, 30))

itens_vida_ativos = []
timer_spawn_vida = 0

# fundo
imagem_ceu = transform.scale(image.load("background/blue-with-stars.png"), (800, 600))
mapa_2 = transform.scale(image.load('background/Space Background2.png'), (800, 600))
mapa_3 = transform.scale(image.load('background/Space Background3.png'), (800, 600))
galaxia = transform.scale(image.load('background/estrelas.jpg'), (800, 600))
fundo_67 = transform.scale(image.load('background/fundo_67.jpeg'), (800, 600))


# tile de asteroide 
a2 = transform.scale(image.load('background/asteroid-2.png'), (tile_size, tile_size))

# planeta pequeno 
ps = image.load('background/prop-planet-small.png')

# planeta grande 
pb = image.load('background/prop-planet-big.png')

#coisa voando
asteroide = transform.scale(image.load('background/asteroid-2.png'), (50, 50))

#sixseven boss
boss = transform.scale(image.load('imagens/67zin.png'), (300, 600))

#Rhand
Rhand = transform.scale(image.load('imagens/hand1.png'), (150, 150))

#Lhand
Lhand = transform.flip(Rhand, True, False)

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
fonteLAY = font.Font('textos/texto.ttf', 10)

# imagem de coraçao do lado da vida
vida = image.load('imagens/vida.png')
life = 3

# tela de derrota
blur = 150
blur_surface = Surface((1000, 600))
blur_surface.set_alpha(blur) # Valor de opacidade (0 = invisível, 255 = totalmente opaco)
blur_surface.fill((0, 0, 0)) # Cor do desfoque (preto)
fonteJ = font.Font('textos/texto.ttf', 15)
botao_rec = Rect(300,300,150,50)
fonteDerrota = font.Font('textos/GTA.otf', 75)

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

#tiro da nave principal

tiro_animacao = []
lista_tiros = []
tempo_tiro = 0
intervalo_tiro = 150  

for i in range(5):      # quantidade de frames
    img = image.load(f"inimigo_medio/Shooting/Shot{i}.png")
    img = transform.scale(img, (30, 15))
    tiro_animacao.append(img)

class Tiro:

    def __init__(self, x, y, direita):
        self.x = x
        self.y = y
        self.direita = direita
        self.velocidade = 12
        self.animacao = tiro_animacao
        self.frame = 0
        self.tempo_animacao = 0
        self.hitbox = Rect(self.x, self.y, 30, 15)

    def atualizar(self, dt):
        # movimento
        if self.direita:
            self.x += self.velocidade
        else:
            self.x -= self.velocidade
        # hitbox
        self.hitbox.x = self.x
        self.hitbox.y = self.y
        # animação
        self.tempo_animacao += dt
        if self.tempo_animacao > 60:
            self.frame += 1
            if self.frame >= len(self.animacao):
                self.frame = 0
            self.tempo_animacao = 0

    def desenhar(self, tela):
        imagem = self.animacao[self.frame]
        if not self.direita:
            imagem = transform.flip(imagem, True, False)
        tela.blit(imagem, (self.x, self.y))

    def fora_da_tela(self):
        return self.x > 820 or self.x < -40
    

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


#inimigos do boss

bat_67 = []

for i in range(2):
    bat_67.append(transform.scale(image.load(f"imagens/bat_6{i+7}.png"), (80, 80)))

opcoes_de_cores_bat = [bat_67]

class batNPC:
    def __init__(self, limite_x, chao_y, opcoes_de_cores_bat, lado='direita'):
            #posição inicial na tela
            if lado == 'direita':
                self.x = random.randint(570, 600)
                self.y = random.randint(240, 370)
                self.velocidade_x = random.choice([-4, -3, -2]) # voa para a esquerda
            else: # se o boss estiver na esquerda
                self.x = random.randint(60, 90) # nasce perto da mão esquerda do boss
                self.y = random.randint(240, 370)
                self.velocidade_x = random.choice([2, 3, 4]) # voa para a direita
            
            self.velocidade_y = random.choice([1,2,3,4,-1,-2,-3,-4,0])

            self.minha_animacao = random.choice(opcoes_de_cores_bat)
            self.frame_atual = random.randint(0,  len(self.minha_animacao) - 1)
            self.tempo_animacao = 0

            self.bat_hitbox = Rect(self.x, self.y, tam+7, tam+10)

    def atualizar_e_desenhar(self, tela, dt, lista_animacao, mult_vel):
        #movimento
        self.x = self.x + (self.velocidade_x * mult_vel)
        self.y = self.y + (self.velocidade_y * mult_vel)

        self.bat_hitbox.x = self.x + 22
        self.bat_hitbox.y = self.y +10

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

bando_de_bats = []

for i in range(qtd_bats): # Pode colocar 10, 20...
    # Passamos as opções de cores para ele sortear quando nascer
    novo_bat = batNPC(800, 0, opcoes_de_cores_bat)
    bando_de_bats.append(novo_bat)

def tiros_boss(lado='direita'):
    lista_inimigo = []
    for i in range(10):
        if lado == 'direita':
            x_inicial = random.randint(800, 1200) # Nasce fora pela direita
        else:
            x_inicial = random.randint(-400, -50) # Nasce fora pela esquerda
            
        y_inicial = random.randint(0,600)
        lista_inimigo.append([x_inicial, y_inicial])
    return lista_inimigo

#naves inimigas modo médio
def tiros():
    lista_inimigo = []
    for i in range(8):
        x_inicial = 700
        y_inicial = random.randint(0,600)
        lista_inimigo.append([x_inicial, y_inicial])
    return lista_inimigo

lista = tiros()
lista_boss = tiros_boss()

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
        if tela_atual == 'inicio':
            if ev.type == KEYDOWN:
                if ev.key == K_DOWN: opcao_selecionada = (opcao_selecionada + 1) % len(opcoes)
                if ev.key == K_UP:   opcao_selecionada = (opcao_selecionada - 1) % len(opcoes)
                if ev.key == K_RETURN:
                    if opcao_selecionada == 0: tela_atual = 'login' 
                    if opcao_selecionada == 0:valor_opacidade = 0
                    else: quit(); sys.exit()
        if tela_atual == 'login':
            if ev.type == MOUSEBUTTONDOWN:
                campo_ativo = caixa_nome.collidepoint(ev.pos)
            if ev.type == KEYDOWN:
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
                if botao_rec.collidepoint(pos_clique) and (derrota or vitoria):                    
                    resetar_jogo(estado)
                    musica_fase = ''
                    life = estado['life']
                    derrota = estado['derrota']
                    vitoria = estado['vitoria']
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
                    boss_x = estado['boss_x']
                    boss_vida = estado['boss_vida']
                    bando_de_bats = estado['bando_de_bats']
                    lista_boss = estado['lista_boss']
                    lado_boss = estado['lado_boss']
                    etapa_boss = estado['etapa_boss']
                    timer_boss = estado['timer_boss']
                    atirar = estado['atirar']
                    pos_xA = estado['pos_xA']
                    pos_yA = estado['pos_yA']
                    modo_ataque = False
                    modo_ataque2 = False
                    modo_ataque3 = False
                    modo_rapido = False
                    angulo_boss = 0
                    velocidade_giro_boss = 0.08
                    Rhand_y = 380
                    Lhand_y = 480
                    velocidade_mao = velocidade_giro_boss * 11.5

    clock.tick(60)
    dt = clock.get_time()
    tempo_tiro += dt
    keys = key.get_pressed()

    if tela_atual == 'inicio':
        desenha_texto_sombra('SPACE', fonte_gta_titulo, AMARELO_GTA, centraliza_x('SPACE', fonte_gta_titulo), 100)
        desenha_texto_sombra('WARS', fonte_gta_titulo, BRANCO, centraliza_x('WARS', fonte_gta_titulo), 200)
        if valor_opacidade < 255:
            valor_opacidade += 0.03
            
        sixseven.set_alpha(int(valor_opacidade))
        screen.blit(sixseven, (75, 170))
        for i, opt in enumerate(opcoes):
            y = 400 + (i * 50)
            cor = AMARELO_GTA if i == opcao_selecionada else BRANCO
            desenha_texto_sombra(opt, fonte_menu, cor, centraliza_x(opt, fonte_menu), y)

    if tela_atual == 'login':
        tela_inicio()
                  
    elif tela_atual == 'jogo':

        if derrota == False and vitoria == False:
            tempo_atual = time.get_ticks()
            tempo_decorrido = (tempo_atual - tempo_inicial) // 1000
        
        #dificuldade primeiro nivel
        if tempo_decorrido>=30:
            aumento_vel = 1.5
        else:
            aumento_vel = 1

        #coracoes
        if derrota == False and vitoria == False:
            timer_spawn_vida += dt
            
            if timer_spawn_vida > 30000:
                novo_coracao = {
                    'x': random.randint(800, 850),
                    'y': random.randint(50, 550),
                    'hitbox': Rect(0, 0, 30, 30)
                }
                itens_vida_ativos.append(novo_coracao)
                timer_spawn_vida = 0

        # -----ATALHOS-----

        if keys[K_6]:
            modo_6 = True
        if keys[K_7] and modo_6:
            life = 10000
        
        if keys[K_4]:
            modo_4 = True
        if keys[K_2] and modo_4:
            life = 3
        if keys[K_o]:
            tempo_decorrido += 115
        if keys[K_g]:
            modo_g = True
        if keys[K_u] and modo_g:
            modo_u = True
        if keys[K_i] and modo_u:
            top5 = [("---", 9999), ("---", 9999), ("---", 9999), ("---", 9999), ("---", 9999)]
            with open("ranking.txt", "w") as arquivo:
                for jogador, score in top5:
                    arquivo.write(f"{jogador},{score}\n")

        # --- MAPA + MÚSICA ---

        if tempo_decorrido >= 0:
            screen.blit(galaxia, (0, 0))

        if tempo_decorrido < 55:
            screen.blit(imagem_ceu, (0, 0))
        
        if tempo_decorrido < 60 and ((tempo_atual-tempo_inicial)//500)%2 == 0:
            screen.blit(imagem_ceu, (0, 0))

        if 60 < tempo_decorrido < 115:
            screen.blit(mapa_2, (0, 0))

        if 60 < tempo_decorrido < 120 and ((tempo_atual-tempo_inicial)//500)%2 == 0:
            screen.blit(mapa_2, (0, 0))

        if 120 < tempo_decorrido :
            screen.blit(fundo_67, (0, 0))

        if not vitoria and not derrota:
            if tempo_decorrido < 60:
                tocar_musica("sons/fase_fácil.mp3")
            elif tempo_decorrido < 115:
                tocar_musica("sons/fase_media_f.mp3")
            elif tempo_decorrido >= 120 and vitoria == False:
                tocar_musica("sons/67boss.mp3")

        # ---MOVIMENTAÇÃO + ANIMAÇÃO + HITBOXES + BOSS-----

        #nave principal

        if keys[K_a] and life!=0 and pos_x > 0 and vitoria == False:
            esquerda = True
            direita = False
            pos_x -= 0.3*dt
        elif keys[K_d] and life!=0 and pos_x < 720 and vitoria == False:
            direita = True
            esquerda = False
            pos_x += 0.3*dt
        if keys[K_w] and life!=0 and pos_y > 0 and vitoria == False:
            pos_y -= 0.3*dt
        elif keys[K_s] and life!=0 and pos_y < 560 and vitoria == False:
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

        #inimigos

        hitboxes_inimigas = []
        
        #asteroides
        if  116 > tempo_decorrido > 60 and derrota == False and vitoria == False:
            for ast in lista_asteroides:
                ast[0] -= vel_ast 
                
                screen.blit(asteroide, (ast[0], ast[1]))
                raio = tam-5
                centro_x = int(ast[0] + raio)
                centro_y = int(ast[1] + raio)
                ast_hitbox = Rect(centro_x - raio, centro_y - raio, raio * 2, raio * 2)
                # ast_hitbox = draw.circle(screen, (255, 0, 0), (centro_x, centro_y), raio, 2)
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

        #sixseven boss
        if  120 < tempo_decorrido and derrota == False and vitoria == False:
            if etapa_boss == 0:
                timer_boss += dt
                if timer_boss > 2000:
                    lado_boss = random.choice(['direita', 'esquerda'])
                    if lado_boss == 'direita':
                        boss_x = 900
                        boss_x_destino = 480
                    else:
                        boss_x = -400
                        boss_x_destino = 40
                    etapa_boss = 1
                    timer_boss = 0
            elif etapa_boss == 1:
                if boss_x > boss_x_destino:
                    boss_x -= velocidade_boss * 10
                elif boss_x < boss_x_destino:
                    boss_x += velocidade_boss * 10
                if abs(boss_x - boss_x_destino) < 15:
                    etapa_boss = 2
                    timer_boss = 0
                    
                    bando_de_bats = [] 
                    for i in range(qtd_bats):
                        bando_de_bats.append(batNPC(0, 0, opcoes_de_cores_bat, lado_boss))
                    lista_boss = tiros_boss(lado_boss)
                    
                    qual_ataque = random.choice([1, 2])
                    if qual_ataque == 1:
                        modo_ataque = True
                    else:
                        modo_ataque2 = True
                        Rhand_y = 120
                        Lhand_y = 140
                    random.choice(gritos_boss).play()
            elif etapa_boss == 2:
                timer_boss += dt
                if (modo_ataque or modo_ataque2) and not modo_rapido:
                    velocidade_mao = 20
                    velocidade_giro_boss = 4
                    modo_rapido = True
                if timer_boss > 4000:
                    modo_ataque = False
                    modo_ataque2 = False
                    modo_ataque3 = False
                    modo_rapido = False
                    angulo_boss = 0
                    Rhand_y = 420
                    Lhand_y = 440
                    velocidade_giro_boss = 0.08
                    velocidade_mao = velocidade_giro_boss * 11.5
                    etapa_boss = 3 #
                    timer_boss = 0
            elif etapa_boss == 3:
                if lado_boss == 'direita':
                    boss_x += velocidade_boss * 10
                    if boss_x > 900:
                        etapa_boss = 0 
                else:
                    boss_x -= velocidade_boss * 10
                    if boss_x < -400:
                        etapa_boss = 0
            boss_y = -30
            angulo_boss += velocidade_giro_boss
            if modo_ataque == False and modo_ataque2 == False and modo_ataque3 == False:
                if angulo_boss >= 4 or angulo_boss <= -4:
                    velocidade_giro_boss = velocidade_giro_boss * -1
                    velocidade_mao = velocidade_mao * -1
            if modo_ataque == True or modo_ataque2 == True or modo_ataque3 == True:
                if angulo_boss >= 4 or angulo_boss <= -4:
                    velocidade_giro_boss = velocidade_giro_boss * -1
            boss_girando = transform.rotate(boss, angulo_boss)
            retangulo_original = boss.get_rect(topleft=(boss_x, boss_y))
            retangulo_girando = boss_girando.get_rect(center=retangulo_original.center)
            screen.blit(boss_girando, retangulo_girando.topleft)
            Rhand_x = boss_x-20
            Rhand_y += -velocidade_mao
            head_hitbox1 = Rect(boss_x+70, boss_y+80, 170, 160)
            draw.rect(screen, (255, 255, 255), head_hitbox1, 2)
            hitboxes_inimigas.append(head_hitbox1)
            Head_hitbox2 = Rect(boss_x+100, boss_y+240, 110, 350)
            draw.rect(screen, (255, 255, 255), Head_hitbox2, 2)
            hitboxes_inimigas.append(Head_hitbox2)
            if modo_ataque2 == False:
                Rhand_y = max(380, min(Rhand_y, 480))
            screen.blit(Rhand, (Rhand_x, Rhand_y))
            Rhand_hitbox1 = Rect(Rhand_x+40, Rhand_y+40, 80, 75)
            Rhand_hitbox2 = Rect(Rhand_x+60, Rhand_y+112, 45, 35)
            Rhand_hitbox3 = Rect(Rhand_x, Rhand_y, 90, 45)
            Rhand_hitbox4 = Rect(Rhand_x+23, Rhand_y+53, 18, 50)
            Rhand_hitbox5 = Rect(Rhand_x+120, Rhand_y+80, 30, 30)
            draw.rect(screen, (255, 255, 255), Rhand_hitbox1, 2)
            draw.rect(screen, (255, 255, 255), Rhand_hitbox2, 2)
            draw.rect(screen, (255, 255, 255), Rhand_hitbox3, 2)
            draw.rect(screen, (255, 255, 255), Rhand_hitbox4, 2)
            draw.rect(screen, (255, 255, 255), Rhand_hitbox5, 2)
            hitboxes_inimigas.append(Rhand_hitbox1)
            hitboxes_inimigas.append(Rhand_hitbox2)
            hitboxes_inimigas.append(Rhand_hitbox3)
            hitboxes_inimigas.append(Rhand_hitbox4)
            hitboxes_inimigas.append(Rhand_hitbox5)
            Lhand_x = boss_x+180
            Lhand_y += velocidade_mao
            if modo_ataque2 == False:
                Lhand_y = max(380, min(Lhand_y, 480))
            screen.blit(Lhand, (Lhand_x, Lhand_y))
            Lhand_hitbox1 = Rect(Lhand_x+30, Lhand_y+40, 80, 75)
            Lhand_hitbox2 = Rect(Lhand_x+45, Lhand_y+112, 45, 35)
            Lhand_hitbox3 = Rect(Lhand_x+60, Lhand_y, 90, 45)
            Lhand_hitbox4 = Rect(Lhand_x+108, Lhand_y+53, 18, 50)
            Lhand_hitbox5 = Rect(Lhand_x, Lhand_y+80, 30, 30)
            draw.rect(screen, (255, 255, 255), Lhand_hitbox1, 2)
            draw.rect(screen, (255, 255, 255), Lhand_hitbox2, 2)
            draw.rect(screen, (255, 255, 255), Lhand_hitbox3, 2)
            draw.rect(screen, (255, 255, 255), Lhand_hitbox4, 2)
            draw.rect(screen, (255, 255, 255), Lhand_hitbox5, 2)
            hitboxes_inimigas.append(Lhand_hitbox1)
            hitboxes_inimigas.append(Lhand_hitbox2)
            hitboxes_inimigas.append(Lhand_hitbox3)
            hitboxes_inimigas.append(Lhand_hitbox4)
            hitboxes_inimigas.append(Lhand_hitbox5)
            if modo_ataque == True or modo_ataque3 == True:
                if Lhand_y >= 480 or Lhand_y <= 380:
                    velocidade_mao = velocidade_mao * -1
            if modo_ataque2 == True:
                if Lhand_y >=180 or Lhand_y <= 80:
                    velocidade_mao = velocidade_mao * -1
            if (modo_ataque == True or modo_ataque2 == True or modo_ataque3 == True) and modo_rapido == False:
                velocidade_mao = 20
                velocidade_giro_boss = 4
                modo_rapido = True #tempo para parar o ataque             
            if modo_ataque == True and modo_rapido == True:
                for bat in bando_de_bats:
                    bat.atualizar_e_desenhar(screen, dt, bat.minha_animacao, aumento_vel)
                    hitboxes_inimigas.append(bat.bat_hitbox)
                    draw.rect(screen, (255, 0, 0), (bat.bat_hitbox), 2)
            if modo_ataque2 == True and modo_rapido == True:
                for pos in lista_boss:
                    if lado_boss == 'direita':
                        pos[0] = pos[0] - 0.8 * dt
                        imagem_tiro = shot_imagem[current_frame_S]
                    else:
                        pos[0] = pos[0] + 0.8 * dt
                        imagem_tiro = transform.flip(shot_imagem[current_frame_S], True, False)
                    
                    screen.blit(imagem_tiro, (pos[0], pos[1]), (0, 0, 45, 15))
                    
                    laser_hitbox = Rect(pos[0], pos[1], 45, 15)
                    hitboxes_inimigas.append(laser_hitbox)
                    draw.rect(screen, (255, 0, 0), (laser_hitbox), 2)
                    
                    if lado_boss == 'direita' and pos[0] < -100:
                        pos[0] = 800
                        pos[1] = random.randint(0, 600)
                    elif lado_boss == 'esquerda' and pos[0] > 900:
                        pos[0] = -100
                        pos[1] = random.randint(0, 600)
                        
                anim_time_S += dt
                anim_time_sec_S = anim_time_S / 1000

                if anim_time_sec_S > 0.1:
                    current_frame_S += 1
                    if current_frame_S > 4:
                        current_frame_S = 0
                    anim_time_S = 0

        draw.rect(screen, (102, 51, 0), (20, 20, 200, 70), border_radius=20)

        #movimenação aleatória das naves
        if derrota == False:
            if tempo_decorrido < 60:
                for nave in bando_de_naves:
                    nave.atualizar_e_desenhar(screen, dt, nave.minha_animacao, aumento_vel)
                    hitboxes_inimigas.append(nave.ship_hitbox)

        #hitbox do jogador
        player_hitbox = Rect(pos_x, pos_y, 79.5, 40.5)

        if player_hitbox.collidelist(hitboxes_inimigas) != -1 and life != 0 and not modo_invencivel and vitoria == False:
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
            modo_invencivel = True
            tempo_invencivel = 3000
        

        #jumpscare
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

        if 120 > tempo_decorrido > 117:
            pos_x = 350
            pos_y = 300
            pos_yA += 0.1*dt
            screen.blit(arma, (pos_xA, pos_yA))
            
        if tempo_decorrido>120:
            atirar = True

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
            if derrota == False:
                derrota = True
                mixer.music.stop()
                musica_fase = ''

        # colocar os textos
        texto1 = fonteLAY.render('A - esquerda', True, (255, 255, 255))
        texto2 = fonteLAY.render('D - direita', True, (255, 255, 255))
        texto3 = fonteLAY.render('w - cima', True, (255, 255, 255))
        texto4 = fonteLAY.render('S - baixo', True, (255, 255, 255))
        texto5 = fonteLAY.render('J - atirar', True, (255, 255, 255))

        screen.blit(texto1, (25, 420))
        screen.blit(texto2, (25, 440))
        screen.blit(texto3, (25, 460))
        screen.blit(texto4, (25, 480))
        if tempo_decorrido >= 115:
            screen.blit(texto5, (25, 500))

        texto = fonte.render(f'Tempo: {tempo_decorrido}s', True, (255,255,255))
        screen.blit(texto, (30,100))


        #desenho do boss
        if tempo_decorrido >= 120 and derrota == False and vitoria == False:
            draw.rect(screen, (102, 51, 0), (230, 20, 200, 70), border_radius=20)
            sixseven = transform.scale(boss, (25, 50))
            barra_largura_atual = boss_vida * 1.5
            draw.rect(screen, (0, 0, 0), (240, 45, 150, 20), border_radius=20)
            if barra_largura_atual > 0:
                draw.rect(screen, (204, 0, 0), (240, 45, barra_largura_atual, 20), border_radius=20)
            screen.blit(sixseven, (390, 32))

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
            textoDerrota = fonteDerrota.render('WASTED', True, VERMELHO)
            screen.blit(textoDerrota, (200,100))
            draw.rect(screen, (255,255,255), (300,300,150,50), border_radius = 20)
            texto6 = fonte.render('Jogar de novo', True, (0,0,0))
            screen.blit(texto6, (310,310))
    
        #perda de vidas
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

        #fazer a nave ficar atirando
        if atirar == True and derrota == False and vitoria == False:
            if keys[K_j] and tempo_tiro >= intervalo_tiro:
                tempo_tiro = 0
                if direita:
                    lista_tiros.append(
                        Tiro(pos_x + 65, pos_y + 15, True)
                    )
                else:
                    lista_tiros.append(
                        Tiro(pos_x - 15, pos_y + 15, False)
                    )

            tiros_para_remover = []
            for tiro in lista_tiros:
                tiro.atualizar(dt)
                tiro.desenhar(screen)
                if tiro.hitbox.colliderect(head_hitbox1):
                    boss_tomar_dano(1)
                    tiros_para_remover.append(tiro)
                elif tiro.hitbox.colliderect(Head_hitbox2):
                    boss_tomar_dano(1)
                    tiros_para_remover.append(tiro)
                if tiro.fora_da_tela():
                    tiros_para_remover.append(tiro)

            for tiro in tiros_para_remover:
                if tiro in lista_tiros:
                    lista_tiros.remove(tiro)

        #vitória
        if boss_vida <= 0:
            if vitoria == False:
                vitoria = True
                mixer.music.stop()
                musica_fase = ''
                top5.append((nome, tempo_decorrido))
                top5.sort(key=lambda x: x[1], reverse=False)
                top5 = top5[:5]
                try:
                    with open("ranking.txt", "w") as arquivo:
                        for jogador, score in top5:
                            arquivo.write(f"{jogador},{score}\n")                
                except:
                    pass
                vit.play()
            
            pos_x += 0.3 * dt
            if blur < 250:
                blur += 1
            blur_surface.set_alpha(blur) 
            screen.blit(blur_surface, (0, 0))
            if blur >= 250:
                textoVitoria = fonteDerrota.render('MISSION PASSED', True, VERDE)
                screen.blit(textoVitoria, (150,100))
                draw.rect(screen, (255,255,255), (300,300,150,50), border_radius = 20)
                texto_botao = fonte.render('Jogar de novo', True, (0,0,0))
                screen.blit(texto_botao, (310,310))

        if derrota == True or vitoria == True:
            texto_titulo_top = fonte.render('Top 5:', True, (255, 255, 0))
            screen.blit(texto_titulo_top, (550, 200)) 
            
            for i, (jogador, score) in enumerate(top5):
                if jogador == "---":
                    texto_score = fonte.render(f'{i+1}º - ---', True, (200, 200, 200))
                else:
                    texto_score = fonte.render(f'{i+1}º - {jogador} - {score}s', True, (200, 200, 200))
                
                screen.blit(texto_score, (550, 240 + (i * 25)))

    display.update()