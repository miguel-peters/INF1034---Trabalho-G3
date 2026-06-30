import pygame

pygame.init()
tela = pygame.display.set_mode((800, 600))
relogio = pygame.time.Clock()

# Variável que controla a tela atual
estado_jogo = "MENU"

rodando = True
while rodando:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            rodando = False
        # Se estiver no menu e pressionar espaço, vai para o jogo
        if estado_jogo == "MENU" and evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_SPACE:
                estado_jogo = "JOGO"

    tela.fill((0, 0, 0)) # Limpa a tela

    if estado_jogo == "MENU":
        # Desenhar elementos do menu aqui
        pass
    elif estado_jogo == "JOGO":
        # Desenhar elementos do jogo aqui
        pass

    pygame.display.flip()
    relogio.tick(60)

pygame.quit()
