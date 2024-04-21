import random 
import pygame
class Team:

    def __init__(self):
        self.characters = [[None] * 3 for _ in range(2)]
        self.x_offset = 0
        self.y_offset = 0

    def add_character(self, character, index, index2,team):
        if index < 0 or index >= 2:
            if index2 < 0 or index2 >= 3:
                raise IndexError("Index out of range")
        if team == 0:
            self.characters[index][index2] = (character, 100 + index2 * 120, 200 - index * 80)
        else:
            self.characters[index][index2] = (character, 100 + index2 * 120, 200 + index * 80)

    def remove_character(self,character):
        for i in range(2):
            for j in range(3):
                if self.characters[i][j] is not None:
                    if self.characters[i][j][0] == character:
                        self.characters[i][j] = (None, self.characters[i][j][1], self.characters[i][j][2])
                        break
                    
class Game:
                def __init__(self, team1, team2):
                    self.team1 = team1
                    self.team2 = team2
                
                def turn(self,charater,charater2,teamtarget):
                    print(charater.name + " attacks " + charater2.name)
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
                                if characteri[0] is not None:
                                    characteri = characteri[0]
                                    if characteri.hp/characteri.max_hp < lowest_hp:
                                        lowest_hp = characteri.hp/characteri.max_hp
                                        lowest_hp_character = characteri
                    if lowest_hp_character is not None:
                        if lowest_hp_character.hp < lowest_hp_character.max_hp:
                            heal_amount = int(character.attack())
                            print(character.name + " heals " + lowest_hp_character.name + " in " + str(heal_amount) + " HP")
                            lowest_hp_character.hp = min(lowest_hp_character.hp + heal_amount, lowest_hp_character.max_hp)


                def search_attack(self,index,character,teamtarget):
                                
                                for k in range(2):
                                    character2 = teamtarget.characters[k][index]
                                    if character2 is not None and character2[0] is not None:
                                        self.turn(character, character2[0],teamtarget)
                                        break  
                                    if index+1 < 3 :
                                        if teamtarget.characters[k][index+1] is not None and teamtarget.characters[k][index+1][0]:
                                            character2 = teamtarget.characters[k][index+1]
                                            self.turn(character, character2[0],teamtarget)
                                            break 
                                    if index-1 >= 0 :
                                        if teamtarget.characters[k][index-1] is not None and teamtarget.characters[k][index-1][0]:
                                            character2 = teamtarget.characters[k][index-1]
                                            self.turn(character, character2[0],teamtarget)
                                            break  # Exit the loop when an attack occurs

                                    if index+2 <= 2 : 
                                        if teamtarget.characters[k][index+2] is not None and teamtarget.characters[k][index+2][0]:
                                            character2 = teamtarget.characters[k][index+2]
                                            self.turn(character, character2[0],teamtarget)
                                            break  # Exit the loop when an attack occurs
                                        
                                    if index-2 >= 0:
                                        
                                        if teamtarget.characters[k][index-2] is not None and teamtarget.characters[k][index-2][0]:
                                            character2 = teamtarget.characters[k][index-2]
                                            self.turn(character, character2[0],teamtarget)
                                            break  # Exit the loop when an attack occurs
                                    
                                    
                def play(self):
                        for i in range(2):
                            for j in range(3):
                                character = self.team1.characters[i][j]
                                character2 = self.team2.characters[i][j]
                                character2 = character2[0] if character2 is not None else None
                                character = character[0] if character is not None else None
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
                    self.damage = 10 + random.randint(1, 10)
                    self.hp = 80
                    self.max_hp = 80
                    self.velocity = random.randint(1, 10)
                elif class_name == "Healer":
                    self.damage = 5 + random.randint(1, 5)
                    self.hp = 40
                    self.max_hp = 40
                    self.velocity = random.randint(1, 5)
                elif class_name == "Tank":
                    self.damage = 5 + random.randint(1, 2)
                    self.hp = 300
                    self.max_hp = 300
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
                pygame.draw.rect(screen, (255, 0, 0), (x - 40, y - 50, (self.max_hp/self.max_hp)*80, 10))
                pygame.draw.rect(screen, (0, 255, 0), (x - 40, y - 50, (self.hp/self.max_hp)*80, 10))







