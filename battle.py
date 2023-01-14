import random
import sys
import os
import pygame
import pyganim
from pygame import *
import sqlite3
from setting import Pokemon


def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


system_photo = pygame.image.load(resource_path("resources/system/sprites/MainUIAtlasTrilinear.png"))
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
        self.battle_log_background = \
            pygame.image.load(resource_path(f"resources/system/sprites/battle_log.png"))
        self.right_hp_background = pygame.Surface([157, 41], pygame.SRCALPHA)
        self.left_hp_background = pygame.Surface([157, 41], pygame.SRCALPHA)
        self.right_hp_background.blit(system_photo, (0, 0), [1843, 1237, 157, 41])
        self.left_hp_background.blit(system_photo, (0, 0), [1843, 1279, 157, 41])
        self.image.blit(self.battle_location_background, [9, 50])
        self.image.blit(self.right_hp_background, [20, 70])
        self.image.blit(self.left_hp_background, [410, 305])

        # setting pokeballs icons
        self.poke_icon_true = pygame.Surface([19, 19], pygame.SRCALPHA)
        self.poke_icon_false = pygame.Surface([19, 19], pygame.SRCALPHA)
        self.poke_icon_none = pygame.Surface([19, 19], pygame.SRCALPHA)
        self.poke_icon_true.blit(system_photo, (0, 0), [704, 123, 19, 19])
        self.poke_icon_false.blit(system_photo, (0, 0), [704, 12, 19, 19])
        self.poke_icon_none.blit(system_photo, (0, 0), [1500, 400, 20, 21])

        # setting buttons icons
        self.surrender_icon_none = pygame.Surface([70, 56], pygame.SRCALPHA)
        self.surrender_icon_none.blit(system_photo, (0, 0), [725, 266, 70, 56])
        self.surrender_icon_hover = pygame.Surface([70, 56], pygame.SRCALPHA)
        self.surrender_icon_hover.blit(system_photo, (0, 0), [725, 210, 70, 56])

        self.surrender_button_x = [self.rect.x + 700, self.rect.x + 770]
        self.surrender_button_y = [self.rect.y + 400, self.rect.y + 456]

        # Action mechanics
        self.active = True  # Battle status (going/end)
        self.battle_status = "waiting"  # status of battle
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

        if type_of_battle == "wild_poke":
            catch_success = False

        # # TEST
        # self.item_effect(2)

    def poke_img_load(self):
        self.player_A_active_poke_icon_standart = pygame.image.load(
            resource_path(f"resources/pokemon/"
                          f"{self.player_A_active_poke.type_poke}/{self.player_A_active_poke.id_pokedex}/me.png"))
        self.player_B_active_poke_icon = pygame.image.load(
            resource_path(f"resources/pokemon/"
                          f"{self.player_B_active_poke.type_poke}/{self.player_B_active_poke.id_pokedex}/foe.png"))
        self.player_A_active_poke_standart = pygame.transform.scale(self.player_A_active_poke_icon_standart,
                                                                    (192, 192))
        self.player_A_active_poke_icon = pygame.Surface([192, 198], pygame.SRCALPHA)
        # create poke anim in battle_background
        self.player_A_active_poke_icon_frame_1 = pygame.Surface([192, 198], pygame.SRCALPHA)
        self.player_A_active_poke_icon_frame_2 = pygame.Surface([192, 198], pygame.SRCALPHA)
        self.player_A_active_poke_icon_frame_1.blit(self.player_A_active_poke_standart, [0, 0])
        self.player_A_active_poke_icon_frame_2.blit(self.player_A_active_poke_standart, [0, 6])
        self.player_A_active_poke_icon_anim = pyganim.PygAnimation([
            (self.player_A_active_poke_icon_frame_1, 0.5),
            (self.player_A_active_poke_icon_frame_2, 0.5)])
        self.player_A_active_poke_icon_anim.play()
        self.image.blit(self.player_B_active_poke_icon, [370, 82])
        self.text_surface = font.render(self.text, True, self.color)

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
            self.player_A_active_poke_icon_anim.pause()
            self.actions_list.append(self.log_message)
            self.arguments_list.append("· You are surrendered!")
            self.actions_list.append(self.delay_func)
            self.arguments_list.append(True)
            self.actions_list.append(self.log_message)
            self.arguments_list.append("· You lost the battle!")
            self.actions_list.append(self.delay_func)
            self.arguments_list.append(True)
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

    def start_battle(self):
        self.battle_log.append("Battle started.")

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

    def delay_func(self, log_clear=False):
        if self.time_delay < 0:
            if log_clear:
                self.text = ""
                self.text_surface = font.render(self.text, True, self.color)
            self.time_delay = 50
            self.current_action_value = False
            self.action_index += 1
        else:
            self.time_delay -= 1

    def button_hover(self, x_mouse, y_mouse):
        if (700 + self.rect.x) < x_mouse < (770 + self.rect.x) and (400 + self.rect.y) < y_mouse < (456 + self.rect.y):
            self.image.blit(self.surrender_icon_hover, (700, 400))
        else:
            self.image.blit(self.surrender_icon_none, (700, 400))

    def press_checker(self, e_pos_x, e_pos_y):
        # close button condition
        if self.surrender_button_x[0] <= e_pos_x <= self.surrender_button_x[1] and \
                self.surrender_button_y[0] <= e_pos_y <= self.surrender_button_y[1]:
            self.action_A = "surrender"

    def update(self, screen, *args):
        # update buttons pos
        self.surrender_button_x = [self.rect.x + 700, self.rect.x + 770]
        self.surrender_button_y = [self.rect.y + 400, self.rect.y + 456]

        # battle status
        if self.active:
            # print(self.battle_status)
            if self.battle_status == "waiting":
                if self.action_A is None and self.action_B is None:  # BUT HERE MUST BE OR (not and)
                    pass
                else:
                    self.battle_status = "action"
            if self.battle_status == "action":
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
                        self.action_index = 0
                        self.current_action = None
                        self.current_arguments = None
                        self.current_action_value = False
                        self.battle_status = "waiting"

            # if battle end
            elif self.battle_status == "end":
                self.active = False
                args[1].world_status_changer("MAIN")  # change status of world
                # args[2].map_changer("from_TestMap_to_TestHouse", "up", 19 * 32, 15 * 32)
                self.kill()

        #
        if self.active:
            self.image.fill((255, 255, 255, 0))
            self.image.blit(self.background_img, [0, 0])

            self.image.blit(self.battle_location_background, [9, 50])
            self.image.blit(self.battle_log_background, [9, 410])
            self.image.blit(self.right_hp_background, [20, 70])
            self.image.blit(self.left_hp_background, [410, 305])

            self.pokeball_icons_draw()
            self.button_hover(args[0][0], args[0][1])  # mouse pos in args

            self.player_A_active_poke_icon_anim.blit(self.image, [30, 215])
            self.image.blit(self.player_B_active_poke_icon, [370, 82])

            self.image.blit(self.text_surface, (30, 425))
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
