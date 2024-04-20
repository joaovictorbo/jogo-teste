import pygame
import sys
from team import Team, Character, Game

character1 = Character("Renan","Damage")
character2 = Character("Pedro","Healer")
team1 = Team()
team2 = Team()
team1.add_character(character1,0,0)
team1.add_character(character2,0,1)
team2.add_character(character1,0,0)
team2.add_character(character2,0,1)

# Inicialização do Pygame
pygame.init()
largura = 800
altura = 600
screen = pygame.display.set_mode((largura, altura))
pygame.display.set_caption("Meu Jogo")


# Loop principal do jogo
while True:
    # Verificar eventos
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    # Atualizar a tela
    screen.fill((0, 0, 0))
    for i in range(2):
        for j in range(3):
            if team1.characters[i][j] is not None:
                team1.characters[i][j][0].draw(screen,team1.characters[i][j][1],team1.characters[i][j][2])
    for i in range(2):
        for j in range(3):
            if team2.characters[i][j] is not None:
                team2.characters[i][j][0].draw(screen,team2.characters[i][j][1],team2.characters[i][j][2]+400)
    
    pygame.display.flip()