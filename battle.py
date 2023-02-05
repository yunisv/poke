import random
import sys
import os
import pygame
import pyganim
from pygame import *
import sqlite3
from setting import *
from Moves import *


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
        self.weather = None
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
        self.selected_A = None  # action mechanics
        self.selected_B = None  # action mechanics

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
        sqlite_connection = sqlite3.connect(resource_path(f'resources/system/database/POKE_DB.db'))
        cursor = sqlite_connection.cursor()
        self.poke_move_1_pos = [self.rect.x + 599, self.rect.y + 59]  # + [170, 40]
        self.poke_move_2_pos = [self.rect.x + 599, self.rect.y + 106]  # + [170, 40]
        self.poke_move_3_pos = [self.rect.x + 599, self.rect.y + 153]  # + [170, 40]
        self.poke_move_4_pos = [self.rect.x + 599, self.rect.y + 200]  # + [170, 40]
        self.move_desc_surface = pygame.Surface([185, 79], pygame.HWSURFACE)
        self.move_desc_surface.set_colorkey((0, 0, 0))
        self.move_desc_surface = self.move_desc_surface.convert_alpha()
        self.move_desc_surface.blit(system_photo, (0, 0), [515, 20, 185, 79])
        if self.player_A_active_poke.move_1:
            self.poke_move_1_sprite = pygame.Surface([170, 40], pygame.HWSURFACE)
            self.poke_move_1_sprite.set_colorkey((0, 0, 0))
            self.poke_move_1_sprite = self.poke_move_1_sprite.convert_alpha()
            self.poke_move_1_sprite.blit(system_photo, (0, 0), [1190, 1640, 170, 40])

            sqlite_select_query = f'SELECT * FROM moves WHERE id like {self.player_A_active_poke.move_1}'
            cursor.execute(sqlite_select_query)
            records = cursor.fetchall()
            for row in records:
                self.player_A_active_poke_move_1_id = row[0]
                self.player_A_active_poke_move_1_name = row[1]
                self.player_A_active_poke_move_1_name = f"{self.player_A_active_poke_move_1_name}".title()
                self.player_A_active_poke_move_1_element = row[3]
                self.player_A_active_poke_move_1_power = row[4]
                self.player_A_active_poke_move_1_pp = row[5]
                self.player_A_active_poke_move_1_accuracy = row[6]
                self.player_A_active_poke_move_1_type = row[9]
                self.player_A_active_poke_move_1_effect = row[10]

            if self.player_A_active_poke_move_1_type == 1:
                self.poke_move_1_sprite.blit(status_attack_icon, (4, 22))  # type of attack
            elif self.player_A_active_poke_move_1_type == 2:
                self.poke_move_1_sprite.blit(damage_attack_icon, (4, 22))  # type of attack
            elif self.player_A_active_poke_move_1_type == 3:
                self.poke_move_1_sprite.blit(special_attack_icon, (4, 22))  # type of attack
            self.element_poke_getter(self.player_A_active_poke_move_1_element, self.poke_move_1_sprite)  # element atk
            self.player_A_active_poke_move_1_name_sprite = font_small.render(
                self.player_A_active_poke_move_1_name, True, (255, 255, 255)
            )  # name of move (font.render)
            # name of move
            self.poke_move_1_sprite.blit(self.player_A_active_poke_move_1_name_sprite, (5, 5))
            # setting pp of move
            self.player_A_active_poke_move_1_pp_str = \
                f"{self.player_A_active_poke.pp_1}/{self.player_A_active_poke_move_1_pp}"
            self.player_A_active_poke_move_1_pp_str = self.zero_adder_to_number(
                self.player_A_active_poke_move_1_pp_str, 5, "space"
            )
            self.player_A_active_poke_move_1_pp_str = font_small.render(
                self.player_A_active_poke_move_1_pp_str, True, (255, 255, 255)
            )
            self.poke_move_1_sprite.blit(self.player_A_active_poke_move_1_pp_str, (130, 22))

            # getting desc about move
            for id_of_json_move, data in moves.items():
                if data['name'] == self.move_word(self.player_A_active_poke_move_1_name):
                    self.player_A_active_poke_move_1_desc = data["desc"]
            self.player_A_active_poke_move_1_acc_text = f"ACC: {self.player_A_active_poke_move_1_accuracy}"
            self.player_A_active_poke_move_1_pwr_text = f"PWR: {self.player_A_active_poke_move_1_power}"
            self.player_A_active_poke_move_1_acc_sprite = font_small.render(
                self.zero_adder_to_number(self.player_A_active_poke_move_1_acc_text, 8, "space"), True, (255, 255, 255)
            )
            self.player_A_active_poke_move_1_pwr_sprite = font_small.render(
                self.zero_adder_to_number(self.player_A_active_poke_move_1_pwr_text, 8, "space"), True, (255, 255, 255)
            )

            self.moves_sprite.append(self.poke_move_1_sprite)
        if self.player_A_active_poke.move_2:
            self.poke_move_2_sprite = pygame.Surface([170, 40], pygame.HWSURFACE)
            self.poke_move_2_sprite.set_colorkey((0, 0, 0))
            self.poke_move_2_sprite = self.poke_move_2_sprite.convert_alpha()
            self.poke_move_2_sprite.blit(system_photo, (0, 0), [1190, 1640, 170, 40])

            sqlite_select_query = f'SELECT * FROM moves WHERE id like {self.player_A_active_poke.move_2}'
            cursor.execute(sqlite_select_query)
            records = cursor.fetchall()
            for row in records:
                self.player_A_active_poke_move_2_id = row[0]
                self.player_A_active_poke_move_2_name = row[1]
                self.player_A_active_poke_move_2_name = f"{self.player_A_active_poke_move_2_name}".title()
                self.player_A_active_poke_move_2_element = row[3]
                self.player_A_active_poke_move_2_power = row[4]
                self.player_A_active_poke_move_2_pp = row[5]
                self.player_A_active_poke_move_2_accuracy = row[6]
                self.player_A_active_poke_move_2_type = row[9]
                self.player_A_active_poke_move_2_effect = row[10]

            if self.player_A_active_poke_move_2_type == 1:
                self.poke_move_2_sprite.blit(status_attack_icon, (4, 22))  # type of attack
            elif self.player_A_active_poke_move_2_type == 2:
                self.poke_move_2_sprite.blit(damage_attack_icon, (4, 22))  # type of attack
            elif self.player_A_active_poke_move_2_type == 3:
                self.poke_move_2_sprite.blit(special_attack_icon, (4, 22))  # type of attack
            self.element_poke_getter(self.player_A_active_poke_move_2_element, self.poke_move_2_sprite)
            self.player_A_active_poke_move_2_name_sprite = font_small.render(
                self.player_A_active_poke_move_2_name, True, (255, 255, 255)
            )
            # setting pp of move
            self.player_A_active_poke_move_2_pp_str = \
                f"{self.player_A_active_poke.pp_2}/{self.player_A_active_poke_move_2_pp}"
            self.player_A_active_poke_move_2_pp_str = self.zero_adder_to_number(
                self.player_A_active_poke_move_2_pp_str, 5, "space"
            )
            self.player_A_active_poke_move_2_pp_str = font_small.render(
                self.player_A_active_poke_move_2_pp_str, True, (255, 255, 255)
            )
            self.poke_move_2_sprite.blit(self.player_A_active_poke_move_2_pp_str, (130, 22))
            self.poke_move_2_sprite.blit(self.player_A_active_poke_move_2_name_sprite, (5, 5))

            # getting desc about move
            for id_of_json_move, data in moves.items():
                if data['name'] == self.move_word(self.player_A_active_poke_move_2_name):
                    self.player_A_active_poke_move_2_desc = data["desc"]
            self.player_A_active_poke_move_2_acc_text = f"ACC: {self.player_A_active_poke_move_2_accuracy}"
            self.player_A_active_poke_move_2_pwr_text = f"PWR: {self.player_A_active_poke_move_2_power}"
            self.player_A_active_poke_move_2_acc_sprite = font_small.render(
                self.zero_adder_to_number(self.player_A_active_poke_move_2_acc_text, 8, "space"), True, (255, 255, 255)
            )
            self.player_A_active_poke_move_2_pwr_sprite = font_small.render(
                self.zero_adder_to_number(self.player_A_active_poke_move_2_pwr_text, 8, "space"), True, (255, 255, 255)
            )

            self.moves_sprite.append(self.poke_move_2_sprite)
        if self.player_A_active_poke.move_3:
            self.poke_move_3_sprite = pygame.Surface([170, 40], pygame.HWSURFACE)
            self.poke_move_3_sprite.set_colorkey((0, 0, 0))
            self.poke_move_3_sprite = self.poke_move_3_sprite.convert_alpha()
            self.poke_move_3_sprite.blit(system_photo, (0, 0), [1190, 1640, 170, 40])

            sqlite_select_query = f'SELECT * FROM moves WHERE id like {self.player_A_active_poke.move_3}'
            cursor.execute(sqlite_select_query)
            records = cursor.fetchall()
            for row in records:
                self.player_A_active_poke_move_3_id = row[0]
                self.player_A_active_poke_move_3_name = row[1]
                self.player_A_active_poke_move_3_name = f"{self.player_A_active_poke_move_3_name}".title()
                self.player_A_active_poke_move_3_element = row[3]
                self.player_A_active_poke_move_3_power = row[4]
                self.player_A_active_poke_move_3_pp = row[5]
                self.player_A_active_poke_move_3_accuracy = row[6]
                self.player_A_active_poke_move_3_type = row[9]
                self.player_A_active_poke_move_3_effect = row[10]

            if self.player_A_active_poke_move_3_type == 1:
                self.poke_move_3_sprite.blit(status_attack_icon, (4, 22))  # type of attack
            elif self.player_A_active_poke_move_3_type == 2:
                self.poke_move_3_sprite.blit(damage_attack_icon, (4, 22))  # type of attack
            elif self.player_A_active_poke_move_3_type == 3:
                self.poke_move_3_sprite.blit(special_attack_icon, (4, 22))  # type of attack
            self.element_poke_getter(self.player_A_active_poke_move_3_element, self.poke_move_3_sprite)
            self.player_A_active_poke_move_3_name_sprite = font_small.render(
                self.player_A_active_poke_move_3_name, True, (255, 255, 255)
            )
            # setting pp of move
            self.player_A_active_poke_move_3_pp_str = \
                f"{self.player_A_active_poke.pp_3}/{self.player_A_active_poke_move_3_pp}"
            self.player_A_active_poke_move_3_pp_str = self.zero_adder_to_number(
                self.player_A_active_poke_move_3_pp_str, 5, "space"
            )
            self.player_A_active_poke_move_3_pp_str = font_small.render(
                self.player_A_active_poke_move_3_pp_str, True, (255, 255, 255)
            )
            self.poke_move_3_sprite.blit(self.player_A_active_poke_move_3_pp_str, (130, 22))
            self.poke_move_3_sprite.blit(self.player_A_active_poke_move_3_name_sprite, (5, 5))

            # getting desc about move
            for id_of_json_move, data in moves.items():
                if data['name'] == self.move_word(self.player_A_active_poke_move_3_name):
                    self.player_A_active_poke_move_3_desc = data["desc"]
            self.player_A_active_poke_move_3_acc_text = f"ACC: {self.player_A_active_poke_move_3_accuracy}"
            self.player_A_active_poke_move_3_pwr_text = f"PWR: {self.player_A_active_poke_move_3_power}"
            self.player_A_active_poke_move_3_acc_sprite = font_small.render(
                self.zero_adder_to_number(self.player_A_active_poke_move_3_acc_text, 8, "space"), True, (255, 255, 255)
            )
            self.player_A_active_poke_move_3_pwr_sprite = font_small.render(
                self.zero_adder_to_number(self.player_A_active_poke_move_3_pwr_text, 8, "space"), True, (255, 255, 255)
            )
            self.moves_sprite.append(self.poke_move_3_sprite)
        if self.player_A_active_poke.move_4:
            self.poke_move_4_sprite = pygame.Surface([170, 40], pygame.HWSURFACE)
            self.poke_move_4_sprite.set_colorkey((0, 0, 0))
            self.poke_move_4_sprite = self.poke_move_4_sprite.convert_alpha()
            self.poke_move_4_sprite.blit(system_photo, (0, 0), [1190, 1640, 170, 40])

            sqlite_select_query = f'SELECT * FROM moves WHERE id like {self.player_A_active_poke.move_4}'
            cursor.execute(sqlite_select_query)
            records = cursor.fetchall()
            for row in records:
                self.player_A_active_poke_move_4_id = row[0]
                self.player_A_active_poke_move_4_name = row[1]
                self.player_A_active_poke_move_4_name = f"{self.player_A_active_poke_move_4_name}".title()
                self.player_A_active_poke_move_4_element = row[3]
                self.player_A_active_poke_move_4_power = row[4]
                self.player_A_active_poke_move_4_pp = row[5]
                self.player_A_active_poke_move_4_accuracy = row[6]
                self.player_A_active_poke_move_4_type = row[9]
                self.player_A_active_poke_move_4_effect = row[10]

            if self.player_A_active_poke_move_4_type == 1:
                self.poke_move_4_sprite.blit(status_attack_icon, (4, 22))  # type of attack
            elif self.player_A_active_poke_move_4_type == 2:
                self.poke_move_4_sprite.blit(damage_attack_icon, (4, 22))  # type of attack
            elif self.player_A_active_poke_move_4_type == 3:
                self.poke_move_4_sprite.blit(special_attack_icon, (4, 22))  # type of attack
            self.element_poke_getter(self.player_A_active_poke_move_4_element, self.poke_move_4_sprite)
            self.player_A_active_poke_move_4_name_sprite = font_small.render(
                self.player_A_active_poke_move_4_name, True, (255, 255, 255)
            )
            # setting pp of move
            self.player_A_active_poke_move_4_pp_str = \
                f"{self.player_A_active_poke.pp_4}/{self.player_A_active_poke_move_4_pp}"
            self.player_A_active_poke_move_4_pp_str = self.zero_adder_to_number(
                self.player_A_active_poke_move_4_pp_str, 5, "space"
            )
            self.player_A_active_poke_move_4_pp_str = font_small.render(
                self.player_A_active_poke_move_4_pp_str, True, (255, 255, 255)
            )
            self.poke_move_4_sprite.blit(self.player_A_active_poke_move_4_pp_str, (130, 22))
            self.poke_move_4_sprite.blit(self.player_A_active_poke_move_4_name_sprite, (5, 5))

            # getting desc about move
            for id_of_json_move, data in moves.items():
                if data['name'] == self.move_word(self.player_A_active_poke_move_4_name):
                    self.player_A_active_poke_move_4_desc = data["desc"]
            self.player_A_active_poke_move_4_acc_text = f"ACC: {self.player_A_active_poke_move_4_accuracy}"
            self.player_A_active_poke_move_4_pwr_text = f"PWR: {self.player_A_active_poke_move_4_power}"
            self.player_A_active_poke_move_4_acc_sprite = font_small.render(
                self.zero_adder_to_number(self.player_A_active_poke_move_4_acc_text, 8, "space"), True, (255, 255, 255)
            )
            self.player_A_active_poke_move_4_pwr_sprite = font_small.render(
                self.zero_adder_to_number(self.player_A_active_poke_move_4_pwr_text, 8, "space"), True, (255, 255, 255)
            )

            self.moves_sprite.append(self.poke_move_4_sprite)
        self.choose_attack_text = "Choose Attack"
        self.choose_attack_sprite = font_large.render(self.choose_attack_text, True, (255, 255, 255))
        cursor.close()
        sqlite_connection.close()

        # setting poke_opponent moves
        sqlite_connection = sqlite3.connect(resource_path(f'resources/system/database/POKE_DB.db'))
        cursor = sqlite_connection.cursor()
        if self.player_B_active_poke.move_1:
            sqlite_select_query = f'SELECT * FROM moves WHERE id like {self.player_B_active_poke.move_1}'
            cursor.execute(sqlite_select_query)
            records = cursor.fetchall()
            for row in records:
                self.player_B_active_poke_move_1_id = row[0]
                self.player_B_active_poke_move_1_name = row[1]
                self.player_B_active_poke_move_1_name = f"{self.player_A_active_poke_move_1_name}".title()
                self.player_B_active_poke_move_1_element = row[3]
                self.player_B_active_poke_move_1_power = row[4]
                self.player_B_active_poke_move_1_pp = row[5]
                self.player_B_active_poke_move_1_accuracy = row[6]
                self.player_B_active_poke_move_1_type = row[9]
                self.player_B_active_poke_move_1_effect = row[10]
        if self.player_B_active_poke.move_2:
            sqlite_select_query = f'SELECT * FROM moves WHERE id like {self.player_B_active_poke.move_2}'
            cursor.execute(sqlite_select_query)
            records = cursor.fetchall()
            for row in records:
                self.player_B_active_poke_move_2_id = row[0]
                self.player_B_active_poke_move_2_name = row[1]
                self.player_B_active_poke_move_2_name = f"{self.player_A_active_poke_move_2_name}".title()
                self.player_B_active_poke_move_2_element = row[3]
                self.player_B_active_poke_move_2_power = row[4]
                self.player_B_active_poke_move_2_pp = row[5]
                self.player_B_active_poke_move_2_accuracy = row[6]
                self.player_B_active_poke_move_2_type = row[9]
                self.player_B_active_poke_move_2_effect = row[10]
        if self.player_B_active_poke.move_3:
            sqlite_select_query = f'SELECT * FROM moves WHERE id like {self.player_B_active_poke.move_3}'
            cursor.execute(sqlite_select_query)
            records = cursor.fetchall()
            for row in records:
                self.player_B_active_poke_move_3_id = row[0]
                self.player_B_active_poke_move_3_name = row[1]
                self.player_B_active_poke_move_3_name = f"{self.player_A_active_poke_move_3_name}".title()
                self.player_B_active_poke_move_3_element = row[3]
                self.player_B_active_poke_move_3_power = row[4]
                self.player_B_active_poke_move_3_pp = row[5]
                self.player_B_active_poke_move_3_accuracy = row[6]
                self.player_B_active_poke_move_3_type = row[9]
                self.player_B_active_poke_move_3_effect = row[10]
        if self.player_B_active_poke.move_4:
            sqlite_select_query = f'SELECT * FROM moves WHERE id like {self.player_B_active_poke.move_4}'
            cursor.execute(sqlite_select_query)
            records = cursor.fetchall()
            for row in records:
                self.player_B_active_poke_move_4_id = row[0]
                self.player_B_active_poke_move_4_name = row[1]
                self.player_B_active_poke_move_4_name = f"{self.player_A_active_poke_move_4_name}".title()
                self.player_B_active_poke_move_4_element = row[3]
                self.player_B_active_poke_move_4_power = row[4]
                self.player_B_active_poke_move_4_pp = row[5]
                self.player_B_active_poke_move_4_accuracy = row[6]
                self.player_B_active_poke_move_4_type = row[9]
                self.player_B_active_poke_move_4_effect = row[10]
        cursor.close()
        sqlite_connection.close()

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

    def action_func(self, action_A, action_B):
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
        if self.action_A == "attack" and self.action_B == "attack":
            # надо бы придумать сценарий из функций (конец файла)
            if self.player_A_active_poke.STAT_SPD >= self.player_B_active_poke.STAT_SPD:
                exec(f"self.damage_counter(self.player_A_active_poke, "
                     f"self.player_A_active_poke_move_{self.selected_A}_element,"
                     f" self.player_A_active_poke_move_{self.selected_A}_type,"
                     f"self.player_B_active_poke, self.player_A_active_poke_move_{self.selected_A}_power,"
                     f"self.player_A_active_poke.STAT_ATK, self.player_A_active_poke.STAT_SPATK,"
                     f"self.player_B_active_poke.STAT_DEF, self.player_B_active_poke.STAT_SPDEF)")
                # !!!!!! here we need check HP of poke
                exec(f"self.damage_counter(self.player_B_active_poke, "
                     f"self.player_B_active_poke_move_{self.selected_B}_element,"
                     f"self.player_B_active_poke_move_{self.selected_B}_type, self.player_A_active_poke,"
                     f"self.player_B_active_poke_move_{self.selected_B}_power,"
                     f"self.player_B_active_poke.STAT_ATK,"
                     f"self.player_B_active_poke.STAT_SPATK,"
                     f"self.player_A_active_poke.STAT_DEF,"
                     f"self.player_A_active_poke.STAT_SPDEF)")
            else:
                exec(f"self.damage_counter(self.player_B_active_poke,"
                     f"self.player_B_active_poke_move_{self.selected_B}_element,"
                     f"self.player_B_active_poke_move_{self.selected_B}_type, self.player_A_active_poke,"
                     f"self.player_B_active_poke_move_{self.selected_B}_power,"
                     f"self.player_B_active_poke.STAT_ATK,"
                     f"self.player_B_active_poke.STAT_SPATK,"
                     f"self.player_A_active_poke.STAT_DEF,"
                     f"self.player_A_active_poke.STAT_SPDEF)")
                # !!!!!! here we need check HP of poke
                exec(f"self.damage_counter(self.player_A_active_poke,"
                     f"self.player_A_active_poke_move_{self.selected_A}_element,"
                     f" self.player_A_active_poke_move_{self.selected_A}_type,"
                     f"self.player_B_active_poke, self.player_A_active_poke_move_{self.selected_A}_power,"
                     f"self.player_A_active_poke.STAT_ATK, self.player_A_active_poke.STAT_SPATK,"
                     f"self.player_B_active_poke.STAT_DEF, self.player_B_active_poke.STAT_SPDEF)")
            self.action_A = None
            self.action_B = None

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

        # checking mouse on "attack" menu
        if self.menu_type == "attack":
            if self.player_A_active_poke.move_1:
                if self.poke_move_1_pos[0] < x_mouse < (self.poke_move_1_pos[0] + 170) and \
                        self.poke_move_1_pos[1] < y_mouse < (self.poke_move_1_pos[1] + 40):
                    self.image.blit(self.move_desc_surface, (410, 39))
                    self.renderTextCenteredAt(self.player_A_active_poke_move_1_desc, font_small, (255, 255, 255),
                                              502, 42, self.image, 170, "center")
                    self.image.blit(self.player_A_active_poke_move_1_acc_sprite, (440, 100))
                    self.image.blit(self.player_A_active_poke_move_1_pwr_sprite, (500, 100))
            if self.player_A_active_poke.move_2:
                if self.poke_move_2_pos[0] < x_mouse < (self.poke_move_2_pos[0] + 170) and \
                        self.poke_move_2_pos[1] < y_mouse < (self.poke_move_2_pos[1] + 40):
                    self.image.blit(self.move_desc_surface, (410, 89))
                    self.renderTextCenteredAt(self.player_A_active_poke_move_2_desc, font_small, (255, 255, 255),
                                              502, 92, self.image, 170, "center")
                    self.image.blit(self.player_A_active_poke_move_2_acc_sprite, (440, 150))
                    self.image.blit(self.player_A_active_poke_move_2_pwr_sprite, (500, 150))
            if self.player_A_active_poke.move_3:
                if self.poke_move_3_pos[0] < x_mouse < (self.poke_move_3_pos[0] + 170) and \
                        self.poke_move_3_pos[1] < y_mouse < (self.poke_move_3_pos[1] + 40):
                    self.image.blit(self.move_desc_surface, (410, 129))
                    self.renderTextCenteredAt(self.player_A_active_poke_move_3_desc, font_small, (255, 255, 255),
                                              502, 132, self.image, 170, "center")
                    self.image.blit(self.player_A_active_poke_move_3_acc_sprite, (440, 190))
                    self.image.blit(self.player_A_active_poke_move_3_pwr_sprite, (500, 190))
            if self.player_A_active_poke.move_4:
                if self.poke_move_4_pos[0] < x_mouse < (self.poke_move_4_pos[0] + 170) and \
                        self.poke_move_4_pos[1] < y_mouse < (self.poke_move_4_pos[1] + 40):
                    self.image.blit(self.move_desc_surface, (410, 179))
                    self.renderTextCenteredAt(self.player_A_active_poke_move_4_desc, font_small, (255, 255, 255),
                                              502, 182, self.image, 170, "center")
                    self.image.blit(self.player_A_active_poke_move_4_acc_sprite, (440, 240))
                    self.image.blit(self.player_A_active_poke_move_4_pwr_sprite, (500, 240))

    def npc_move_setter(self):
        attack = 0
        selected_move = 0

        # checking attack moves
        if self.player_B_active_poke.move_1:
            if self.player_B_active_poke.pp_1 != 0:
                damage_to_poke = self.damage_counter(self.player_B_active_poke,
                                                     self.player_B_active_poke_move_1_element,
                                                     self.player_B_active_poke_move_1_type, self.player_A_active_poke,
                                                     self.player_B_active_poke_move_1_power,
                                                     self.player_B_active_poke.STAT_ATK,
                                                     self.player_B_active_poke.STAT_SPATK,
                                                     self.player_A_active_poke.STAT_DEF,
                                                     self.player_A_active_poke.STAT_SPDEF)
                if damage_to_poke > attack:
                    attack = damage_to_poke
                    selected_move = 1
        if self.player_B_active_poke.move_2:
            if self.player_B_active_poke.pp_2 != 0:
                damage_to_poke = self.damage_counter(self.player_B_active_poke,
                                                     self.player_B_active_poke_move_2_element,
                                                     self.player_B_active_poke_move_2_type, self.player_A_active_poke,
                                                     self.player_B_active_poke_move_2_power,
                                                     self.player_B_active_poke.STAT_ATK,
                                                     self.player_B_active_poke.STAT_SPATK,
                                                     self.player_A_active_poke.STAT_DEF,
                                                     self.player_A_active_poke.STAT_SPDEF)
                if damage_to_poke > attack:
                    attack = damage_to_poke
                    selected_move = 2
        if self.player_B_active_poke.move_3:
            if self.player_B_active_poke.pp_3 != 0:
                damage_to_poke = self.damage_counter(self.player_B_active_poke,
                                                     self.player_B_active_poke_move_3_element,
                                                     self.player_B_active_poke_move_3_type, self.player_A_active_poke,
                                                     self.player_B_active_poke_move_3_power,
                                                     self.player_B_active_poke.STAT_ATK,
                                                     self.player_B_active_poke.STAT_SPATK,
                                                     self.player_A_active_poke.STAT_DEF,
                                                     self.player_A_active_poke.STAT_SPDEF)
                if damage_to_poke > attack:
                    attack = damage_to_poke
                    selected_move = 3
        if self.player_B_active_poke.move_4:
            if self.player_B_active_poke.pp_4 != 0:
                damage_to_poke = self.damage_counter(self.player_B_active_poke,
                                                     self.player_B_active_poke_move_4_element,
                                                     self.player_B_active_poke_move_4_type, self.player_A_active_poke,
                                                     self.player_B_active_poke_move_4_power,
                                                     self.player_B_active_poke.STAT_ATK,
                                                     self.player_B_active_poke.STAT_SPATK,
                                                     self.player_A_active_poke.STAT_DEF,
                                                     self.player_A_active_poke.STAT_SPDEF)
                if damage_to_poke > attack:
                    selected_move = 4

        # checking status moves
        if self.player_B_active_poke.move_1:
            if self.player_B_active_poke.pp_1 != 0:
                if self.player_B_active_poke_move_1_type == 1:
                    if random.random() <= 0.2:
                        selected_move = 1
        if self.player_B_active_poke.move_2:
            if self.player_B_active_poke.pp_2 != 0:
                if self.player_B_active_poke_move_2_type == 1:
                    if random.random() <= 0.2:
                        selected_move = 2
        if self.player_B_active_poke.move_3:
            if self.player_B_active_poke.pp_3 != 0:
                if self.player_B_active_poke_move_3_type == 1:
                    if random.random() <= 0.2:
                        selected_move = 3
        if self.player_B_active_poke.move_4:
            if self.player_B_active_poke.pp_4 != 0:
                if self.player_B_active_poke_move_4_type == 1:
                    if random.random() <= 0.2:
                        selected_move = 4
        # if we don't select move
        if selected_move == 0:
            list_of_poke = []
            if self.player_B_poke_1 and self.player_B_active_poke != self.player_B_poke_1 and self.player_B_poke_1.HP != 0:
                list_of_poke.append(1)
            if self.player_B_poke_2 and self.player_B_active_poke != self.player_B_poke_2 and self.player_B_poke_2.HP != 0:
                list_of_poke.append(2)
            if self.player_B_poke_3 and self.player_B_active_poke != self.player_B_poke_3 and self.player_B_poke_3.HP != 0:
                list_of_poke.append(3)
            if self.player_B_poke_4 and self.player_B_active_poke != self.player_B_poke_4 and self.player_B_poke_4.HP != 0:
                list_of_poke.append(4)
            if self.player_B_poke_5 and self.player_B_active_poke != self.player_B_poke_5 and self.player_B_poke_5.HP != 0:
                list_of_poke.append(5)
            if self.player_B_poke_6 and self.player_B_active_poke != self.player_B_poke_6 and self.player_B_poke_6.HP != 0:
                list_of_poke.append(6)

            self.action_B = "change"
            self.selected_B = random.choice(list_of_poke)
        else:
            self.action_B = "attack"
            self.selected_B = selected_move

    def press_checker(self, e_pos_x, e_pos_y):
        # buttons condition
        if self.battle_status == "waiting":
            if self.surrender_button_x[0] <= e_pos_x <= self.surrender_button_x[1] and \
                    self.surrender_button_y[0] <= e_pos_y <= self.surrender_button_y[1]:
                self.menu_type = None
                self.action_A = "surrender"
            if self.attack_button_x[0] <= e_pos_x <= self.attack_button_x[1] and \
                    self.attack_button_y[0] <= e_pos_y <= self.attack_button_y[1]:
                self.menu_type = "attack"

            # if we select attack move
            if self.menu_type == "attack":
                if self.poke_move_1_pos[0] < e_pos_x < (self.poke_move_1_pos[0] + 170) and \
                        self.poke_move_1_pos[1] < e_pos_y < (self.poke_move_1_pos[1] + 40):
                    self.selected_A = 1
                    self.action_A = "attack"
            if self.menu_type == "attack":
                if self.poke_move_2_pos[0] < e_pos_x < (self.poke_move_2_pos[0] + 170) and \
                        self.poke_move_2_pos[1] < e_pos_y < (self.poke_move_2_pos[1] + 40):
                    self.selected_A = 2
                    self.action_A = "attack"
            if self.menu_type == "attack":
                if self.poke_move_3_pos[0] < e_pos_x < (self.poke_move_3_pos[0] + 170) and \
                        self.poke_move_3_pos[1] < e_pos_y < (self.poke_move_3_pos[1] + 40):
                    self.selected_A = 3
                    self.action_A = "attack"
            if self.menu_type == "attack":
                if self.poke_move_4_pos[0] < e_pos_x < (self.poke_move_4_pos[0] + 170) and \
                        self.poke_move_4_pos[1] < e_pos_y < (self.poke_move_4_pos[1] + 40):
                    self.selected_A = 4
                    self.action_A = "attack"

    def menu_updater(self):
        if self.menu_type == "attack":
            y = 59
            for i in self.moves_sprite:
                self.image.blit(i, [599, y])
                pygame.draw.rect(self.image, (105, 105, 105), [599, y, 170, 40], 2)
                y += 47
            self.image.blit(self.choose_attack_sprite, (618, 260))  # choose attack sprite

    def update(self, screen, *args):
        # update buttons pos
        self.surrender_button_x = [self.rect.x + 700, self.rect.x + 770]
        self.surrender_button_y = [self.rect.y + 400, self.rect.y + 456]
        self.attack_button_x = [self.rect.x + 600, self.rect.x + 674]
        self.attack_button_y = [self.rect.y + 310, self.rect.y + 368]

        self.poke_move_1_pos = [self.rect.x + 599, self.rect.y + 59]  # + [170, 40]
        self.poke_move_2_pos = [self.rect.x + 599, self.rect.y + 106]  # + [170, 40]
        self.poke_move_3_pos = [self.rect.x + 599, self.rect.y + 153]  # + [170, 40]
        self.poke_move_4_pos = [self.rect.x + 599, self.rect.y + 200]  # + [170, 40]

        # battle status
        if self.active:
            # getting npc move
            if self.type_of_battle == "npc" and self.action_B is None:
                self.npc_move_setter()

            if self.battle_status == "waiting":
                if self.action_A is None or self.action_B is None:  # BUT HERE MUST BE OR (not and)
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
                    if (self.player_A_active_poke.HP / self.player_A_active_poke.STAT_HP) >= 0.66:
                        self.hp_pokemon_A_sprite = pygame.draw.line(self.image, (0, 200, 64),
                                                                    [self.HP_line_percentage_pokemon_A, 327],
                                                                    [560, 327], 4)
                    elif (self.player_A_active_poke.HP / self.player_A_active_poke.STAT_HP) <= 0.33:
                        self.hp_pokemon_A_sprite = pygame.draw.line(self.image, (220, 50, 50),
                                                                    [self.HP_line_percentage_pokemon_A, 327],
                                                                    [560, 327], 4)
                    else:
                        self.hp_pokemon_A_sprite = pygame.draw.line(self.image, (255, 255, 0),
                                                                    [self.HP_line_percentage_pokemon_A, 327],
                                                                    [560, 327], 4)
                if self.pokemon_hp_B_anim.state != "stopped":
                    self.pokemon_hp_B_anim.blit(self.image, [26, 90])
                else:
                    if (self.player_B_active_poke.HP / self.player_B_active_poke.STAT_HP) >= 0.66:
                        self.hp_pokemon_B_sprite = pygame.draw.line(self.image, (0, 200, 64),
                                                                    [26, 91],
                                                                    [self.HP_line_percentage_pokemon_B, 91], 4)
                    elif (self.player_B_active_poke.HP / self.player_B_active_poke.STAT_HP) <= 0.33:
                        self.hp_pokemon_B_sprite = pygame.draw.line(self.image, (220, 50, 50),
                                                                    [26, 91],
                                                                    [self.HP_line_percentage_pokemon_B, 91], 4)
                    else:
                        self.hp_pokemon_B_sprite = pygame.draw.line(self.image, (255, 255, 0),
                                                                    [26, 91],
                                                                    [self.HP_line_percentage_pokemon_B, 91], 4)
            else:
                self.player_A_active_poke_icon_anim.blit(self.image, [30, 215])

                if (self.player_A_active_poke.HP / self.player_A_active_poke.STAT_HP) >= 0.66:
                    self.hp_pokemon_A_sprite = pygame.draw.line(self.image, (0, 200, 64),
                                                                [self.HP_line_percentage_pokemon_A, 327],
                                                                [560, 327], 4)
                elif (self.player_A_active_poke.HP / self.player_A_active_poke.STAT_HP) <= 0.33:
                    self.hp_pokemon_A_sprite = pygame.draw.line(self.image, (220, 50, 50),
                                                                [self.HP_line_percentage_pokemon_A, 327],
                                                                [560, 327], 4)
                else:
                    self.hp_pokemon_A_sprite = pygame.draw.line(self.image, (255, 255, 0),
                                                                [self.HP_line_percentage_pokemon_A, 327],
                                                                [560, 327], 4)

                if (self.player_B_active_poke.HP / self.player_B_active_poke.STAT_HP) >= 0.66:
                    self.hp_pokemon_B_sprite = pygame.draw.line(self.image, (0, 200, 64),
                                                                [26, 91],
                                                                [self.HP_line_percentage_pokemon_B, 91], 4)
                elif (self.player_B_active_poke.HP / self.player_B_active_poke.STAT_HP) <= 0.33:
                    self.hp_pokemon_B_sprite = pygame.draw.line(self.image, (220, 50, 50),
                                                                [26, 91],
                                                                [self.HP_line_percentage_pokemon_B, 91], 4)
                else:
                    self.hp_pokemon_B_sprite = pygame.draw.line(self.image, (255, 255, 0),
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
                self.image.blit(self.poke_gender_female_sprite, (30, 72))
            self.menu_updater()  # bliting menu
            self.pokeball_icons_draw()  # bliting pokeball icons (mini)
            self.button_hover(args[0][0], args[0][1])  # checking hover possible objects (mouse pos in args)

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
            if (self.player_A_active_poke.HP / self.player_A_active_poke.STAT_HP) >= 0.66:
                exec(f"self.frame_hp_A_drop_{i}.fill((0, 200, 64))")
            elif (self.player_A_active_poke.HP / self.player_A_active_poke.STAT_HP) <= 0.33:
                exec(f"self.frame_hp_A_drop_{i}.fill((220, 50, 50))")
            else:
                exec(f"self.frame_hp_A_drop_{i}.fill((255, 255, 0))")
            exec(f"self.frame_hp_A_{i}.blit(self.frame_hp_A_drop_{i}, [{147 - round(self.hp_drop_A * i)}, 0])")

            exec(f"self.frame_hp_B_{i} = pygame.Surface([147, 4], pygame.SRCALPHA)")
            exec(f"self.frame_hp_B_drop_{i} = pygame.Surface([{round(self.hp_drop_B * i)}, 4])")
            if (self.player_B_active_poke.HP / self.player_B_active_poke.STAT_HP) >= 0.66:
                exec(f"self.frame_hp_B_drop_{i}.fill((0, 200, 64))")
            elif (self.player_B_active_poke.HP / self.player_B_active_poke.STAT_HP) <= 0.33:
                exec(f"self.frame_hp_B_drop_{i}.fill((220, 50, 50))")
            else:
                exec(f"self.frame_hp_B_drop_{i}.fill((255, 255, 0))")
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

    @staticmethod
    def element_poke_getter(id_element_move, self_image):
        def element_drawer(element):
            if element == 3:
                return flying_type
            elif element == 18:
                return fairy_type
            elif element == 9:
                return steel_type
            elif element == 4:
                return poison_type
            elif element == 8:
                return ghost_type
            elif element == 13:
                return electric_type
            elif element == 15:
                return ice_type
            elif element == 14:
                return psychic_type
            elif element == 16:
                return dragon_type
            elif element == 12:
                return grass_type
            elif element == 6:
                return rock_type
            elif element == 1:
                return normal_type
            elif element == 11:
                return water_type
            elif element == 17:
                return dark_type
            elif element == 7:
                return bug_type
            elif element == 2:
                return fight_type
            elif element == 10:
                return fire_type
            elif element == 5:
                return ground_type

        self_image.blit(element_drawer(id_element_move), (36, 24))

    @staticmethod
    def move_word(word):
        word_lst = word.split("-")
        word = " ".join(word_lst)
        return word

    @staticmethod
    def renderTextCenteredAt(text, font, colour, x, y, screen, allowed_width, position):
        # first, split the text into words
        words = text.split()

        # now, construct lines out of these words
        lines = []
        while len(words) > 0:
            # get as many words as will fit within allowed_width
            line_words = []
            while len(words) > 0:
                line_words.append(words.pop(0))
                fw, fh = font.size(' '.join(line_words + words[:1]))
                if fw > allowed_width:
                    break

            # add a line consisting of those words
            line = ' '.join(line_words)
            lines.append(line)

        # now we've split our text into lines that fit into the width, actually
        # render them

        # we'll render each line below the last, so we need to keep track of
        # the culmative height of the lines we've rendered so far
        y_offset = 0
        for line in lines:
            fw, fh = font.size(line)

            # (tx, ty) is the top-left of the font surface
            if position == "center":
                tx = x - fw / 2
                ty = y + y_offset
            elif position == "left":
                tx = x
                ty = y + y_offset
            else:
                tx = x - fw / 2
                ty = y + y_offset

            font_surface = font.render(line, True, colour)
            screen.blit(font_surface, (tx, ty))

            y_offset += fh

    def damage_counter(self, active_poke, move_element, move_type, opponent_poke, power, Atk, Spatk, Def, Spdef, other=1):
        # 'Weather' is the damage multiplier that is 1 by default but will become 1.5 if
        # the attacker is using a Water-type move while Rain is active or if they use
        # a Fire-type move when Sunny Day is active, and, additionally,
        # can become 0.5 if the attacker uses a Water-type move while Sunny Day is active or
        # if they use a Fire-type move while Rain is active
        if self.weather == "rain":
            if move_element == 17:
                weather = 1.5
            elif move_element == 10:
                weather = 0.5
            else:
                weather = 1
        elif self.weather == "sunny":
            if move_element == 17:
                weather = 0.5
            elif move_element == 10:
                weather = 1.5
            else:
                weather = 1
        else:
            weather = 1

        # 'Critical' will be 1 in most cases but is the multiplier applied when the attacker lands a move
        # that turns out to be a Critical Hit, which will make this factor become 1.5
        if random.random() >= 0.8:
            critical = 1.5
        else:
            critical = 1

        # 'STAB' stands for Same Type Attack Bonus and will be 1 unless the attacker uses a move that matches their
        # type, in which case this value will become 1.5 (or 2 if the attacker has the Adaptability ability)
        STAB = 1
        for i in pokedex[active_poke.id_pokedex]["Types"]:
            if move_element == i:
                STAB = 1.5

        # random is a chaotic value between 0.85 and 1 that is determined by RNG (random number generator)
        # and represents the natural variance that can occur in battle, which can only potentially decrease
        # a move's overall damage and is considered by many hardcore gamers to be a
        # prime example of "artificial difficulty" in the franchise
        random_num = round(random.uniform(0.75, 1), 2)

        # Type refers to the type effectiveness of a move as determined by the type of the attacker's move as well as
        # the type of the defending Pokémon, which result in this factor being one of the following:
        # 0 if the defender is immune, 0.25 if the defender is x2 resistant, 0.5 if the defender is resistant,
        # 1 if the defender is neutral, 2 if the defender is weak to the attacking type, or
        # 4 if the defender is x2 weak to the attacking type
        type_number = 1  # default number
        for i in pokedex[opponent_poke.id_pokedex]["Types"]:
            if i == "Normal":
                if move_element == 2:
                    type_number = type_number * 2
                elif move_element == 8:
                    type_number = 0

            elif i == "Fighting":
                if move_element in [3, 14, 18]:
                    type_number = type_number * 2
                elif move_element in [6, 7, 17]:
                    type_number = type_number / 2

            elif i == "Flying":
                if move_element in [6, 13, 15]:
                    type_number = type_number * 2
                elif move_element in [2, 12]:
                    type_number = type_number / 2
                elif move_element == 5:
                    type_number = 0

            elif i == "Poison":
                if move_element in [5, 14]:
                    type_number = type_number * 2
                elif move_element in [2, 4, 7, 12, 18]:
                    type_number = type_number / 2

            elif i == "Ground":
                if move_element in [11, 12, 15]:
                    type_number = type_number * 2
                elif move_element in [4, 6]:
                    type_number = type_number / 2
                elif move_element == 13:
                    type_number = 0

            elif i == "Rock":
                if move_element in [2, 5, 9, 11, 12]:
                    type_number = type_number * 2
                elif move_element in [1, 3, 4, 10]:
                    type_number = type_number / 2

            elif i == "Bug":
                if move_element in [3, 6, 10]:
                    type_number = type_number * 2
                elif move_element in [2, 5, 12]:
                    type_number = type_number / 2

            elif i == "Ghost":
                if move_element in [8, 17]:
                    type_number = type_number * 2
                elif move_element in [4, 7]:
                    type_number = type_number / 2
                elif move_element in [1, 2]:
                    type_number = 0

            elif i == "Steel":
                if move_element in [2, 5, 10]:
                    type_number = type_number * 2
                elif move_element in [1, 3, 6, 7, 9, 12, 14, 15, 16, 18]:
                    type_number = type_number / 2
                elif move_element == 4:
                    type_number = 0

            elif i == "Fire":
                if move_element in [5, 6, 11]:
                    type_number = type_number * 2
                elif move_element in [7, 9, 10, 12, 15, 18]:
                    type_number = type_number / 2

            elif i == "Water":
                if move_element in [12, 13]:
                    type_number = type_number * 2
                elif move_element in [9, 10, 11, 15]:
                    type_number = type_number / 2

            elif i == "Grass":
                if move_element in [3, 4, 7, 10, 15]:
                    type_number = type_number * 2
                elif move_element in [5, 11, 12, 13]:
                    type_number = type_number / 2

            elif i == "Electric":
                if move_element == 5:
                    type_number = type_number * 2
                elif move_element in [3, 9, 13]:
                    type_number = type_number / 2

            elif i == "Psychic":
                if move_element in [7, 8, 17]:
                    type_number = type_number * 2
                elif move_element in [2, 14]:
                    type_number = type_number / 2

            elif i == "Ice":
                if move_element in [2, 6, 9, 10]:
                    type_number = type_number * 2
                elif move_element == 15:
                    type_number = type_number / 2

            elif i == "Dragon":
                if move_element in [15, 17, 18]:
                    type_number = type_number * 2
                elif move_element in [10, 11, 12, 13]:
                    type_number = type_number / 2

            elif i == "Dark":
                if move_element in [2, 18]:
                    type_number = type_number * 2
                elif move_element in [7, 8]:
                    type_number = type_number / 2
                elif move_element == 14:
                    type_number = 0

            elif i == "Fairy":
                if move_element in [4, 9]:
                    type_number = type_number * 2
                elif move_element in [2, 17]:
                    type_number = type_number / 2
                elif move_element == 16:
                    type_number = 0

        #  Burn is normally 1 but will become 0.5 if the attacker has the Burned status condition
        #  and uses a physical move
        if opponent_poke.status == "burn" and move_type == 2:
            burn = 0.5
        else:
            burn = 1

        # Check type of attacks
        if move_type == 2:
            A = Atk
            D = Def
        else:
            A = Spatk
            D = Spdef

        damage = ((((active_poke.LV * 2) / 5 + 2) * power * (A / D) / 50) + 2) * burn * weather * critical * STAB * \
                 random_num * type_number * other
        print(f"critical - {critical}, STAB-{STAB}, random_num-{random_num}, type_num-{type_number}")
        print(f" {opponent_poke} takes {damage} dmg")  # !!!!! над обработать
        return damage
