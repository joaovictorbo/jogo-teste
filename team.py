import random
import pygame

class Team:
    def __init__(self):
        # Matrizes 2x3 com None
        self.characters = [[None] * 3 for _ in range(2)]
        self.x_offset = 0
        self.y_offset = 0

    def add_character(self, character, index, index2, team):
        if index < 0 or index >= 2:
            if index2 < 0 or index2 >= 3:
                raise IndexError("Index out of range")
        if team == 0:
            # Time 1
            self.characters[index][index2] = (character, 100 + index2 * 120, 200 - index * 80)
        else:
            # Time 2
            self.characters[index][index2] = (character, 100 + index2 * 120, 200 + index * 80)

    def remove_character(self, character):
        for i in range(2):
            for j in range(3):
                if self.characters[i][j] is not None:
                    if self.characters[i][j][0] == character:
                        # Remove apenas esse personagem, mas mantém a posição
                        self.characters[i][j] = (None, self.characters[i][j][1], self.characters[i][j][2])
                        break

class Game:
    def __init__(self, team1, team2, screen):
        self.team1 = team1
        self.team2 = team2
        self.screen = screen

    def turn(self, charater, charater2, teamtarget):
        print(charater.name + " attacks " + charater2.name)
        charater2.hp -= charater.attack()
        if charater2.hp <= 0:
            charater2.hp = 0
            teamtarget.remove_character(charater2)

    def search_heal(self, character, teamtarget):
        lowest_hp = 1
        lowest_hp_character = None
        # Procura no teamtarget quem está com a menor % de vida
        for i in range(2):
            for j in range(3):
                slot = teamtarget.characters[i][j]
                if slot is not None and slot[0] is not None:
                    characteri = slot[0]
                    if characteri.hp / characteri.max_hp < lowest_hp:
                        lowest_hp = characteri.hp / characteri.max_hp
                        lowest_hp_character = characteri

        # Se encontrou alguém para curar, faz a cura
        if lowest_hp_character is not None:
            if lowest_hp_character.hp < lowest_hp_character.max_hp:
                heal_amount = int(character.attack())
                print(character.name + " heals " + lowest_hp_character.name + " in " + str(heal_amount) + " HP")
                lowest_hp_character.hp = min(lowest_hp_character.hp + heal_amount, 
                                             lowest_hp_character.max_hp)

    def search_attack(self, index, character, teamtarget):
        """
        Tenta atacar o inimigo em (k, index).
        Se estiver vazio, procura index +/- 1, +/- 2, etc.
        Antes de aplicar o dano, roda a animação (animate_attack).
        """
        # 1) Posição do atacante (para a animação)
        attacker_x, attacker_y = self.find_character_position(character, self.team1)
        # Se não estiver no team1, pode estar no team2
        if attacker_x is None:
            attacker_x, attacker_y = self.find_character_position(character, self.team2)
            # Caso seja mesmo do time2, some 300 no Y (pois é onde desenhamos)
            if attacker_x is not None:
                attacker_y += 300

        # 2) Tenta atacar no time alvo
        for k in range(2):
            char_slot = teamtarget.characters[k][index]
            if char_slot is not None and char_slot[0] is not None:
                # Achamos um alvo direto
                target = char_slot[0]
                target_x, target_y = char_slot[1], char_slot[2]
                if teamtarget == self.team2:
                    target_y += 300  # Ajuste do Y para time 2
                # Anima
                self.animate_attack(attacker_x, attacker_y, target_x, target_y)
                # Aplica o ataque
                self.turn(character, target, teamtarget)
                self.show(char_slot[1], char_slot[2] + (300 if teamtarget == self.team2 else 0))
                break

            # Se não encontrou nesse index, tenta o index +1, -1, +2, -2
            if index + 1 < 3:
                if teamtarget.characters[k][index+1] is not None and teamtarget.characters[k][index+1][0]:
                    target_slot = teamtarget.characters[k][index+1]
                    target = target_slot[0]
                    target_x, target_y = target_slot[1], target_slot[2]
                    if teamtarget == self.team2:
                        target_y += 300
                    self.animate_attack(attacker_x, attacker_y, target_x, target_y)
                    self.turn(character, target, teamtarget)
                    break

            if index - 1 >= 0:
                if teamtarget.characters[k][index-1] is not None and teamtarget.characters[k][index-1][0]:
                    target_slot = teamtarget.characters[k][index-1]
                    target = target_slot[0]
                    target_x, target_y = target_slot[1], target_slot[2]
                    if teamtarget == self.team2:
                        target_y += 300
                    self.animate_attack(attacker_x, attacker_y, target_x, target_y)
                    self.turn(character, target, teamtarget)
                    break

            if index + 2 <= 2:
                if teamtarget.characters[k][index+2] is not None and teamtarget.characters[k][index+2][0]:
                    target_slot = teamtarget.characters[k][index+2]
                    target = target_slot[0]
                    target_x, target_y = target_slot[1], target_slot[2]
                    if teamtarget == self.team2:
                        target_y += 300
                    self.animate_attack(attacker_x, attacker_y, target_x, target_y)
                    self.turn(character, target, teamtarget)
                    break

            if index - 2 >= 0:
                if teamtarget.characters[k][index-2] is not None and teamtarget.characters[k][index-2][0]:
                    target_slot = teamtarget.characters[k][index-2]
                    target = target_slot[0]
                    target_x, target_y = target_slot[1], target_slot[2]
                    if teamtarget == self.team2:
                        target_y += 300
                    self.animate_attack(attacker_x, attacker_y, target_x, target_y)
                    self.turn(character, target, teamtarget)
                    break

    def find_character_position(self, character, team):
        """
        Retorna (x, y) se encontrar o 'character' dentro de 'team'.
        Caso não encontre, retorna (None, None).
        """
        for i in range(2):
            for j in range(3):
                if team.characters[i][j] is not None:
                    if team.characters[i][j][0] == character:
                        # Retorna X, Y
                        return team.characters[i][j][1], team.characters[i][j][2]
        return None, None

    def animate_attack(self, attacker_x, attacker_y, target_x, target_y):
        """
        Anima um pequeno 'projétil' indo de (attacker_x, attacker_y)
        até (target_x, target_y).
        """
        steps = 20  # Quantidade de 'frames' na animação
        for step in range(steps):
            # 1) Limpa a tela
            self.screen.fill((0, 0, 0))

            # 2) Redesenha todos do time1
            for i in range(2):
                for j in range(3):
                    if self.team1.characters[i][j] is not None:
                        if self.team1.characters[i][j][0] is not None:
                            char_obj, x_pos, y_pos = self.team1.characters[i][j]
                            char_obj.draw(self.screen, x_pos, y_pos)

            # 3) Redesenha todos do time2 (com +300 em y)
            for i in range(2):
                for j in range(3):
                    if self.team2.characters[i][j] is not None:
                        if self.team2.characters[i][j][0] is not None:
                            char_obj, x_pos, y_pos = self.team2.characters[i][j]
                            char_obj.draw(self.screen, x_pos, y_pos + 300)

            # 4) Calcula a interpolação (0 → 1)
            t = step / float(steps - 1)
            current_x = attacker_x + t * (target_x - attacker_x)
            current_y = attacker_y + t * (target_y - attacker_y)

            # 5) Desenha o projétil (um círculo branco de raio 5)
            pygame.draw.circle(self.screen, (255, 255, 255), (int(current_x), int(current_y)), 5)

            # 6) Atualiza a tela e faz uma pequena pausa
            pygame.display.flip()
            pygame.time.delay(50)

    def show(self, x, y):
        font = pygame.font.Font(None, 36)
        text = font.render("POW", True, (255, 255, 255))
        text_rect = text.get_rect()
        text_rect.center = (x, y - 40)
        self.screen.blit(text, text_rect)
        pygame.display.flip()
        pygame.time.wait(500)

    def play(self):
        """
        Realiza a lógica de turno para cada 'slot' (i, j).
        Se houver alguém nos dois times, eles se atacam dependendo da velocidade.
        """
        for i in range(2):
            for j in range(3):
                char1_slot = self.team1.characters[i][j]
                char2_slot = self.team2.characters[i][j]

                character = char1_slot[0] if char1_slot is not None else None
                character2 = char2_slot[0] if char2_slot is not None else None

                # Se ambos existem
                if character is not None and character2 is not None:
                    if character.velocity > character2.velocity:
                        # time1 ataca primeiro
                        if character.class_name != "Healer":
                            self.search_attack(j, character, self.team2)
                        else:
                            self.search_heal(character, self.team1)

                        # depois time2
                        if character2.class_name != "Healer":
                            self.search_attack(j, character2, self.team1)
                        else:
                            self.search_heal(character2, self.team2)

                    else:
                        # time2 ataca primeiro
                        if character2.class_name != "Healer":
                            self.search_attack(j, character2, self.team1)
                        else:
                            self.search_heal(character2, self.team2)

                        # depois time1
                        if character.class_name != "Healer":
                            self.search_attack(j, character, self.team2)
                        else:
                            self.search_heal(character, self.team1)

                # Se só existe o time1
                elif character is not None and character2 is None:
                    if character.class_name != "Healer":
                        self.search_attack(j, character, self.team2)
                    else:
                        self.search_heal(character, self.team1)

                # Se só existe o time2
                elif character2 is not None and character is None:
                    if character2.class_name != "Healer":
                        self.search_attack(j, character2, self.team1)
                    else:
                        self.search_heal(character2, self.team2)

