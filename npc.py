import sys
import os
from pygame import *
import pygame
import pyganim
from setting import *
from battle import *


def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


dialog_spritesheet = pygame.image.load(resource_path("resources/system/sprites/222761daf9ee36c.png"))
dialog_image = pygame.transform.scale(dialog_spritesheet, (750, 230))

dialogue_box = pygame.Surface([750, 230], pygame.SRCALPHA)

sans_sound = pygame.mixer.Sound(resource_path("resources/sound/voice_sans.mp3"))
vaqif_sound = pygame.mixer.Sound(resource_path("resources/sound/vaqif.mp3"))


class Dialogue(pygame.sprite.Sprite):
    def __init__(self, *args):
        super(Dialogue, self).__init__()
        self.type_system = "dialog"
        self.image = Surface([750, 230], pygame.SRCALPHA)
        self.rect = Rect(265, 480, 750, 230)
        self.text = None
        self.text2 = None
        self.text3 = None
        self.text4 = None
        self.index = 0

    def text_set(self, text, text2, text3, text4):
        self.text = text
        self.text2 = text2
        self.text3 = text3
        self.text4 = text4

    def update(self, screen, *args):
        self.image.blit(dialog_image, (0, 0))
        self.image.blit(self.text, (40, 30))
        self.image.blit(self.text2, (40, 65))
        self.image.blit(self.text3, (40, 100))
        self.image.blit(self.text4, (40, 135))
        screen.blit(self.image, (250, 500))

    def end(self):
        self.image.fill((0, 0, 0))


