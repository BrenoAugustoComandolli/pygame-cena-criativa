import pygame
import sys

# Inicialização do Pygame
pygame.init()

# Configurações da tela
size = (800, 600)
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Simulação de Futebol em Primeira Pessoa")

# Carrega a imagem de fundo
background_image = pygame.image.load('assets/campo.jpg')
background_image = pygame.transform.scale(background_image, (800, 600))

# Carrega imagens do jogador e da bola
player_image = pygame.image.load('assets/jogador.png')  # Supondo uma nova imagem para o jogador
player_image = pygame.transform.scale(player_image, (50, 50))
ball_image = pygame.image.load('assets/bola.png')
ball_image = pygame.transform.scale(ball_image, (30, 30))

collisao_sound = pygame.mixer.Sound("assets/toque_bola.mp3")
gol_sound = pygame.mixer.Sound("assets/comemoracao.mp3")

goal_left = pygame.Rect(0, 200, 30, 200)
goal_right = pygame.Rect(760, 200, 30, 200)

# Posições iniciais
player_pos = [400, 300]
ball_pos = [400, 350]

# Velocidade do jogador e da bola
player_speed = 0.5
ball_speed = [0, 0]

# Atrito
friction = 0.98

# Função para verificar colisões
def check_collision(pos1, pos2, size1, size2):
    return abs(pos1[0] - pos2[0]) < (size1[0] + size2[0]) / 2 and abs(pos1[1] - pos2[1]) < (size1[1] + size2[1]) / 2

# Loop principal
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Movimento do jogador
    keys = pygame.key.get_pressed()
    moving = False
    if keys[pygame.K_LEFT] and player_pos[0] > 25:  # Ajuste para evitar que o jogador saia da imagem
        player_pos[0] -= player_speed
        moving = True
        direction = (-1, 0)
    if keys[pygame.K_RIGHT] and player_pos[0] < 725:  # Ajuste para evitar que o jogador saia da imagem
        player_pos[0] += player_speed
        moving = True
        direction = (1, 0)
    if keys[pygame.K_UP] and player_pos[1] > 25:  # Ajuste para evitar que o jogador saia da imagem
        player_pos[1] -= player_speed
        moving = True
        direction = (0, -1)
    if keys[pygame.K_DOWN] and player_pos[1] < 525:  # Ajuste para evitar que o jogador saia da imagem
        player_pos[1] += player_speed
        moving = True
        direction = (0, 1)

    # Verifica colisão e atualiza a velocidade da bola
    if check_collision(player_pos, ball_pos, (50, 50), (30, 30)) and moving:
        ball_speed = [direction[0] * 1, direction[1] * 1]
        collisao_sound.play()


    # Aplica o atrito para desacelerar a bola
    ball_speed[0] *= friction
    ball_speed[1] *= friction

    # Movimento da bola
    ball_pos[0] += ball_speed[0]
    ball_pos[1] += ball_speed[1]

    # Verifica se a bola entrou em algum dos gols
    ball_rect = pygame.Rect(ball_pos[0], ball_pos[1], 30, 30)
    if goal_left.colliderect(ball_rect) or goal_right.colliderect(ball_rect):
        gol_sound.play()
        font = pygame.font.Font(None, 50)
        text = font.render("Gooooooooool!!!!", True, (255, 255, 255))
        screen.blit(text, (50,50))

    # Impede que a bola saia do campo
    if ball_pos[0] > 770 or ball_pos[0] < 30:
        ball_speed[0] = -ball_speed[0]
        ball_pos[0] = max(min(ball_pos[0], 770), 30)
    if ball_pos[1] > 570 or ball_pos[1] < 30:
        ball_speed[1] = -ball_speed[1]
        ball_pos[1] = max(min(ball_pos[1], 570), 30)

    # Desenha a imagem de fundo
    screen.blit(background_image, [0, 0])
    # Desenha o jogador e a bola
    screen.blit(player_image, player_pos)
    screen.blit(ball_image, ball_pos)

    pygame.display.flip()