class Character:
    def __init__(self, name, class_name):
        self.class_name = class_name
        self.name = name
        self.attacks = 0
        self.special_attack = False
        self.skills = []

        if class_name == "Damage":
            self.damage = 20 + random.randint(1, 10)
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
            self.hp = 200
            self.max_hp = 200
            self.velocity = random.randint(1, 3)

    def attack(self):
        """
        Retorna o dano do personagem. A cada 2 ataques, 
        o 'special_attack' dobra o dano (damage *= 2).
        """
        damage = self.damage
        self.attacks += 1
        if self.attacks % 2 == 0:
            self.special_attack = True
        else:
            self.special_attack = False

        if self.special_attack:
            damage *= 2
        return damage

    def draw(self, screen, x, y):
        """
        Desenha o personagem na posição (x, y), 
        com sua barra de vida e nome.
        """
        font = pygame.font.Font(None, 36)
        text = font.render(self.name, True, (255, 255, 255))
        text_rect = text.get_rect()
        text_rect.center = (x, y - 20)
        screen.blit(text, text_rect)

        # Desenha barra de vida (vermelha e verde)
        pygame.draw.rect(screen, (255, 0, 0), 
                         (x - 40, y - 50, 80, 10))
        life_width = int((self.hp / self.max_hp) * 80)
        pygame.draw.rect(screen, (0, 255, 0), 
                         (x - 40, y - 50, life_width, 10))

        # Se quiser, tire esse flip daqui para evitar renders parciais
        pygame.display.flip()