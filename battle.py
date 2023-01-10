import random
import sys
import os
import pygame
from pygame import *
import sqlite3
from setting import Pokemon, font_standart


def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


system_photo = pygame.image.load(resource_path("resources/system/sprites/MainUIAtlasTrilinear.png"))


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
        self.image = Surface([791, 750], pygame.SRCALPHA)  # Battle Sprite
        self.image.blit(self.background_img, [0, 0])
        self.rect = Rect(x, y, 791, 750)

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
        right_hp_background = pygame.Surface([157, 41], pygame.SRCALPHA)
        left_hp_background = pygame.Surface([157, 41], pygame.SRCALPHA)
        right_hp_background.blit(system_photo, (0, 0), [1843, 1237, 157, 41])
        left_hp_background.blit(system_photo, (0, 0), [1843, 1279, 157, 41])
        self.image.blit(self.battle_location_background, [9, 50])
        self.image.blit(right_hp_background, [20, 70])
        self.image.blit(left_hp_background, [410, 305])

        # setting pokeballs icons
        poke_icon_true = pygame.Surface([19, 19], pygame.SRCALPHA)
        poke_icon_false = pygame.Surface([19, 19], pygame.SRCALPHA)
        poke_icon_none = pygame.Surface([19, 19], pygame.SRCALPHA)
        poke_icon_true.blit(system_photo, (0, 0), [704, 123, 19, 19])
        poke_icon_false.blit(system_photo, (0, 0), [704, 12, 19, 19])
        poke_icon_none.blit(system_photo, (0, 0), [1500, 400, 20, 21])

        # setting buttons icons
        surrender_icon_none = pygame.Surface([70, 56], pygame.SRCALPHA)
        surrender_icon_none.blit(system_photo, (0, 0), [725, 266, 70, 56])
        surrender_icon_hover = pygame.Surface([70, 56], pygame.SRCALPHA)
        surrender_icon_hover.blit(system_photo, (0, 0), [725, 210, 70, 56])
        self.image.blit(surrender_icon_none, (300, 300))

        self.active = True  # Battle status (going/end)
        self.battle_status = "waiting"  # status of battle
        self.action = False  # action mechanics
        self.action_A = None  # action of player A
        self.action_B = None  # action of player B

        self.time_delay = 120
        self.log = None  # message mechanics
        self.text = ""  # message mechanics
        self.text_surface = None
        self.letter_index = 0
        self.color = (0, 0, 0)

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
                    if i == 1:
                        self.image.blit(poke_icon_none, [432, 355])
                    elif i == 2:
                        self.image.blit(poke_icon_none, [454, 355])
                    elif i == 3:
                        self.image.blit(poke_icon_none, [476, 355])
                    elif i == 4:
                        self.image.blit(poke_icon_none, [498, 355])
                    elif i == 5:
                        self.image.blit(poke_icon_none, [520, 355])
                    elif i == 6:
                        self.image.blit(poke_icon_none, [542, 355])
                else:
                    exec(f'self.player_A_poke_{i} = Pokemon(i, "player_pokes.db")')
                    if i == 1:
                        if self.player_A_poke_1.HP == 0:
                            self.image.blit(poke_icon_false, [432, 355])
                        else:
                            self.image.blit(poke_icon_true, [432, 355])
                    elif i == 2:
                        if self.player_A_poke_2.HP == 0:
                            self.image.blit(poke_icon_false, [454, 355])
                        else:
                            self.image.blit(poke_icon_true, [454, 355])
                    elif i == 3:
                        if self.player_A_poke_3.HP == 0:
                            self.image.blit(poke_icon_false, [476, 355])
                        else:
                            self.image.blit(poke_icon_true, [476, 355])
                    elif i == 4:
                        if self.player_A_poke_4.HP == 0:
                            self.image.blit(poke_icon_false, [498, 355])
                        else:
                            self.image.blit(poke_icon_true, [498, 355])
                    elif i == 5:
                        if self.player_A_poke_5.HP == 0:
                            self.image.blit(poke_icon_false, [520, 355])
                        else:
                            self.image.blit(poke_icon_true, [520, 355])
                    elif i == 6:
                        if self.player_A_poke_6.HP == 0:
                            self.image.blit(poke_icon_false, [542, 355])
                        else:
                            self.image.blit(poke_icon_true, [542, 355])

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
                        if i == 1:
                            self.image.blit(poke_icon_none, [26, 120])
                        elif i == 2:
                            self.image.blit(poke_icon_none, [48, 120])
                        elif i == 3:
                            self.image.blit(poke_icon_none, [70, 120])
                        elif i == 4:
                            self.image.blit(poke_icon_none, [92, 120])
                        elif i == 5:
                            self.image.blit(poke_icon_none, [114, 120])
                        elif i == 6:
                            self.image.blit(poke_icon_none, [136, 120])
                    else:
                        exec(f'self.player_B_poke_{i} = Pokemon(i, "npc_pokes.db",'
                             f'"SELECT * FROM [{i}] WHERE id_npc like {opponent[1]}")')
                        if i == 1:
                            if self.player_B_poke_1.HP == 0:
                                self.image.blit(poke_icon_false, [26, 120])
                            else:
                                self.image.blit(poke_icon_true, [26, 120])
                        elif i == 2:
                            if self.player_B_poke_2.HP == 0:
                                self.image.blit(poke_icon_false, [48, 120])
                            else:
                                self.image.blit(poke_icon_true, [48, 120])
                        elif i == 3:
                            if self.player_B_poke_3.HP == 0:
                                self.image.blit(poke_icon_false, [70, 120])
                            else:
                                self.image.blit(poke_icon_true, [70, 120])
                        elif i == 4:
                            if self.player_B_poke_4.HP == 0:
                                self.image.blit(poke_icon_false, [92, 120])
                            else:
                                self.image.blit(poke_icon_true, [92, 120])
                        elif i == 5:
                            if self.player_B_poke_5.HP == 0:
                                self.image.blit(poke_icon_false, [114, 120])
                            else:
                                self.image.blit(poke_icon_true, [114, 120])
                        elif i == 6:
                            if self.player_B_poke_6.HP == 0:
                                self.image.blit(poke_icon_false, [136, 120])
                            else:
                                self.image.blit(poke_icon_true, [136, 120])

                cursor.close()
                sqlite_connection.close()

            except sqlite3.Error as error:
                print("Ошибка при работе с SQLite", error)

        self.player_A_active_poke = self.player_A_poke_1
        self.player_B_active_poke = self.player_B_poke_1

        # bliting poke_icons on field
        self.player_A_active_poke_icon_standart = pygame.image.load(
            resource_path(f"resources/pokemon/"
                          f"{self.player_A_active_poke.type_poke}/{self.player_A_active_poke.id_pokedex}/me.png"))
        self.player_B_active_poke_icon = pygame.image.load(
            resource_path(f"resources/pokemon/"
                          f"{self.player_B_active_poke.type_poke}/{self.player_B_active_poke.id_pokedex}/foe.png"))
        self.player_A_active_poke_icon = pygame.transform.scale(self.player_A_active_poke_icon_standart, (192, 192))
        # self.player_B_active_poke_icon = pygame.transform.scale(self.player_B_active_poke_icon_standart, (192, 192))
        self.image.blit(self.player_A_active_poke_icon, [30, 215])
        self.image.blit(self.player_B_active_poke_icon, [370, 82])
        self.text_surface = font_standart.render(self.text, True, self.color)

        if type_of_battle == "wild_poke":
            catch_success = False

        # # TEST
        # self.item_effect(2)

        if self.active:
            if self.battle_status == "waiting":
                if self.action_A is None or self.action_B is None:
                    pass
                else:
                    self.battle_status = "action"
            if self.battle_status == "action":
                if not self.action:
                    self.action_func(self.action_A, self.action_B)
                    self.action = True
                else:
                    pass

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
        if action_A == "surrender" or action_B == "surrender":
            self.log_message("you are surrender!")
            self.kill()
        # if action_A == "change" or action_A == "item":
        #     if action_B == "change" or action_B == "item":
        #         if self.player_A_active_poke.STAT_SPD > self.player_B_active_poke.STAT_SPD:
        #
        #         elif self.player_A_active_poke.STAT_SPD < self.player_B_active_poke.STAT_SPD:
        #
        #         else:

    def battle_status_changer(self, status):
        self.battle_status = status

    def start_battle(self):
        self.battle_log.append("")

    def log_message(self, message):
        self.log = message
        if self.time_delay == 0:
            if self.action:
                self.battle_status = "waiting"
                self.action = False
            self.time_delay = 120
        else:
            if self.letter_index != len(self.log):
                self.text += self.log[self.letter_index]
                self.letter_index += 1
            else:
                self.time_delay -= 1
            self.text_surface = font_standart.render(self.text, True, self.color)
            pass

    def button_hover(self, x_mouse, y_mouse):
        if 300 < x_mouse < 400 and 100 < y_mouse < 200:
            print("moused")

    def update(self, screen, *args):
        self.button_hover(args[0][0], args[0][1])
        self.image.blit(self.text_surface, (100, 100))
        screen.blit(self.image, (self.rect.x, self.rect.y))
