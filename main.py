import pygame
import sys
from team import Team, Character, Game
import time 

character1 = Character("Renan","Damage")
character4 = Character("Danta2","Tank")
character3 = Character("Danta","Healer")
character2 = Character("Renan2","Damage")
character5 = Character("Renan3","Tank")
character6 = Character("Renan4","Healer")
character7 = Character("Renan5","Damage")
team1 = Team()
team2 = Team()
team1.add_character(character5,0,2,0)
team1.add_character(character1,1,2,0)
team2.add_character(character4,0,2,1)
team2.add_character(character3,1,0,1)
team2.add_character(character2,1,1,1)
team1.add_character(character6,0,0,0)
team2.add_character(character7,1,1,0)

# Inicialização do Pygame
pygame.init()
largura = 800
altura = 600
screen = pygame.display.set_mode((largura, altura))
pygame.display.set_caption("Meu Jogo")
game = Game(team1,team2,screen)


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
    game.play()
    pygame.time.delay(200)
    pygame.display.flip()