import random 
import pygame
class Team:

    def __init__(self):
        self.characters = [[None] * 3 for _ in range(2)]
        self.x_offset = 0
        self.y_offset = 0

    def add_character(self, character, index, index2):
        if index < 0 or index >= 2:
            if index2 < 0 or index2 >= 3:
                raise IndexError("Index out of range")
        self.characters[index][index2] = (character, 100 + index2 * 120, 100 + index * 80)

    def remove_character(self,character):
        for i in range(2):
            for j in range(3):
                if self.characters[i][j] == character:
                    self.characters[i][j] = None
                    break
        print(character.name + " is dead")
                    
class Game:
                def __init__(self, team1, team2):
                    self.team1 = team1
                    self.team2 = team2
                
                def turn(self,charater,charater2,teamtarget):
                        charater2.hp -= charater.attack()
                        if charater2.hp <= 0:
                                    charater2.hp = 0
                                    teamtarget.remove_character(charater2)
                def search_heal(self,character,teamtarget):
                    lowest_hp = 1
                    lowest_hp_character = None
                    for i in range(2):
                        for j in range(3):
                            characteri = teamtarget.characters[i][j]
                            if characteri is not None:
                                if characteri.hp/characteri.max_hp < lowest_hp:
                                    lowest_hp = characteri.hp/characteri.max_hp
                                    lowest_hp_character = characteri
                    if lowest_hp_character is not None:
                        if lowest_hp_character.hp < lowest_hp_character.max_hp:
                            heal_amount = int(character.attack())
                            lowest_hp_character.hp = min(lowest_hp_character.hp + heal_amount, lowest_hp_character.max_hp)


                def search_attack(self,index,character,teamtarget):
                                
                                for k in range(2):
                                    character2 = teamtarget.characters[k][index]
                                    if character2 is not None:
                                        self.turn(character, character2,teamtarget)
                                        break  
                                    if index+1 < 3 :
                                        if teamtarget.characters[k][index+1] is not None:
                                            character2 = teamtarget.characters[k][index+1]
                                            self.turn(character, character2,teamtarget)
                                            break 
                                    if index-1 >= 0 :
                                        if teamtarget.characters[k][index-1] is not None:
                                            character2 = teamtarget.characters[k][index-1]
                                            self.turn(character, character2,teamtarget)
                                            break  # Exit the loop when an attack occurs

                                    if index+2 <= 2 : 
                                        if teamtarget.characters[k][index+2] is not None:
                                            character2 = teamtarget.characters[k][index+2]
                                            self.turn(character, character2,teamtarget)
                                            break  # Exit the loop when an attack occurs
                                        
                                    if index-2 >= 0:
                                        
                                        if teamtarget.characters[k][index-2] is not None:
                                            character2 = teamtarget.characters[k][index-2]
                                            self.turn(character, character2,teamtarget)
                                            break  # Exit the loop when an attack occurs
                                    
                                    
                def play(self):
                        for i in range(2):
                            for j in range(3):
                                character = self.team1.characters[i][j]
                                character2 = self.team2.characters[i][j]
                                if character is not None and character2 is not None:
                                    if character.velocity > character2.velocity:
                                        if character.class_name != "Healer":
                                            self.search_attack(j,character,self.team2)
                                        elif character.class_name == "Healer":
                                            self.search_heal(character,self.team1)
                                        if character2.class_name != "Healer":
                                            self.search_attack(j,character2,self.team1)
                                        elif character2.class_name == "Healer":
                                            self.search_heal(character2,self.team2)
                                    else:
                                        if character2.class_name != "Healer":
                                            self.search_attack(j,character2,self.team1)
                                        elif character2.class_name == "Healer":
                                            self.search_heal(character2,self.team2)
                                        if character.class_name != "Healer":
                                            self.search_attack(j,character,self.team2)
                                        elif character.class_name == "Healer":
                                            self.search_heal(character,self.team1)
                                if character is not None and character2 is None:
                                    if character.class_name != "Healer":
                                        self.search_attack(j,character,self.team2)
                                    elif character.class_name == "Healer":
                                        self.search_heal(character,self.team1)
                                if character2 is not None and character is None:
                                    if character2.class_name != "Healer":
                                        self.search_attack(j,character2,self.team1)
                                    elif character2.class_name == "Healer":
                                        self.search_heal(character2,self.team2)
                                    
                                    
                  
class Character:
            def __init__(self, name,class_name):
                self.class_name = class_name
                self.name = name
                self.attacks = 0
                self.special_attack = False
                self.skills = []

                if class_name == "Damage":
                    self.damage = 40 + random.randint(1, 10)
                    self.hp = 50
                    self.max_hp = 100
                    self.velocity = random.randint(1, 10)
                elif class_name == "Healer":
                    self.damage = 5 + random.randint(1, 5)
                    self.hp = 200
                    self.max_hp = 200
                    self.velocity = random.randint(1, 5)
                elif class_name == "Tank":
                    self.damage = 2 + random.randint(1, 2)
                    self.hp = 100
                    self.max_hp = 100
                    self.velocity = random.randint(1, 3)
                    

            def attack(self):
                damage = self.damage
                self.attacks += 1
                if self.attacks % 2 == 0:
                    self.special_attack = True
                else:
                    self.special_attack = False
                if self.special_attack:
                    damage *= 2
                return damage
            def draw(self, screen,x,y):
                font = pygame.font.Font(None, 36)
                text = font.render(self.name, True, (255, 255, 255))
                text_rect = text.get_rect()
                text_rect.center = (x, y - 20)
                screen.blit(text, text_rect)
                pygame.draw.rect(screen, (0, 255, 0), (x - 10, y - 50, self.max_hp, 10))
                pygame.draw.rect(screen, (255, 0, 0), (x - 10, y - 50, self.hp, 10))







