import random
import sys
import os
import pygame
import pyganim
from pygame import *
import sqlite3
from setting import *


def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


system_photo = pygame.image.load(resource_path("resources/system/sprites/MainUIAtlasTrilinear.png"))
pokeballs_photo = pygame.image.load(resource_path("resources/system/sprites/Pokeballs.png"))
pokeballs_photo_scaled = pygame.transform.scale(pokeballs_photo, (768, 768))
stars_append_photo = pygame.image.load(resource_path("resources/system/sprites/stars_append.png"))
font = pygame.font.Font(resource_path("resources/font/Pixel_Times.ttf"), 20)  # setting font


class Battle_System(pygame.sprite.Sprite):
    def __init__(self, type_of_battle, x, y, opponent, place):
        # opponent {arg} => [type_of_opponent, id_of_poke] (wild_poke)
        # opponent {arg} => [type_of_opponent, id_of_npc] (npc)
        # place {arg} => [location, time]
        super(Battle_System, self).__init__()
        self.type_system = "battle_system"
        self.type_of_battle = type_of_battle
        self.place = place[0]
        self.time = place[1]
        self.background_img = pygame.image.load(resource_path("resources/system/sprites/battle_background.png"))
        self.image = Surface([791, 465], pygame.HWSURFACE)  # Battle Sprite
        self.image = self.image.convert_alpha()  # transparent
        self.image.blit(self.background_img, [0, 0])
        self.rect = Rect(x, y, 791, 465)

        # getting location of battle
        if 4.0 < self.time <= 10.0:
            self.time = "afternoon"
        elif 10.0 < self.time <= 20.0:
            self.time = "day"
        else:
            self.time = "night"

        # bliting field (where we battle)
        self.battle_location_background = \
            pygame.image.load(resource_path(f"resources/img/places/location/{self.place}_{self.time}.png"))
        self.battle_log_background = \
            pygame.image.load(resource_path(f"resources/system/sprites/battle_log.png"))
        self.right_hp_background = pygame.Surface([157, 41], pygame.HWSURFACE)
        self.left_hp_background = pygame.Surface([157, 41], pygame.HWSURFACE)
        self.right_hp_background.set_colorkey((0, 0, 0))
        self.left_hp_background.set_colorkey((0, 0, 0))
        self.right_hp_background = self.right_hp_background.convert_alpha()
        self.left_hp_background = self.left_hp_background.convert_alpha()
        self.right_hp_background.fill((0, 0, 0, 75))
        self.left_hp_background.fill((0, 0, 0, 75))
        self.right_hp_background.blit(system_photo, (0, 0), [1843, 1237, 157, 41])
        self.left_hp_background.blit(system_photo, (0, 0), [1843, 1279, 157, 41])
        self.image.blit(self.battle_location_background, [9, 50])

        # setting pokeballs icons
        self.poke_icon_true = pygame.Surface([19, 19], pygame.HWSURFACE)
        self.poke_icon_false = pygame.Surface([19, 19], pygame.HWSURFACE)
        self.poke_icon_none = pygame.Surface([19, 19], pygame.HWSURFACE)
        self.poke_icon_true.set_colorkey((0, 0, 0))
        self.poke_icon_false.set_colorkey((0, 0, 0))
        self.poke_icon_none.set_colorkey((0, 0, 0))
        self.poke_icon_true = self.poke_icon_true.convert_alpha()
        self.poke_icon_false = self.poke_icon_false.convert_alpha()
        self.poke_icon_none = self.poke_icon_none.convert_alpha()

        self.poke_icon_true.blit(system_photo, (0, 0), [704, 123, 19, 19])
        self.poke_icon_false.blit(system_photo, (0, 0), [704, 12, 19, 19])
        self.poke_icon_none.blit(system_photo, (0, 0), [1500, 400, 20, 21])

        # setting gender icons
        self.poke_gender_male_sprite = pygame.Surface([12, 12], pygame.HWSURFACE)
        self.poke_gender_female_sprite = pygame.Surface([10, 14], pygame.HWSURFACE)
        self.poke_gender_male_sprite.set_colorkey((0, 0, 0))
        self.poke_gender_female_sprite.set_colorkey((0, 0, 0))
        self.poke_gender_male_sprite = self.poke_gender_male_sprite.convert_alpha()
        self.poke_gender_female_sprite = self.poke_gender_female_sprite.convert_alpha()

        self.poke_gender_male_sprite.blit(system_photo, (0, 0), [2034, 1786, 12, 12])
        self.poke_gender_female_sprite.blit(system_photo, (0, 0), [2038, 1770, 10, 14])

        # this need for anim in def "pokemon_onset_anim"
        self.pokeball_sprite_data = {
            "hand_with_ball_x": 0,
            "hand_with_ball_y": 0,
            "pokeball_close_x": 0,
            "pokeball_close_y": 0,
            "pokeball_open_x": 0,
            "pokeball_open_y": 0,
        }
        self.hand_with_ball_sprite = None
        self.hand_without_ball_sprite = None
        self.pokeball_close_sprite = None
        self.pokemon_onset_anim = None

        # setting buttons icons
        self.menu_type = None

        # surrender button
        self.surrender_icon_none = pygame.Surface([70, 56], pygame.HWSURFACE)
        self.surrender_icon_none.set_colorkey((0, 0, 0))
        self.surrender_icon_none = self.surrender_icon_none.convert_alpha()
        self.surrender_icon_none.blit(system_photo, (0, 0), [725, 266, 70, 56])
        self.surrender_icon_hover = pygame.Surface([70, 56], pygame.HWSURFACE)
        self.surrender_icon_hover.set_colorkey((0, 0, 0))
        self.surrender_icon_hover = self.surrender_icon_hover.convert_alpha()
        self.surrender_icon_hover.blit(system_photo, (0, 0), [725, 210, 70, 56])

        self.surrender_button_x = [self.rect.x + 700, self.rect.x + 770]
        self.surrender_button_y = [self.rect.y + 400, self.rect.y + 456]

        # attack button
        self.attack_icon_none = pygame.Surface([74, 58], pygame.HWSURFACE)
        self.attack_icon_none.set_colorkey((0, 0, 0))
        self.attack_icon_none = self.attack_icon_none.convert_alpha()
        self.attack_icon_none.blit(system_photo, (0, 0), [1973, 1418, 74, 58])
        self.attack_icon_hover = pygame.Surface([74, 58], pygame.HWSURFACE)
        self.attack_icon_hover.set_colorkey((0, 0, 0))
        self.attack_icon_hover = self.attack_icon_hover.convert_alpha()
        self.attack_icon_hover.blit(system_photo, (0, 0), [1973, 1477, 74, 58])

        self.attack_button_x = [self.rect.x + 600, self.rect.x + 674]
        self.attack_button_y = [self.rect.y + 310, self.rect.y + 368]

        # Action mechanics
        self.active = True  # Battle status (going/end)
        self.battle_status = "start"  # status of battle
        self.action = False  # action mechanics
        self.action_A = None  # action of player A
        self.action_B = None  # action of player B

        self.actions_list = []  # actions list
        self.arguments_list = []  # args list
        self.current_action = None  # current action
        self.current_arguments = None  # current arguments for function
        self.current_action_value = False  # current action value (checking function is going or not)
        self.action_index = 0

        # Log mechanics
        self.time_delay = 50
        self.log = None  # message mechanics
        self.text = ""  # message mechanics
        self.text_surface = None
        self.letter_index = 0
        self.color = (255, 255, 255)

        # text:"GO {Pokemon}!
        self.text_go = ""
        self.text_go_pokemon = ""
        self.text_surface_go_pokemon_go = None
        self.text_surface_go_pokemon = None
        self.letter_index_go_pokemon = 0
        self.letter_index_go_pokemon_go = 0
        self.color_gold = (255, 160, 0)

        self.battle_log = []  # here will be keep battle_log

        self.player_A_active_poke = None
        self.player_B_active_poke = None

        self.action_func_status = False  # it's mean if all moves (or items or change) are correct and ready for action

        # creating battle arguments
        for i in range(1, 7):
            exec(f"self.player_A_poke_{i}=None")
            exec(f"self.player_B_poke_{i}=None")

        # getting A player's_pokes
        try:
            sqlite_connection = sqlite3.connect(resource_path(f'resources/system/database/player_pokes.db'))
            cursor = sqlite_connection.cursor()
            for i in range(1, 7):
                sqlite_select_query = f'SELECT * FROM poke WHERE id_db like {i}'
                cursor.execute(sqlite_select_query)
                records = cursor.fetchall()
                if len(records) == 0:
                    pass
                else:
                    exec(f'self.player_A_poke_{i} = Pokemon(i, "player_pokes.db")')

            cursor.close()
            sqlite_connection.close()

        except sqlite3.Error as error:
            print("Ошибка при работе с SQLite", error)

        # getting B pokes
        if opponent[0] == "wild_poke":
            self.player_B_poke_1 = Pokemon(opponent[1], "wild")
        elif opponent[0] == "npc":
            try:
                sqlite_connection = sqlite3.connect(resource_path(f'resources/system/database/npc_pokes.db'))
                cursor = sqlite_connection.cursor()
                for i in range(1, 7):
                    sqlite_select_query = f'SELECT * FROM [{i}] WHERE id_npc like {opponent[1]}'
                    cursor.execute(sqlite_select_query)
                    records = cursor.fetchall()
                    if len(records) == 0:
                        pass
                    else:
                        exec(f'self.player_B_poke_{i} = Pokemon(i, "npc_pokes.db",'
                             f'"SELECT * FROM [{i}] WHERE id_npc like {opponent[1]}")')

                cursor.close()
                sqlite_connection.close()

            except sqlite3.Error as error:
                print("Ошибка при работе с SQLite", error)

        self.player_A_active_poke = self.player_A_poke_1
        self.player_B_active_poke = self.player_B_poke_1

        # bliting poke_icons on field
        self.player_A_active_poke_icon_standart = None
        self.player_B_active_poke_icon = None
        self.player_A_active_poke_standart = None
        self.player_A_active_poke_icon = None
        self.player_A_active_poke_icon_frame_1 = None
        self.player_A_active_poke_icon_frame_2 = None
        self.player_A_active_poke_icon_anim = None
        self.poke_img_load()

        # getting names, lvl from active pokes for bliting
        if self.player_A_active_poke.type_poke == "shiny":
            self.player_A_active_poke_name = \
                font_medium.render(self.player_A_active_poke.name_poke, True, self.color_gold)
        else:
            self.player_A_active_poke_name = \
                font_medium.render(self.player_A_active_poke.name_poke, True, (255, 255, 255))
        if self.player_B_active_poke.type_poke == "shiny":
            self.player_B_active_poke_name = \
                font_medium.render(self.player_B_active_poke.name_poke, True, self.color_gold)
        else:
            self.player_B_active_poke_name = \
                font_medium.render(self.player_B_active_poke.name_poke, True, (255, 255, 255))

        self.player_A_active_poke_lvl = \
            font_medium.render(self.zero_adder_to_number(f"Lv.{self.player_A_active_poke.LV}", 6, 'space'),
                               True, (255, 255, 255))
        self.player_B_active_poke_lvl = \
            font_medium.render(self.zero_adder_to_number(f"Lv.{self.player_B_active_poke.LV}", 6, 'space'),
                               True, (255, 255, 255))

        # setting poke attack moves sprite
        self.moves_sprite = []
        if self.player_A_active_poke.move_1:
            self.poke_move_1_sprite = pygame.Surface([170, 40], pygame.HWSURFACE)
            self.poke_move_1_sprite.set_colorkey((0, 0, 0))
            self.poke_move_1_sprite = self.poke_move_1_sprite.convert_alpha()
            self.poke_move_1_sprite.blit(system_photo, (0, 0), [1190, 1640, 170, 40])
            self.moves_sprite.append(self.poke_move_1_sprite)
        if self.player_A_active_poke.move_2:
            self.poke_move_2_sprite = pygame.Surface([170, 40], pygame.HWSURFACE)
            self.poke_move_2_sprite.set_colorkey((0, 0, 0))
            self.poke_move_2_sprite = self.poke_move_2_sprite.convert_alpha()
            self.poke_move_2_sprite.blit(system_photo, (0, 0), [1190, 1640, 170, 40])
            self.moves_sprite.append(self.poke_move_2_sprite)
        if self.player_A_active_poke.move_3:
            self.poke_move_3_sprite = pygame.Surface([170, 40], pygame.HWSURFACE)
            self.poke_move_3_sprite.set_colorkey((0, 0, 0))
            self.poke_move_3_sprite = self.poke_move_3_sprite.convert_alpha()
            self.poke_move_3_sprite.blit(system_photo, (0, 0), [1190, 1640, 170, 40])
            self.moves_sprite.append(self.poke_move_3_sprite)
        if self.player_A_active_poke.move_4:
            self.poke_move_4_sprite = pygame.Surface([170, 40], pygame.HWSURFACE)
            self.poke_move_4_sprite.set_colorkey((0, 0, 0))
            self.poke_move_4_sprite = self.poke_move_4_sprite.convert_alpha()
            self.poke_move_4_sprite.blit(system_photo, (0, 0), [1190, 1640, 170, 40])
            self.moves_sprite.append(self.poke_move_4_sprite)

        if type_of_battle == "wild_poke":
            catch_success = False

        # # TEST
        # self.item_effect(2)
        self.pokemon_onset_anim_setter("pokeball")
        self.pokemon_hp_xp_sprite_setter()

    def poke_img_load(self):
        self.player_A_active_poke_icon_standart = pygame.image.load(
            resource_path(f"resources/pokemon/"
                          f"{self.player_A_active_poke.type_poke}/{self.player_A_active_poke.id_pokedex}/me.png"))
        self.player_B_active_poke_icon = pygame.image.load(
            resource_path(f"resources/pokemon/"
                          f"{self.player_B_active_poke.type_poke}/{self.player_B_active_poke.id_pokedex}/foe.png"))
        self.player_A_active_poke_standart = pygame.transform.scale(self.player_A_active_poke_icon_standart,
                                                                    (192, 192))
        self.player_A_active_poke_icon = pygame.Surface([192, 198], pygame.HWSURFACE)
        self.player_A_active_poke_icon.set_colorkey((0, 0, 0))
        self.player_A_active_poke_icon = self.player_A_active_poke_icon.convert_alpha()
        # create poke anim in battle_background
        self.player_A_active_poke_icon_frame_1 = pygame.Surface([192, 198], pygame.HWSURFACE)
        self.player_A_active_poke_icon_frame_2 = pygame.Surface([192, 198], pygame.HWSURFACE)
        self.player_A_active_poke_icon_frame_1.set_colorkey((0, 0, 0))
        self.player_A_active_poke_icon_frame_1 = self.player_A_active_poke_icon_frame_1.convert_alpha()
        self.player_A_active_poke_icon_frame_2.set_colorkey((0, 0, 0))
        self.player_A_active_poke_icon_frame_2 = self.player_A_active_poke_icon_frame_2.convert_alpha()
        self.player_A_active_poke_icon_frame_1.blit(self.player_A_active_poke_standart, [0, 5])
        self.player_A_active_poke_icon_frame_2.blit(self.player_A_active_poke_standart, [0, 0])
        self.player_A_active_poke_icon_anim = pyganim.PygAnimation([
            (self.player_A_active_poke_icon_frame_1, 0.5),
            (self.player_A_active_poke_icon_frame_2, 0.5)])
        self.player_A_active_poke_icon_anim.play()
        self.image.blit(self.player_B_active_poke_icon, [370, 82])
        self.text_surface = font.render(self.text, True, self.color)
        self.text_surface_go_pokemon = font.render(self.text_go_pokemon, True, self.color_gold)
        self.text_surface_go_pokemon_go = font.render(self.text_go, True, self.color)

    def item_access(self, id_of_item):
        if self.type_of_battle == "NPC":
            if 1 <= id_of_item <= 16 or 63 <= id_of_item <= 126 or id_of_item >= 190:
                self.action_func_status = False
            else:
                self.action_func_status = True
        elif self.type_of_battle == "wild_poke":
            if 63 <= id_of_item <= 126 or id_of_item >= 190:
                self.action_func_status = False
            else:
                self.action_func_status = True
        else:
            self.action_func_status = False

    def item_effect(self, id_of_item):
        if id_of_item == 1:
            catch_rate = 1
        if 2 <= id_of_item <= 16:
            try:
                sqlite_connection = sqlite3.connect(resource_path(f'resources/system/database/POKE_DB.db'))
                cursor = sqlite_connection.cursor()
                sqlite_select_query = f'SELECT capture_rate FROM pokemon_species ' \
                                      f'WHERE id like {self.player_B_active_poke.id_pokedex}'
                cursor.execute(sqlite_select_query)
                records = cursor.fetchone()
                catch_rate = records[0]

                cursor.close()
                sqlite_connection.close()

            except sqlite3.Error as error_info:
                catch_rate = None
                print("Ошибка при работе с SQLite", error_info)

            pokeball_multiplier = None
            if id_of_item == 2:
                pokeball_multiplier = 2
            elif id_of_item == 3:
                pokeball_multiplier = 1.5
            elif id_of_item == 4:
                pokeball_multiplier = 1
            # elif id_of_item == 5:

            status_rate = None
            if self.player_B_active_poke.status is None:
                status_rate = 1
            elif self.player_B_active_poke.status == "par" or "brn" or "psn":
                status_rate = 1.5
            elif self.player_B_active_poke.status == "slp" or "frz":
                status_rate = 2.5
            catch_rate = (catch_rate * pokeball_multiplier * status_rate *
                          (1 - (2 / 3) * (self.player_B_active_poke.HP / self.player_B_active_poke.STAT_HP))) / 255
            catch_number = random.random()
            if catch_number < catch_rate:
                print(f"catch_rate is: {catch_number}")
                catch_rate = True

    def action_func(self, action_A, action_B):  # WE NEED CHECK IT < ADD BUTTON SURRENDER
        if action_A == "start" and action_B == "start":
            self.actions_list.append(self.delay_func)
            self.arguments_list.append([True, 20])

            self.actions_list.append(self.log_message)
            self.arguments_list.append("· Battle start!")

            self.actions_list.append(self.delay_func)
            self.arguments_list.append([True, 20])

            # self.actions_list.append(self.log_message)
            # self.arguments_list.append(f"· Go {self.player_A_active_poke.name_poke}!")

            self.actions_list.append(self.log_message_go_pokemon)
            self.arguments_list.append(['· Go ', f"{self.player_A_active_poke.name_poke}!"])

            self.actions_list.append(self.delay_func)
            self.arguments_list.append([True, 50])

            self.actions_list.append(self.start_ender_func)
            self.arguments_list.append(None)

        elif action_A == "surrender" or action_B == "surrender":
            self.player_A_active_poke_icon_anim.pause()

            self.actions_list.append(self.log_message)
            self.arguments_list.append("· You are surrendered!")

            self.actions_list.append(self.delay_func)
            self.arguments_list.append([True, 50])

            self.actions_list.append(self.log_message)
            self.arguments_list.append("· You lost the battle!")

            self.actions_list.append(self.delay_func)
            self.arguments_list.append([True, 50])

            self.actions_list.append(self.end_battle)
            self.arguments_list.append(None)
        # if action_A == "change" or action_A == "item":
        #     if action_B == "change" or action_B == "item":
        #         if self.player_A_active_poke.STAT_SPD > self.player_B_active_poke.STAT_SPD:
        #
        #         elif self.player_A_active_poke.STAT_SPD < self.player_B_active_poke.STAT_SPD:
        #
        #         else:

    def battle_status_changer(self, status):
        self.battle_status = status

    def end_battle(self):
        self.battle_status = "end"
        self.action = False

    def log_message(self, message):
        self.log = message
        if self.letter_index != len(self.log):
            self.text += self.log[self.letter_index]
            self.letter_index += 1
            self.current_action_value = True
        else:
            self.letter_index = 0
            self.current_action_value = False
            self.action_index += 1
        self.text_surface = font.render(self.text, True, self.color)

    def log_message_go_pokemon(self, message):
        self.log = message
        if self.letter_index_go_pokemon_go != len(self.log[0]):
            self.text_go += self.log[0][self.letter_index_go_pokemon_go]
            self.letter_index_go_pokemon_go += 1
            self.current_action_value = True
        else:
            if self.letter_index_go_pokemon != len(self.log[1]):
                self.text_go_pokemon += self.log[1][self.letter_index_go_pokemon]
                self.letter_index_go_pokemon += 1
                self.current_action_value = True
            else:
                self.letter_index_go_pokemon = 0
                self.letter_index_go_pokemon_go = 0
                self.current_action_value = False
                self.action_index += 1
        self.text_surface_go_pokemon_go = font.render(self.text_go, True, self.color)
        self.text_surface_go_pokemon = font.render(self.text_go_pokemon, True, self.color_gold)

    def start_ender_func(self):
        self.pokemon_onset_anim.stop()
        del self.pokemon_onset_anim
        self.pokemon_hp_A_anim.stop()
        del self.pokemon_hp_A_anim
        self.pokemon_hp_B_anim.stop()
        del self.pokemon_hp_B_anim
        self.action_A = None
        self.action_B = None
        self.action_index += 1

    def log_clearner(self):
        self.text = ""
        self.text_surface = font.render(self.text, True, self.color)

        self.text_go = ""
        self.text_go_pokemon = ""
        self.text_surface_go_pokemon_go = font.render(self.text_go, True, self.color)
        self.text_surface_go_pokemon = font.render(self.text_go_pokemon, True, self.color_gold)

        self.action_index += 1

    def delay_func(self, args):
        # [log_clear, time_for_future_delay_func]
        if self.time_delay < 0:
            if args[0]:
                self.text = ""
                self.text_surface = font.render(self.text, True, self.color)

                self.text_go = ""
                self.text_go_pokemon = ""
                self.text_surface_go_pokemon_go = font.render(self.text_go, True, self.color)
                self.text_surface_go_pokemon = font.render(self.text_go_pokemon, True, self.color_gold)
            self.time_delay = args[1]
            self.current_action_value = False
            self.action_index += 1
        else:
            self.time_delay -= 1

    def button_hover(self, x_mouse, y_mouse):
        if self.surrender_button_x[0] < x_mouse < self.surrender_button_x[1] and \
                self.surrender_button_y[0] < y_mouse < self.surrender_button_y[1]:
            self.image.blit(self.surrender_icon_hover, (700, 400))
        else:
            self.image.blit(self.surrender_icon_none, (700, 400))

        if self.attack_button_x[0] < x_mouse < self.attack_button_x[1] and \
                self.attack_button_y[0] < y_mouse < self.attack_button_y[1]:
            self.image.blit(self.attack_icon_hover, (600, 310))
        else:
            self.image.blit(self.attack_icon_none, (600, 310))

    def press_checker(self, e_pos_x, e_pos_y):
        # close button condition
        if self.battle_status == "waiting":
            if self.surrender_button_x[0] <= e_pos_x <= self.surrender_button_x[1] and \
                    self.surrender_button_y[0] <= e_pos_y <= self.surrender_button_y[1]:
                self.menu_type = None
                self.action_A = "surrender"
            if self.attack_button_x[0] <= e_pos_x <= self.attack_button_x[1] and \
                    self.attack_button_y[0] <= e_pos_y <= self.attack_button_y[1]:
                self.menu_type = "attack"

    def menu_updater(self):
        if self.menu_type == "attack":
            y = 59
            for i in self.moves_sprite:
                self.image.blit(i, [599, y])
                pygame.draw.rect(self.image, (105, 105, 105), [599, y, 170, 40], 2)
                y += 47

    def update(self, screen, *args):
        # update buttons pos
        self.surrender_button_x = [self.rect.x + 700, self.rect.x + 770]
        self.surrender_button_y = [self.rect.y + 400, self.rect.y + 456]
        self.attack_button_x = [self.rect.x + 600, self.rect.x + 674]
        self.attack_button_y = [self.rect.y + 310, self.rect.y + 368]

        # battle status
        if self.active:
            if self.battle_status == "waiting":
                if self.action_A is None and self.action_B is None:  # BUT HERE MUST BE OR (not and)
                    pass
                else:
                    self.battle_status = "action"
            elif self.battle_status == "action":
                # print(self.arguments_list)
                if not self.action:
                    self.action_func(self.action_A, self.action_B)
                    self.action = True
                else:
                    #  If there are still any functions in the list, we perform them
                    if self.action_index + 1 <= len(self.actions_list) != 0:
                        if self.current_action_value is False:  # if current action is empty
                            self.current_action = self.actions_list[self.action_index]
                            self.current_arguments = self.arguments_list[self.action_index]
                            self.current_action_value = True
                        else:
                            if self.current_arguments is None:  # if function doesn't need any arguments
                                self.current_action()
                            else:  # if function need arguments, we give them
                                self.current_action(self.current_arguments)
                    else:
                        self.actions_list = []
                        self.arguments_list = []
                        self.action_index = 0
                        self.action = False
                        self.current_action = None
                        self.current_arguments = None
                        self.current_action_value = False
                        self.battle_status = "waiting"

            # if battle just started
            elif self.battle_status == "start":
                self.pokemon_onset_anim.play()
                self.pokemon_hp_A_anim.play()
                self.pokemon_hp_B_anim.play()
                self.action_A = "start"
                self.action_B = "start"
                self.battle_status = "action"

            # if battle end
            elif self.battle_status == "end":
                self.active = False
                args[1].world_status_changer("MAIN")  # change status of world
                # args[2].map_changer("from_TestMap_to_TestHouse", "up", 19 * 32, 15 * 32)
                self.kill()

        #  bliting
        if self.active:
            self.image.fill((255, 255, 255, 0))
            self.image.blit(self.background_img, [0, 0])

            self.image.blit(self.battle_location_background, [9, 50])
            self.image.blit(self.battle_log_background, [9, 410])
            self.image.blit(self.right_hp_background, [20, 70])
            self.image.blit(self.left_hp_background, [410, 305])

            self.pokeball_icons_draw()
            self.button_hover(args[0][0], args[0][1])  # mouse pos in args

            if self.action_A == 'start':
                # poke onset anim setting
                if self.pokemon_onset_anim.state != "stopped":
                    self.pokemon_onset_anim.blit(self.image, [0, 100])
                else:
                    self.image.blit(self.player_A_active_poke_standart, [30, 220])

                # poke hp anim setting
                if self.pokemon_hp_A_anim.state != "stopped":
                    self.pokemon_hp_A_anim.blit(self.image, [414, 326])
                else:
                    self.hp_pokemon_A_sprite = pygame.draw.line(self.image, (0, 200, 64),
                                                                [self.HP_line_percentage_pokemon_A, 327],
                                                                [560, 327], 4)

                if self.pokemon_hp_B_anim.state != "stopped":
                    self.pokemon_hp_B_anim.blit(self.image, [26, 90])
                else:
                    self.hp_pokemon_B_sprite = pygame.draw.line(self.image, (0, 200, 64),
                                                                [26, 91],
                                                                [self.HP_line_percentage_pokemon_B, 91], 4)
            else:
                self.player_A_active_poke_icon_anim.blit(self.image, [30, 215])
                self.hp_pokemon_A_sprite = pygame.draw.line(self.image, (0, 200, 64),
                                                            [self.HP_line_percentage_pokemon_A, 327],
                                                            [560, 327], 4)
                self.hp_pokemon_B_sprite = pygame.draw.line(self.image, (0, 200, 64),
                                                            [26, 91],
                                                            [self.HP_line_percentage_pokemon_B, 91], 4)
            self.image.blit(self.player_B_active_poke_icon, [370, 82])

            self.image.blit(self.player_A_active_poke_name, (430, 308))
            self.image.blit(self.player_B_active_poke_name, (45, 72))
            self.image.blit(self.player_A_active_poke_lvl, (520, 308))
            self.image.blit(self.player_B_active_poke_lvl, (130, 72))
            if self.player_A_active_poke.poke_gender == "male":
                self.image.blit(self.poke_gender_male_sprite, (415, 308))
            else:
                self.image.blit(self.poke_gender_female_sprite, (415, 308))
            if self.player_B_active_poke.poke_gender == "male":
                self.image.blit(self.poke_gender_male_sprite, (30, 72))
            else:
                self.image.blit(self.poke_gender_female_sprite, (30, 72))\

            self.menu_updater()  # bliting menu

            self.image.blit(self.text_surface, (30, 425))
            self.image.blit(self.text_surface_go_pokemon_go, (30, 425))
            self.image.blit(self.text_surface_go_pokemon, (75, 425))
            screen.blit(self.image, (self.rect.x, self.rect.y))

    def pokeball_icons_draw(self):
        x_cord_of_A_icons = 432
        x_cord_of_B_icons = 26
        for i in range(1, 7):
            if eval(f"self.player_A_poke_{i} is None"):
                self.image.blit(self.poke_icon_none, [x_cord_of_A_icons, 355])
            else:
                if eval(f"self.player_A_poke_{i}.HP == 0"):
                    self.image.blit(self.poke_icon_false, [x_cord_of_A_icons, 355])
                else:
                    self.image.blit(self.poke_icon_true, [x_cord_of_A_icons, 355])

            if eval(f"self.player_B_poke_{i} is None"):
                self.image.blit(self.poke_icon_none, [x_cord_of_B_icons, 120])
            else:
                if eval(f"self.player_B_poke_{i}.HP == 0"):
                    self.image.blit(self.poke_icon_false, [x_cord_of_B_icons, 120])
                else:
                    self.image.blit(self.poke_icon_true, [x_cord_of_B_icons, 120])

            x_cord_of_A_icons = x_cord_of_A_icons + 22
            x_cord_of_B_icons = x_cord_of_B_icons + 22

    def pokemon_hp_xp_sprite_setter(self):
        self.hp_drop_A = (147 * (self.player_A_active_poke.HP / self.player_A_active_poke.STAT_HP)) / 20
        self.hp_drop_B = (147 * (self.player_B_active_poke.HP / self.player_B_active_poke.STAT_HP)) / 20

        for i in range(0, 21):
            exec(f"self.frame_hp_A_{i} = pygame.Surface([147, 4], pygame.SRCALPHA)")
            exec(f"self.frame_hp_A_drop_{i} = pygame.Surface([{round(self.hp_drop_A * i)}, 4])")
            exec(f"self.frame_hp_A_drop_{i}.fill((0, 200, 64))")
            exec(f"self.frame_hp_A_{i}.blit(self.frame_hp_A_drop_{i}, [{147 - round(self.hp_drop_A * i)}, 0])")

            exec(f"self.frame_hp_B_{i} = pygame.Surface([147, 4], pygame.SRCALPHA)")
            exec(f"self.frame_hp_B_drop_{i} = pygame.Surface([{round(self.hp_drop_B * i)}, 4])")
            exec(f"self.frame_hp_B_drop_{i}.fill((0, 200, 64))")
            exec(f"self.frame_hp_B_{i}.blit(self.frame_hp_B_drop_{i}, [0, 0])")

        # creating array for frames (animations)
        self.pokemon_hp_A_anim_array = []
        self.pokemon_hp_B_anim_array = []
        for i in range(0, 21):
            exec(f"self.pokemon_hp_A_anim_array.append([self.frame_hp_A_{i}, 0.05])")
            exec(f"self.pokemon_hp_B_anim_array.append([self.frame_hp_B_{i}, 0.05])")
        self.pokemon_hp_A_anim = pyganim.PygAnimation(self.pokemon_hp_A_anim_array)
        self.pokemon_hp_B_anim = pyganim.PygAnimation(self.pokemon_hp_B_anim_array)
        self.pokemon_hp_A_anim.loop = not self.pokemon_hp_A_anim.loop
        self.pokemon_hp_B_anim.loop = not self.pokemon_hp_B_anim.loop

        self.HP_line_percentage_pokemon_A = 560 - (
                146 * (self.player_A_active_poke.HP / self.player_A_active_poke.STAT_HP))
        self.HP_line_percentage_pokemon_B = 173 - (
                146 * (self.player_B_active_poke.HP / self.player_B_active_poke.STAT_HP))

    def pokemon_onset_anim_setter(self, pokeball):
        for i in range(1, 23):
            exec(f"self.frame_me_{i} = pygame.Surface([340, 340], pygame.SRCALPHA)")

        if pokeball == "pokeball":
            self.pokeball_sprite_data["hand_with_ball_x"] = 384
            self.pokeball_sprite_data["hand_with_ball_y"] = 448
            self.pokeball_sprite_data["pokeball_close_x"] = 357
            self.pokeball_sprite_data["pokeball_close_y"] = 308

        # getting needing sprites for anim
        self.hand_with_ball_sprite = pygame.Surface([47, 62], pygame.SRCALPHA)
        self.hand_without_ball_sprite = pygame.Surface([46, 64], pygame.SRCALPHA)
        self.pokeball_close_sprite = pygame.Surface([28, 28], pygame.SRCALPHA)
        self.hand_with_ball_sprite.blit(
            pokeballs_photo, (0, 0),
            [self.pokeball_sprite_data["hand_with_ball_x"], self.pokeball_sprite_data["hand_with_ball_y"], 47, 62])
        self.hand_without_ball_sprite.blit(pokeballs_photo, (0, 0), [336, 383, 46, 64])
        self.pokeball_close_sprite.blit(
            pokeballs_photo, (0, 0),
            [self.pokeball_sprite_data["pokeball_close_x"], self.pokeball_sprite_data["pokeball_close_y"], 28, 28])
        self.frame_me_hand_with_ball = pygame.transform.flip(self.hand_with_ball_sprite, True, False)
        self.frame_me_hand_without_ball = pygame.transform.flip(self.hand_without_ball_sprite, True, False)

        # frame 1
        self.frame_me_1_hand_with_ball = pygame.transform.rotate(self.frame_me_hand_with_ball, 240)
        self.frame_me_1.blit(self.frame_me_1_hand_with_ball, [-50, 250])

        # frame 2
        self.frame_me_2_hand_with_ball = pygame.transform.rotate(self.frame_me_hand_with_ball, 240)
        self.frame_me_2.blit(self.frame_me_2_hand_with_ball, [-40, 250])

        # frame 3
        self.frame_me_3_hand_with_ball = pygame.transform.rotate(self.frame_me_hand_with_ball, 240)
        self.frame_me_3.blit(self.frame_me_3_hand_with_ball, [-30, 250])

        # frame 4
        self.frame_me_4_hand_with_ball = pygame.transform.rotate(self.frame_me_hand_with_ball, 240)
        self.frame_me_4.blit(self.frame_me_4_hand_with_ball, [-20, 250])

        # frame 5
        self.frame_me_5_hand_with_ball = pygame.transform.rotate(self.frame_me_hand_with_ball, 250)
        self.frame_me_5.blit(self.frame_me_5_hand_with_ball, [-13, 247])

        # frame 6
        self.frame_me_6_hand_with_ball = pygame.transform.rotate(self.frame_me_hand_with_ball, 260)
        self.frame_me_6.blit(self.frame_me_6_hand_with_ball, [-6, 243])

        # frame 7
        self.frame_me_7_hand_with_ball = pygame.transform.rotate(self.frame_me_hand_with_ball, 270)
        self.frame_me_7.blit(self.frame_me_7_hand_with_ball, [0, 240])

        # frame 8
        self.frame_me_8_hand_with_ball = pygame.transform.rotate(self.frame_me_hand_with_ball, 280)
        self.frame_me_8.blit(self.frame_me_8_hand_with_ball, [-4, 230])

        # frame 9
        self.frame_me_9_hand_without_ball = pygame.transform.rotate(self.frame_me_hand_without_ball, 265)
        self.pokeball_close_sprite_9 = pygame.Surface([28, 28], pygame.SRCALPHA)
        self.pokeball_close_sprite_9 = pygame.transform.rotate(self.pokeball_close_sprite, 210)
        self.frame_me_9.blit(self.frame_me_9_hand_without_ball, [-10, 210])
        self.frame_me_9.blit(self.pokeball_close_sprite_9, [30, 180])

        # frame 10
        self.frame_me_10_hand_without_ball = pygame.transform.rotate(self.frame_me_hand_without_ball, 265)
        self.pokeball_close_sprite_10 = pygame.Surface([28, 28], pygame.SRCALPHA)
        self.pokeball_close_sprite_10 = pygame.transform.rotate(self.pokeball_close_sprite, 190)
        self.frame_me_10.blit(self.frame_me_10_hand_without_ball, [-10, 210])
        self.frame_me_10.blit(self.pokeball_close_sprite_10, [40, 160])

        # frame 11
        self.frame_me_11_hand_without_ball = pygame.transform.rotate(self.frame_me_hand_without_ball, 265)
        self.pokeball_close_sprite_11 = pygame.Surface([28, 28], pygame.SRCALPHA)
        self.pokeball_close_sprite_11 = pygame.transform.rotate(self.pokeball_close_sprite, 170)
        self.frame_me_11.blit(self.frame_me_11_hand_without_ball, [-20, 210])
        self.frame_me_11.blit(self.pokeball_close_sprite_11, [50, 140])

        # frame 12
        self.frame_me_12_hand_without_ball = pygame.transform.rotate(self.frame_me_hand_without_ball, 265)
        self.pokeball_close_sprite_12 = pygame.Surface([28, 28], pygame.SRCALPHA)
        self.pokeball_close_sprite_12 = pygame.transform.rotate(self.pokeball_close_sprite, 150)
        self.frame_me_12.blit(self.frame_me_12_hand_without_ball, [-30, 210])
        self.frame_me_12.blit(self.pokeball_close_sprite_12, [60, 120])

        # frame 13
        self.frame_me_13_hand_without_ball = pygame.transform.rotate(self.frame_me_hand_without_ball, 265)
        self.pokeball_close_sprite_13 = pygame.Surface([28, 28], pygame.SRCALPHA)
        self.pokeball_close_sprite_13 = pygame.transform.rotate(self.pokeball_close_sprite, 130)
        self.frame_me_13.blit(self.frame_me_13_hand_without_ball, [-40, 210])
        self.frame_me_13.blit(self.pokeball_close_sprite_13, [70, 120])

        # frame 14
        self.frame_me_14_hand_without_ball = pygame.transform.rotate(self.frame_me_hand_without_ball, 265)
        self.pokeball_close_sprite_14 = pygame.Surface([28, 28], pygame.SRCALPHA)
        self.pokeball_close_sprite_14 = pygame.transform.rotate(self.pokeball_close_sprite, 110)
        self.frame_me_14.blit(self.frame_me_14_hand_without_ball, [-50, 210])
        self.frame_me_14.blit(self.pokeball_close_sprite_14, [80, 140])

        # frame 15
        self.pokeball_close_sprite_15 = pygame.Surface([28, 28], pygame.SRCALPHA)
        self.pokeball_close_sprite_15 = pygame.transform.rotate(self.pokeball_close_sprite, 90)
        self.frame_me_15.blit(self.pokeball_close_sprite_15, [90, 160])

        # frame 16
        self.pokeball_close_sprite_16 = pygame.Surface([28, 28], pygame.SRCALPHA)
        self.pokeball_close_sprite_16 = pygame.transform.rotate(self.pokeball_close_sprite, 70)
        self.frame_me_16.blit(self.pokeball_close_sprite_16, [100, 170])

        # frame 17
        self.pokeball_close_sprite_17 = pygame.Surface([28, 28], pygame.SRCALPHA)
        self.pokeball_close_sprite_17 = pygame.transform.rotate(self.pokeball_close_sprite, 50)
        self.frame_me_17.blit(self.pokeball_close_sprite_17, [100, 180])

        # frame 18
        self.pokeball_close_sprite_18 = pygame.Surface([28, 28], pygame.SRCALPHA)
        self.pokeball_close_sprite_18 = pygame.transform.rotate(self.pokeball_close_sprite, 30)
        self.frame_me_18.blit(self.pokeball_close_sprite_18, [100, 200])

        # frame 19
        self.stars_append_sprite_19 = pygame.Surface([140, 140], pygame.SRCALPHA)
        self.stars_append_sprite_19.blit(stars_append_photo, (0, 0), [200, 27, 140, 140])
        self.frame_me_19.blit(self.player_A_active_poke_standart, [30, 120])
        self.frame_me_19.blit(self.stars_append_sprite_19, [60, 185])

        # frame 20
        self.stars_append_sprite_20 = pygame.Surface([140, 140], pygame.SRCALPHA)
        self.stars_append_sprite_20.blit(stars_append_photo, (0, 0), [20, 644, 140, 140])
        self.frame_me_20.blit(self.player_A_active_poke_standart, [30, 120])
        self.frame_me_20.blit(self.stars_append_sprite_20, [60, 185])

        # frame 21
        self.stars_append_sprite_21 = pygame.Surface([140, 140], pygame.SRCALPHA)
        self.stars_append_sprite_21.blit(stars_append_photo, (0, 0), [375, 639, 140, 140])
        self.frame_me_21.blit(self.player_A_active_poke_standart, [30, 120])
        self.frame_me_21.blit(self.stars_append_sprite_21, [60, 185])

        # frame 22
        self.stars_append_sprite_22 = pygame.Surface([140, 140], pygame.SRCALPHA)
        self.stars_append_sprite_22.blit(stars_append_photo, (0, 0), [17, 25, 140, 140])
        self.frame_me_22.blit(self.player_A_active_poke_standart, [30, 120])
        self.frame_me_22.blit(self.stars_append_sprite_22, [60, 185])

        self.pokemon_onset_anim = pyganim.PygAnimation([
            (self.frame_me_1, 0.06),
            (self.frame_me_2, 0.06),
            (self.frame_me_3, 0.06),
            (self.frame_me_4, 0.06),
            (self.frame_me_5, 0.06),
            (self.frame_me_6, 0.06),
            (self.frame_me_7, 0.06),
            (self.frame_me_8, 0.06),
            (self.frame_me_9, 0.06),
            (self.frame_me_10, 0.06),
            (self.frame_me_11, 0.06),
            (self.frame_me_12, 0.06),
            (self.frame_me_13, 0.06),
            (self.frame_me_14, 0.06),
            (self.frame_me_15, 0.06),
            (self.frame_me_16, 0.06),
            (self.frame_me_17, 0.06),
            (self.frame_me_18, 0.06),
            (self.frame_me_19, 0.12),
            (self.frame_me_20, 0.12),
            (self.frame_me_21, 0.12),
            (self.frame_me_22, 0.12)])
        self.pokemon_onset_anim.loop = not self.pokemon_onset_anim.loop

    @staticmethod
    def zero_adder_to_number(number, zero_number, type_of_adding):
        string = str(number)
        list_of_str = list(string)
        for i in range(0, zero_number - len(list_of_str)):
            if type_of_adding == 0:
                list_of_str.insert(0, "0")
            elif type_of_adding == "space":
                list_of_str.insert(0, "   ")
        result = "".join(list_of_str)
        return result
