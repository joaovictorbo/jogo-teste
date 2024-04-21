import pygame
import sys
from team import Team, Character, Game
import time 

character1 = Character("Renan","Damage")
character12 = Character("Renan2","Damage")
character13 = Character("Renan3","Damage")
character2 = Character("Pedro","Healer")
character22 = Character("Pedro2","Healer")
character23 = Character("Pedro3","Healer")
character3 = Character("Danta1","Tank")
character4 = Character("Danta2","Tank")
team1 = Team()
team2 = Team()
team1.add_character(character1,0,2,0)
team1.add_character(character12,0,1,0)
team1.add_character(character13,1,2,0)
team2.add_character(character3,0,0,1)
team2.add_character(character4,0,2,1)
team2.add_character(character2,1,0,1)
team2.add_character(character22,1,2,1)
team2.add_character(character23,1,1,1)
game = Game(team1,team2)

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
                if team1.characters[i][j][0] is not None:
                    team1.characters[i][j][0].draw(screen,team1.characters[i][j][1],team1.characters[i][j][2])
    for i in range(2):
        for j in range(3):
            if team2.characters[i][j] is not None:
                if team2.characters[i][j][0] is not None:
                    team2.characters[i][j][0].draw(screen,team2.characters[i][j][1],team2.characters[i][j][2]+300) 
    pygame.display.flip()
    game.play()
    time.sleep(1)