class NPC(pygame.sprite.Sprite):
    def __init__(self, action_data, id_npc, x, y, start_dir, start_time_delay, text, *questions):
        # action_data :if 'talk': ["type_of_action"]
        # action_data :if 'battle_with_selection': ["type_of_action", opponent_team]
        # action_data :if 'battle': ["type_of_action", opponent_team]
        super(NPC, self).__init__()
        self.animation_on = None  # component for moving function
        self.count = 0  # component for moving function
        self.type = "npc"

        self.move = False  # setting npc movement (it will be just stay or move)

        self.action = True  # setting action mechanic
        self.action_on = False  # setting action mechanic
        self.dialogue = None
        self.dialogue_create = True  # setting action mechanic

        # setting, would be npc talk or no
        if action_data[0] == "battle":
            self.talking = False
        else:
            self.talking = True

        self.action_data = action_data[:]

        self.default_text = text.copy()
        self.text_content = text[0].split("|")
        self.text_content2 = text[1].split("|")
        self.text_content3 = text[2].split("|")
        self.text_content4 = text[3].split("|")
        self.text = ""  # our text
        self.text2 = ""  # our text
        self.text3 = ""  # our text
        self.text4 = ""  # our text
        self.color1 = (0, 0, 0)  # color text (default)
        self.color2 = (0, 0, 0)  # color text (default)
        self.color3 = (0, 0, 0)  # color text (default)
        self.color4 = (0, 0, 0)  # color text (default)
        self.letter_index = 0  # setting, would be npc talk or no
        self.letter_index2 = 0  # setting, would be npc talk or no
        self.letter_index3 = 0  # setting, would be npc talk or no
        self.letter_index4 = 0  # setting, would be npc talk or no
        self.text_index = 0  # setting index of text_content
        self.delay_text = 5  # delay between text (dialog) change
        self.change = False  # setting action mechanic

        self.up_answer = False  # setting action mechanic
        self.down_answer = False  # setting action mechanic
        self.change_with_active = False  # setting action mechanic
        self.fps_answer_delay = 3  # setting action mechanic

        self.questions = []
        self.index_of_answers = 0
        self.color_not_active = (210, 204, 22)
        self.color_active = (210, 148, 22)
        self.answer = 2  # default answer index
        for question in questions:
            self.questions.append(question)

        self.index_of_move = -1  # start index for directions and times
        self.time_delay = start_time_delay  # start time delay
        self.current_direction = None  # component for getting current direction
        self.speed_of_player = None  # component for setting static player speed (its will need be /32 for right cords)
        self.static_count = None  # component for static count (its will need be /32 for right cords)
        self.speed_of_count = None  # component for speed count (its will need be /32 for right cords)
        self.directions = []  # direction of npc
        self.times = []  # time (delays) between moving

        npc_spritesheet = pygame.image.load(resource_path(f"resources/img/npc/{id_npc}.png"))  # import npc sprite image

        self.npc_up_0 = pygame.Surface([32, 48], pygame.SRCALPHA)
        self.npc_up_0.blit(npc_spritesheet, (0, 0), [80, 16, 32, 48])
        self.npc_up_1 = pygame.Surface([32, 48], pygame.SRCALPHA)
        self.npc_up_1.blit(npc_spritesheet, (0, 0), [16, 16, 32, 48])
        self.npc_up_2 = pygame.Surface([32, 48], pygame.SRCALPHA)
        self.npc_up_2.blit(npc_spritesheet, (0, 0), [80, 16, 32, 48])
        self.npc_up_3 = pygame.Surface([32, 48], pygame.SRCALPHA)
        self.npc_up_3.blit(npc_spritesheet, (0, 0), [144, 16, 32, 48])
        self.npc_right_0 = pygame.Surface([32, 48], pygame.SRCALPHA)
        self.npc_right_0.blit(npc_spritesheet, (0, 0), [80, 80, 32, 48])
        self.npc_right_1 = pygame.Surface([32, 48], pygame.SRCALPHA)
        self.npc_right_1.blit(npc_spritesheet, (0, 0), [16, 80, 32, 48])
        self.npc_right_2 = pygame.Surface([32, 48], pygame.SRCALPHA)
        self.npc_right_2.blit(npc_spritesheet, (0, 0), [80, 80, 32, 48])
        self.npc_right_3 = pygame.Surface([32, 48], pygame.SRCALPHA)
        self.npc_right_3.blit(npc_spritesheet, (0, 0), [144, 80, 32, 48])
        self.npc_down_0 = pygame.Surface([32, 48], pygame.SRCALPHA)
        self.npc_down_0.blit(npc_spritesheet, (0, 0), [80, 144, 32, 48])
        self.npc_down_1 = pygame.Surface([32, 48], pygame.SRCALPHA)
        self.npc_down_1.blit(npc_spritesheet, (0, 0), [16, 144, 32, 48])
        self.npc_down_2 = pygame.Surface([32, 48], pygame.SRCALPHA)
        self.npc_down_2.blit(npc_spritesheet, (0, 0), [80, 144, 32, 48])
        self.npc_down_3 = pygame.Surface([32, 48], pygame.SRCALPHA)
        self.npc_down_3.blit(npc_spritesheet, (0, 0), [144, 144, 32, 48])
        self.npc_left_0 = pygame.Surface([32, 48], pygame.SRCALPHA)
        self.npc_left_0.blit(npc_spritesheet, (0, 0), [80, 208, 32, 48])
        self.npc_left_1 = pygame.Surface([32, 48], pygame.SRCALPHA)
        self.npc_left_1.blit(npc_spritesheet, (0, 0), [16, 208, 32, 48])
        self.npc_left_2 = pygame.Surface([32, 48], pygame.SRCALPHA)
        self.npc_left_2.blit(npc_spritesheet, (0, 0), [80, 208, 32, 48])
        self.npc_left_3 = pygame.Surface([32, 48], pygame.SRCALPHA)
        self.npc_left_3.blit(npc_spritesheet, (0, 0), [144, 208, 32, 48])

        # setting player's animation
        self.NPC_ANIMATION_RIGHT = pyganim.PygAnimation([
            (self.npc_right_1, 0.2),
            (self.npc_right_2, 0.2),
            (self.npc_right_3, 0.2),
            (self.npc_right_0, 0.2)])
        self.NPC_ANIMATION_LEFT = pyganim.PygAnimation([
            (self.npc_left_1, 0.2),
            (self.npc_left_2, 0.2),
            (self.npc_left_3, 0.2),
            (self.npc_left_0, 0.2)])
        self.NPC_ANIMATION_UP = pyganim.PygAnimation([
            (self.npc_up_1, 0.2),
            (self.npc_up_2, 0.2),
            (self.npc_up_3, 0.2),
            (self.npc_up_0, 0.2)])
        self.NPC_ANIMATION_DOWN = pyganim.PygAnimation([
            (self.npc_down_1, 0.2),
            (self.npc_down_2, 0.2),
            (self.npc_down_3, 0.2),
            (self.npc_down_0, 0.2)])

        self.image = Surface([32, 48], pygame.SRCALPHA)  # our player Surface
        if start_dir == "r":
            self.image.blit(self.npc_right_0, (0, 0))
        elif start_dir == "l":
            self.image.blit(self.npc_left_0, (0, 0))
        elif start_dir == "d":
            self.image.blit(self.npc_down_0, (0, 0))
        elif start_dir == "u":
            self.image.blit(self.npc_up_0, (0, 0))

        # setting rect and coordinates of player
        self.rect = Rect(x, y - 16, 32, 48)
        self.cord_of_npc = [self.rect.x, self.rect.y + 16]
        self.right_cord_of_item = [self.rect.x + 32, self.rect.y + 32]
        self.left_cord_of_item = [self.rect.x, self.rect.y + 32]
        self.up_cord_of_item = [self.rect.x + 16, self.rect.y + 16]
        self.down_cord_of_item = [self.rect.x + 16, self.rect.y + 48]
        self.center_cord_of_item = [self.rect.x + 16, self.rect.y + 32]

        self.xvel = 0  # x-coordinate speed
        self.yvel = 0  # y-coordinate speed

    def set_default_text_content(self):
        self.text_content = self.default_text[0].split("|")
        self.text_content2 = self.default_text[1].split("|")
        self.text_content3 = self.default_text[2].split("|")
        self.text_content4 = self.default_text[3].split("|")

    def movement(self, count_static, speed_of_count, speed_of_player, *args):
        self.static_count = count_static  # component for static count (its will need be /32 for right cords)
        self.speed_of_player = speed_of_player  # component for setting static player speed
        self.speed_of_count = speed_of_count  # component for speed count (its will need be /32 for right cords)

        for i in args:  # setting args
            if isinstance(i, str):  # if "str" => 'direction' type
                self.directions.append(i)
            elif isinstance(i, int):  # if "num" => 'time' type
                self.times.append(i)
        self.current_direction = self.directions[0]

        self.move = True  # its mean , that npc would moving on map

    def update(self, player, screen, *args):
        font_of_npc = args[0]
        system_mech = args[1]
        settings = args[2]
        screen.blit(self.image, (self.rect.x, self.rect.y))
        if self.animation_on:  # if animation is ON (player moving == True)
            if self.count != 0:  # if animation is continuing
                if self.current_direction == "l":
                    self.image.fill((0, 0, 0, 0))  # clear image mechanism
                    self.NPC_ANIMATION_LEFT.play()
                    self.NPC_ANIMATION_LEFT.blit(self.image, (0, 0))  # npc animation
                    self.count -= self.speed_of_count
                    self.rect.x = self.rect.x - self.speed_of_player  # changing cords of npc
                if self.current_direction == "r":
                    self.image.fill((0, 0, 0, 0))
                    self.NPC_ANIMATION_RIGHT.play()
                    self.NPC_ANIMATION_RIGHT.blit(self.image, (0, 0))
                    self.count -= self.speed_of_count
                    self.rect.x = self.rect.x + self.speed_of_player
                if self.current_direction == "u":
                    self.image.fill((0, 0, 0, 0))
                    self.NPC_ANIMATION_UP.play()
                    self.NPC_ANIMATION_UP.blit(self.image, (0, 0))
                    self.count -= self.speed_of_count
                    self.rect.y = self.rect.y - self.speed_of_player
                if self.current_direction == "d":
                    self.image.fill((0, 0, 0, 0))
                    self.NPC_ANIMATION_DOWN.play()
                    self.NPC_ANIMATION_DOWN.blit(self.image, (0, 0))
                    self.count -= self.speed_of_count
                    self.rect.y = self.rect.y + self.speed_of_player
            else:
                self.animation_on = False  # stop player moving

                # setting rect and coordinates of player
                self.cord_of_npc = [self.rect.x, self.rect.y + 16]
                self.right_cord_of_item = [self.rect.x + 32, self.rect.y + 32]
                self.left_cord_of_item = [self.rect.x, self.rect.y + 32]
                self.up_cord_of_item = [self.rect.x + 16, self.rect.y + 16]
                self.down_cord_of_item = [self.rect.x + 16, self.rect.y + 48]
                self.center_cord_of_item = [self.rect.x + 16, self.rect.y + 32]

                # stop anim npc (func)
                self.NPC_ANIMATION_DOWN.stop()
                self.NPC_ANIMATION_UP.stop()
                self.NPC_ANIMATION_RIGHT.stop()
                self.NPC_ANIMATION_LEFT.stop()

        if self.move:
            index = self.index_of_move + 1  # index value for checking collide with player
            if index >= len(self.directions):
                index = 0
            if self.time_delay != 0:  # checking waiting time
                self.time_delay = self.time_delay - 1
            elif (player.right_cord_of_player == self.left_cord_of_item) and self.directions[index] == "l":
                pass
            elif (player.left_cord_of_player == self.right_cord_of_item) and self.directions[index] == "r":
                pass
            elif (player.up_cord_of_player == self.down_cord_of_item) and self.directions[index] == "d":
                pass
            elif (player.down_cord_of_player == self.up_cord_of_item) and self.directions[index] == "u":
                pass
            else:
                if not self.animation_on:
                    self.count = self.static_count  # setting count (time) of moving
                    self.animation_on = True  # start animation (and moving) npc

                    self.index_of_move += 1  # change direction and delay index
                    if self.index_of_move >= len(self.directions):
                        self.index_of_move = 0
                    self.time_delay = self.times[self.index_of_move]  # setting new time (delay)
                    self.current_direction = self.directions[self.index_of_move]  # setting new direction

        if self.action:
            if self.action_on:
                if self.talking:
                    # try to create dialog
                    if self.dialogue_create:
                        settings.world_status_changer("DIALOG")
                        self.dialogue = Dialogue()
                        system_mech.add(self.dialogue)
                        if player.last_move == "left":
                            self.image.fill((255, 255, 255, 0))  # clear image with transparent color for next animation
                            self.image.blit(self.npc_right_0, (0, 0))
                        elif player.last_move == "right":
                            self.image.fill((255, 255, 255, 0))
                            self.image.blit(self.npc_left_0, (0, 0))
                        elif player.last_move == "up":
                            self.image.fill((255, 255, 255, 0))
                            self.image.blit(self.npc_down_0, (0, 0))
                        elif player.last_move == "down":
                            self.image.fill((255, 255, 255, 0))
                            self.image.blit(self.npc_up_0, (0, 0))
                        self.dialogue_create = False
                    # if dialog already is existed
                    try:
                        for q in self.questions:
                            if q["index"] == self.text_index:
                                settings.world_status_changer("DIALOG_ANSWER")
                                if self.index_of_answers != q["answer_count"]:
                                    for i in q["answer"]:
                                        if self.index_of_answers == 0:
                                            self.color2 = self.color_active
                                            self.text2 += i
                                        elif self.index_of_answers == 1:
                                            self.color3 = self.color_not_active
                                            self.text3 += i
                                        elif self.index_of_answers == 2:
                                            self.color4 = self.color_not_active
                                            self.text4 += i

                                        self.index_of_answers += 1

                        if self.letter_index != len(self.text_content[self.text_index]):
                            sans_sound.play()
                            self.text += self.text_content[self.text_index][self.letter_index]
                            self.letter_index += 1
                        else:
                            if self.letter_index2 != len(self.text_content2[self.text_index]):
                                sans_sound.play()
                                self.text2 += self.text_content2[self.text_index][self.letter_index2]
                                self.letter_index2 += 1
                            else:
                                if self.letter_index3 != len(self.text_content3[self.text_index]):
                                    sans_sound.play()
                                    self.text3 += self.text_content3[self.text_index][self.letter_index3]
                                    self.letter_index3 += 1
                                else:
                                    if self.letter_index4 != len(self.text_content4[self.text_index]):
                                        sans_sound.play()
                                        self.text4 += self.text_content4[self.text_index][self.letter_index4]
                                        self.letter_index4 += 1
                        self.time_delay = self.time_delay + 1
                        text_surface = font_of_npc.render(self.text, True, self.color1)
                        text_surface2 = font_of_npc.render(self.text2, True, self.color2)
                        text_surface3 = font_of_npc.render(self.text3, True, self.color3)
                        text_surface4 = font_of_npc.render(self.text4, True, self.color4)
                        self.dialogue.text_set(text_surface, text_surface2, text_surface3, text_surface4)
                        if self.delay_text != 0:
                            self.delay_text -= 1
                            self.change = False

                    # if dialog ends
                    except IndexError:
                        # checking npc will be battle or not, and create their mechanics
                        if self.action_data[0] == "battle_with_selection":
                            if self.answer == 2:
                                test_battle_sprite = Battle_System("npc", 200, 100,
                                                                   ["npc", self.action_data[1]],
                                                                   ["forest", 13.3])
                                system_mech.add(test_battle_sprite)
                                settings.world_status_changer("BATTLE")

                        settings.world_status_changer("MAIN")
                        if self.action_data[0] == "battle_with_selection":
                            if self.answer == 2:
                                settings.world_status_changer("BATTLE")

                        self.delay_text = 5
                        self.text_index = 0
                        self.text = ""
                        self.text2 = ""
                        self.text3 = ""
                        self.text4 = ""
                        self.letter_index = 0
                        self.letter_index2 = 0
                        self.letter_index3 = 0
                        self.letter_index4 = 0
                        self.answer = 2

                        self.set_default_text_content()
                        self.dialogue.kill()
                        system_mech.remove(self.dialogue)
                        self.dialogue_create = True
                        self.action_on = False
                        self.text_index = 0

            # if dialog message not ended - we end this
            if self.change:
                if self.talking:
                    if settings.world_status == "DIALOG":
                        if self.text != self.text_content[self.text_index] and \
                                self.text2 != self.text_content2[self.text_index] and \
                                self.text3 != self.text_content3[self.text_index] and \
                                self.text4 != self.text_content4[self.text_index]:
                            self.letter_index = len(self.text_content[self.text_index])
                            self.letter_index2 = len(self.text_content2[self.text_index])
                            self.letter_index3 = len(self.text_content3[self.text_index])
                            self.letter_index4 = len(self.text_content4[self.text_index])
                            self.text = self.text_content[self.text_index]
                            self.text2 = self.text_content2[self.text_index]
                            self.text3 = self.text_content3[self.text_index]
                            self.text4 = self.text_content4[self.text_index]
                            self.change = False

            # change dialog part
            if self.change:
                if self.talking:
                    if settings.world_status == "DIALOG":
                        self.delay_text = 5
                        self.text_index += 1
                        self.text = ""
                        self.text2 = ""
                        self.text3 = ""
                        self.text4 = ""
                        self.letter_index = 0
                        self.letter_index2 = 0
                        self.letter_index3 = 0
                        self.letter_index4 = 0
                        self.change = False

            if self.up_answer:
                if self.talking:
                    if self.fps_answer_delay != 0:
                        self.fps_answer_delay -= 1
                    else:
                        for q in self.questions:
                            if self.answer == 2:
                                if q["answer_count"] == 3:
                                    self.answer = 4
                                elif q["answer_count"] == 2:
                                    self.answer = 3
                                else:
                                    self.answer = 2
                            elif self.answer == 3:
                                if q["answer_count"] == 3:
                                    self.answer = 2
                                elif q["answer_count"] == 2:
                                    self.answer = 2
                            elif self.answer == 4:
                                if q["answer_count"] == 3:
                                    self.answer = 3

                            if self.answer == 2:
                                self.color2 = self.color_active
                                self.color3 = self.color_not_active
                                self.color4 = self.color_not_active
                            elif self.answer == 3:
                                self.color2 = self.color_not_active
                                self.color3 = self.color_active
                                self.color4 = self.color_not_active
                            elif self.answer == 4:
                                self.color2 = self.color_not_active
                                self.color3 = self.color_not_active
                                self.color4 = self.color_active
                        self.fps_answer_delay = 3
                        self.up_answer = False

            if self.down_answer:
                if self.talking:
                    if self.fps_answer_delay != 0:
                        self.fps_answer_delay -= 1
                    else:
                        for q in self.questions:
                            if self.answer == 2:
                                if q["answer_count"] == 3:
                                    self.answer = 3
                                elif q["answer_count"] == 2:
                                    self.answer = 3
                                else:
                                    self.answer = 2
                            elif self.answer == 3:
                                if q["answer_count"] == 3:
                                    self.answer = 4
                                elif q["answer_count"] == 2:
                                    self.answer = 2
                            elif self.answer == 4:
                                if q["answer_count"] == 3:
                                    self.answer = 2

                            if self.answer == 2:
                                self.color2 = self.color_active
                                self.color3 = self.color_not_active
                                self.color4 = self.color_not_active
                            elif self.answer == 3:
                                self.color2 = self.color_not_active
                                self.color3 = self.color_active
                                self.color4 = self.color_not_active
                            elif self.answer == 4:
                                self.color2 = self.color_not_active
                                self.color3 = self.color_not_active
                                self.color4 = self.color_active
                        self.fps_answer_delay = 3
                        self.down_answer = False

            if self.change_with_active:
                if self.talking:
                    if self.fps_answer_delay != 0:
                        self.fps_answer_delay -= 1
                    else:
                        for q in self.questions:
                            if self.answer == 2:
                                index_of_text_after = 1
                                for i in q["text_after"]:
                                    text = i.split("/")
                                    if len(text) == 1:
                                        self.text_content[self.text_index + index_of_text_after] = text[0]
                                    elif len(text) == 2:
                                        self.text_content[self.text_index + index_of_text_after] = text[0]
                                        self.text_content2[self.text_index + index_of_text_after] = text[1]
                                    elif len(text) == 3:
                                        self.text_content[self.text_index + index_of_text_after] = text[0]
                                        self.text_content2[self.text_index + index_of_text_after] = text[1]
                                        self.text_content3[self.text_index + index_of_text_after] = text[2]
                                    elif len(text) == 4:
                                        self.text_content[self.text_index + index_of_text_after] = text[0]
                                        self.text_content2[self.text_index + index_of_text_after] = text[1]
                                        self.text_content3[self.text_index + index_of_text_after] = text[2]
                                        self.text_content4[self.text_index + index_of_text_after] = text[3]
                                    index_of_text_after += 1
                            elif self.answer == 3:
                                index_of_text_after = 1
                                for i in q["text_after_2"]:
                                    text = i.split("/")
                                    if len(text) == 1:
                                        self.text_content[self.text_index + index_of_text_after] = text[0]
                                    elif len(text) == 2:
                                        self.text_content[self.text_index + index_of_text_after] = text[0]
                                        self.text_content2[self.text_index + index_of_text_after] = text[1]
                                    elif len(text) == 3:
                                        self.text_content[self.text_index + index_of_text_after] = text[0]
                                        self.text_content2[self.text_index + index_of_text_after] = text[1]
                                        self.text_content3[self.text_index + index_of_text_after] = text[2]
                                    elif len(text) == 4:
                                        self.text_content[self.text_index + index_of_text_after] = text[0]
                                        self.text_content2[self.text_index + index_of_text_after] = text[1]
                                        self.text_content3[self.text_index + index_of_text_after] = text[2]
                                        self.text_content4[self.text_index + index_of_text_after] = text[3]
                                    index_of_text_after += 1
                            elif self.answer == 4:
                                index_of_text_after = 1
                                for i in q["text_after_3"]:
                                    text = i.split("/")
                                    if len(text) == 1:
                                        self.text_content[self.text_index + index_of_text_after] = text[0]
                                    elif len(text) == 2:
                                        self.text_content[self.text_index + index_of_text_after] = text[0]
                                        self.text_content2[self.text_index + index_of_text_after] = text[1]
                                    elif len(text) == 3:
                                        self.text_content[self.text_index + index_of_text_after] = text[0]
                                        self.text_content2[self.text_index + index_of_text_after] = text[1]
                                        self.text_content3[self.text_index + index_of_text_after] = text[2]
                                    elif len(text) == 4:
                                        self.text_content[self.text_index + index_of_text_after] = text[0]
                                        self.text_content2[self.text_index + index_of_text_after] = text[1]
                                        self.text_content3[self.text_index + index_of_text_after] = text[2]
                                        self.text_content4[self.text_index + index_of_text_after] = text[3]
                                    index_of_text_after += 1

                        self.color2 = self.color1
                        self.color3 = self.color1
                        self.color4 = self.color1
                        self.fps_answer_delay = 5
                        self.change_with_active = False
                        self.index_of_answers = 0
                        settings.world_status_changer("DIALOG")

                        if settings.world_status == "DIALOG":
                            self.delay_text = 5
                            self.text_index += 1
                            self.text = ""
                            self.text2 = ""
                            self.text3 = ""
                            self.text4 = ""
                            self.letter_index = 0
                            self.letter_index2 = 0
                            self.letter_index3 = 0
                            self.letter_index4 = 0
                            self.change = False

            # checking, if dialogue is empty, kill him
            if self.talking:
                try:
                    if self.text_content[self.text_index] == " " and self.text_content2[self.text_index] == " " and \
                            self.text_content3[self.text_index] == " " and self.text_content4[self.text_index] == " ":

                        # checking npc will be battle or not, and create their mechanics
                        if self.action_data[0] == "battle_with_selection":
                            if self.answer == 2:
                                test_battle_sprite = Battle_System("npc", 200, 100,
                                                                   ["npc", self.action_data[1]],
                                                                   ["forest", 13.3])
                                system_mech.add(test_battle_sprite)

                        settings.world_status_changer("MAIN")
                        if self.action_data[0] == "battle_with_selection":
                            if self.answer == 2:
                                settings.world_status_changer("BATTLE")

                        self.delay_text = 5
                        self.text_index = 0
                        self.text = ""
                        self.text2 = ""
                        self.text3 = ""
                        self.text4 = ""
                        self.letter_index = 0
                        self.letter_index2 = 0
                        self.letter_index3 = 0
                        self.letter_index4 = 0
                        self.answer = 2
                        self.set_default_text_content()

                        self.dialogue.kill()
                        system_mech.remove(self.dialogue)
                        self.dialogue_create = True
                        self.action_on = False
                        self.text_index = 0
                        settings.world_status_changer("MAIN")

                except IndexError:
                    pass

    def draw(self, screen):  # draw player to map
        screen.blit(self.image, (self.rect.x, self.rect.y))
