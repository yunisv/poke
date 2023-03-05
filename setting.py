import sys
import os
from pygame import *
import pygame
import pickle
import sqlite3
import json
from pokemons import *


def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


with open(resource_path('resources/system/database/Pokedex.json')) as f:
    pokedex = json.load(f)

system_mech = pygame.sprite.Group()  # pygame sprite's group for system
font_standart = pygame.font.Font(resource_path("resources/font/roboto.ttf"), 10)  # setting font
font_small = pygame.font.Font(resource_path("resources/font/roboto.ttf"), 11)  # setting font
font_medium = pygame.font.Font(resource_path("resources/font/roboto.ttf"), 12)  # setting font
font_large = pygame.font.Font(resource_path("resources/font/roboto.ttf"), 20)  # setting font

# loading system photo
system_photo = pygame.image.load(resource_path("resources/system/sprites/MainUIAtlasTrilinear.png"))
system_photo_resized = pygame.transform.scale(system_photo, (1024, 1024))

# create system item's Surfaces
flying_type = pygame.Surface([31, 11], pygame.SRCALPHA)
fairy_type = pygame.Surface([31, 11], pygame.SRCALPHA)
steel_type = pygame.Surface([31, 11], pygame.SRCALPHA)
poison_type = pygame.Surface([31, 11], pygame.SRCALPHA)
ghost_type = pygame.Surface([31, 11], pygame.SRCALPHA)
electric_type = pygame.Surface([31, 11], pygame.SRCALPHA)
ice_type = pygame.Surface([31, 11], pygame.SRCALPHA)
psychic_type = pygame.Surface([31, 11], pygame.SRCALPHA)
dragon_type = pygame.Surface([31, 11], pygame.SRCALPHA)
grass_type = pygame.Surface([31, 11], pygame.SRCALPHA)
rock_type = pygame.Surface([31, 11], pygame.SRCALPHA)
normal_type = pygame.Surface([31, 11], pygame.SRCALPHA)
water_type = pygame.Surface([31, 11], pygame.SRCALPHA)
dark_type = pygame.Surface([31, 11], pygame.SRCALPHA)
bug_type = pygame.Surface([31, 11], pygame.SRCALPHA)
fight_type = pygame.Surface([31, 11], pygame.SRCALPHA)
fire_type = pygame.Surface([31, 11], pygame.SRCALPHA)
ground_type = pygame.Surface([31, 11], pygame.SRCALPHA)

shiny_icon_s = pygame.Surface([10, 14], pygame.SRCALPHA)

status_attack_icon = pygame.Surface([28, 14], pygame.HWSURFACE)
special_attack_icon = pygame.Surface([28, 14], pygame.HWSURFACE)
damage_attack_icon = pygame.Surface([28, 14], pygame.HWSURFACE)

# bliting system images
flying_type.blit(system_photo, (0, 0), [825, 57, 31, 11])
fairy_type.blit(system_photo, (0, 0), [860, 184, 31, 11])
steel_type.blit(system_photo, (0, 0), [860, 197, 31, 11])
poison_type.blit(system_photo, (0, 0), [860, 210, 31, 11])
ghost_type.blit(system_photo, (0, 0), [860, 236, 31, 11])
electric_type.blit(system_photo, (0, 0), [860, 262, 31, 11])
ice_type.blit(system_photo, (0, 0), [860, 275, 31, 11])
psychic_type.blit(system_photo, (0, 0), [860, 288, 31, 11])
dragon_type.blit(system_photo, (0, 0), [860, 301, 31, 11])
grass_type.blit(system_photo, (0, 0), [860, 314, 31, 11])
rock_type.blit(system_photo, (0, 0), [860, 327, 31, 11])
normal_type.blit(system_photo, (0, 0), [1475, 1126, 31, 11])
water_type.blit(system_photo, (0, 0), [1508, 1126, 31, 11])
dark_type.blit(system_photo, (0, 0), [1541, 1126, 31, 11])
bug_type.blit(system_photo, (0, 0), [1547, 1126, 31, 11])
fight_type.blit(system_photo, (0, 0), [1706, 1176, 31, 11])
fire_type.blit(system_photo, (0, 0), [1368, 1172, 31, 11])
ground_type.blit(system_photo, (0, 0), [1335, 1172, 31, 11])

shiny_icon_s.blit(system_photo, (0, 0), [2038, 1713, 10, 14])

special_attack_icon.blit(system_photo, (0, 0), [1754, 1367, 28, 14])
status_attack_icon.blit(system_photo, (0, 0), [1873, 1367, 28, 14])
damage_attack_icon.blit(system_photo, (0, 0), [1844, 1367, 28, 14])


class Pokemon:
    def __init__(self, id_db_poke=None, db=None, query=None, *args):
        # [id, ID, type(shiny), Ability, XP, HP, MOVES_ID[ID, PP], item]
        self.poke_exist = True  # poke found in db (std-True)
        self.id_db_poke = id_db_poke
        if db:
            self.db = db
            try:
                sqlite_connection = sqlite3.connect(resource_path(f'resources/system/database/{db}'))
                cursor = sqlite_connection.cursor()
                if query:
                    sqlite_select_query = query
                else:
                    sqlite_select_query = f'SELECT * FROM poke WHERE id_db like {self.id_db_poke}'
                cursor.execute(sqlite_select_query)
                records = cursor.fetchall()
                if len(records) == 0:
                    self.poke_exist = False
                for row in records:
                    self.id_pokedex = row[1]
                    self.name_poke = row[2]
                    self.type_poke = row[3]
                    self.ability_poke = row[4]
                    self.EVATK = row[5]
                    self.EVDEF = row[6]
                    self.EVSPD = row[7]
                    self.EVSPDEF = row[8]
                    self.EVSPATK = row[9]
                    self.EVHP = row[10]
                    self.IVATK = row[24]
                    self.IVDEF = row[25]
                    self.IVSPD = row[26]
                    self.IVSPATK = row[27]
                    self.IVSPDEF = row[28]
                    self.IVHP = row[29]
                    self.HP = row[11]
                    self.XP = row[12]
                    self.move_1 = row[13]
                    self.move_2 = row[14]
                    self.move_3 = row[15]
                    self.move_4 = row[16]
                    self.pp_1 = row[17]
                    self.pp_2 = row[18]
                    self.pp_3 = row[19]
                    self.pp_4 = row[20]
                    self.LV = row[21]
                    self.poke_gender = row[22]
                    self.poke_character = row[23]
                    self.status = row[30]

                    self.current_XP = int(self.XP + (self.LV * 10 * (self.LV - 1)) / 2)

                cursor.close()
                sqlite_connection.close()

            except sqlite3.Error as error:
                print("Ошибка при работе с SQLite", error)

        else:
            for row in args:
                self.id_pokedex = row[1]
                self.name_poke = row[2]
                self.type_poke = row[3]
                self.ability_poke = row[4]
                self.EVATK = row[5]
                self.EVDEF = row[6]
                self.EVSPD = row[7]
                self.EVSPDEF = row[8]
                self.EVSPATK = row[9]
                self.EVHP = row[10]
                self.IVATK = row[24]
                self.IVDEF = row[25]
                self.IVSPD = row[26]
                self.IVSPATK = row[27]
                self.IVSPDEF = row[28]
                self.IVHP = row[29]
                self.HP = row[11]
                self.XP = row[12]
                self.move_1 = row[13]
                self.move_2 = row[14]
                self.move_3 = row[15]
                self.move_4 = row[16]
                self.pp_1 = row[17]
                self.pp_2 = row[18]
                self.pp_3 = row[19]
                self.pp_4 = row[20]
                self.LV = row[21]
                self.poke_gender = row[22]
                self.poke_character = row[23]
                self.status = row[30]

                self.current_XP = int(self.XP + (self.LV * 10 * (self.LV - 1)) / 2)

        if self.poke_exist:
            self.source = resource_path(f"resources/pokemon/{self.type_poke}/{self.id_pokedex}/")
            self.icon_source = self.source + "icon.png"
            self.icon = pygame.image.load(resource_path(self.icon_source))
            self.STAT_ATK = self.stat_formula(pokemons[self.id_pokedex]["ATK"], self.IVATK, self.EVATK,
                                              self.LV, self.poke_character, "ATK")
            self.STAT_DEF = self.stat_formula(pokemons[self.id_pokedex]["DEF"], self.IVDEF, self.EVDEF,
                                              self.LV, self.poke_character, "DEF")
            self.STAT_SPD = self.stat_formula(pokemons[self.id_pokedex]["SPD"], self.IVSPD, self.EVSPD,
                                              self.LV, self.poke_character, "SPD")
            self.STAT_SPATK = self.stat_formula(pokemons[self.id_pokedex]["SPATK"], self.IVSPATK, self.EVSPATK,
                                                self.LV, self.poke_character, "SPATK")
            self.STAT_SPDEF = self.stat_formula(pokemons[self.id_pokedex]["SPDEF"], self.IVSPDEF, self.EVSPDEF,
                                                self.LV, self.poke_character, "SPDEF")
            self.STAT_HP = self.hp_formula(pokemons[self.id_pokedex]["HP"], self.IVHP, self.EVHP, self.LV)

    @staticmethod
    def hp_formula(base, iv, ev, level):
        hp = ((2 * base + int(iv) + (int(ev) / 4)) * level / 100) + level + 10
        return int(hp)

    @staticmethod
    def stat_formula(base, iv, ev, level, nature_poke, STAT):
        with open(resource_path('./resources/system/database/Natures.json')) as d:
            natures = json.load(d)
            nature_cof = 1
            for nature in natures:
                if nature["name"] == nature_poke:
                    for item, value in nature.items():
                        if item == STAT:
                            nature_cof = value
        stat = (((2 * base + int(iv) + (int(ev) / 4)) * level / 100) + 5) * nature_cof
        return int(stat)


class Poke_icon(sprite.Sprite):
    def __init__(self, x, y, poke=None):
        super(Poke_icon, self).__init__()
        self.type_system = "icon_poke"
        self.image_background = pygame.image.load(resource_path("resources/system/sprites/poke_icons.png"))
        self.info_shows = False  # status of showing info poke
        self.x = x  # x pos for icons (pokes)
        self.y = y  # y pos for icons (pokes)
        self.x_standart = self.x
        self.y_standart = self.y
        self.poke_exist = poke.poke_exist
        self.poke_info_show = False
        if poke.poke_exist:
            self.id_db_poke = poke.id_db_poke
            self.db = poke.db

            self.poke_name = font_standart.render(poke.name_poke, True, (255, 255, 255))
            self.icon_of_poke = poke.icon
            self.HP = poke.HP
            self.LV = font_standart.render(("Lv." + str(poke.LV)), True, (255, 255, 255))
            self.HP_line_percentage = 57 + (45 * (poke.HP / poke.STAT_HP))
            self.XP = poke.XP
            self.current_XP = poke.current_XP
            self.status = poke.status

        self.image = Surface((113, 47), pygame.SRCALPHA)
        self.rect = Rect(x, y, 113, 47)

        self.image.blit(self.image_background, (0, 0))  # bliting background image for icons
        if poke.poke_exist:
            self.image.blit(self.poke_name, (50, 8))
            self.image.blit(self.LV, (50, 17))
            self.image.blit(self.icon_of_poke, (11, 6))
            self.line_of_HP = pygame.draw.line(self.image, (0, 200, 64), [57, 32], [self.HP_line_percentage, 32])

    def update(self, screen, *args):
        screen.blit(self.image, (self.rect.x, self.rect.y))
        if self.info_shows:
            screen.blit(self.info_background, (self.rect.x + 125, self.rect.y))


class Poke_info(sprite.Sprite):
    def __init__(self, x, y, id_db_poke, db):
        super(Poke_info, self).__init__()
        self.type_system = "poke_info"
        self.info_background = pygame.image.load(resource_path("resources/system/sprites/poke_info_background.png"))
        self.x = x  # x pos for icons (pokes)
        self.y = y  # y pos for icons (pokes)
        self.id_db_poke = id_db_poke
        self.db = db

        try:
            sqlite_connection = sqlite3.connect(resource_path(f'resources/system/database/{db}'))
            cursor = sqlite_connection.cursor()
            sqlite_select_query = f'SELECT * FROM poke WHERE id_db like {id_db_poke}'
            cursor.execute(sqlite_select_query)
            records = cursor.fetchall()
            if len(records) == 0:
                self.poke_exist = False
            for row in records:
                self.id_pokedex = row[1]
                self.name_poke = row[2]
                self.type_poke = row[3]
                self.ability_poke = row[4]
                self.EVATK = row[5]
                self.EVDEF = row[6]
                self.EVSPD = row[7]
                self.EVSPDEF = row[8]
                self.EVSPATK = row[9]
                self.EVHP = row[10]
                self.IVATK = row[24]
                self.IVDEF = row[25]
                self.IVSPD = row[26]
                self.IVSPATK = row[27]
                self.IVSPDEF = row[28]
                self.IVHP = row[29]
                self.HP = row[11]
                self.XP = row[12]
                self.move_1 = row[13]
                self.move_2 = row[14]
                self.move_3 = row[15]
                self.move_4 = row[16]
                self.pp_1 = row[17]
                self.pp_2 = row[18]
                self.pp_3 = row[19]
                self.pp_4 = row[20]
                self.LV = row[21]
                self.poke_gender = row[22]
                self.poke_character = row[23]
                self.status = row[30]

                self.current_XP = int(self.XP + (self.LV * 10 * (self.LV - 1)) / 2)
                self.till_next = self.LV * 10 - self.XP

            cursor.close()
            sqlite_connection.close()

        except sqlite3.Error as error:
            print("Ошибка при работе с SQLite", error)

        self.image = Surface((460, 291), pygame.SRCALPHA)
        self.rect = Rect(x, y, 460, 291)
        self.close_button_x = [self.rect.x + 430, self.rect.x + 450]
        self.close_button_y = [self.rect.y + 20, self.rect.y + 40]

        self.STAT_ATK = self.stat_formula(pokemons[self.id_pokedex]["ATK"], self.IVATK, self.EVATK,
                                          self.LV, self.poke_character, "ATK")
        self.STAT_DEF = self.stat_formula(pokemons[self.id_pokedex]["DEF"], self.IVDEF, self.EVDEF,
                                          self.LV, self.poke_character, "DEF")
        self.STAT_SPD = self.stat_formula(pokemons[self.id_pokedex]["SPD"], self.IVSPD, self.EVSPD,
                                          self.LV, self.poke_character, "SPD")
        self.STAT_SPATK = self.stat_formula(pokemons[self.id_pokedex]["SPATK"], self.IVSPATK, self.EVSPATK,
                                            self.LV, self.poke_character, "SPATK")
        self.STAT_SPDEF = self.stat_formula(pokemons[self.id_pokedex]["SPDEF"], self.IVSPDEF, self.EVSPDEF,
                                            self.LV, self.poke_character, "SPDEF")
        self.STAT_HP = self.hp_formula(pokemons[self.id_pokedex]["HP"], self.IVHP, self.EVHP, self.LV)

        self.poke_img = self.image_getter(self.type_poke, self.id_pokedex)  # setting img of poke for poke_info
        self.poke_name = font_large.render(self.name_poke, True, (255, 255, 255))
        self.LV = font_standart.render(("Lv." + str(self.LV)), True, (255, 255, 255))
        self.type_font = font_standart.render(self.type_poke, True, (255, 255, 255))
        self.ID = font_standart.render(("ID:" + self.zero_adder_to_number(id_db_poke, 8, 0)), True, (255, 255, 255))
        self.ability_word = font_standart.render("Ability", True, (255, 255, 255))
        self.nature_word = font_standart.render("Nature", True, (255, 255, 255))
        self.OT_word = font_standart.render("OT", True, (255, 255, 255))
        self.Exp_word = font_standart.render("Exp", True, (255, 255, 255))
        self.Moves_word = font_standart.render("Moves", True, (255, 255, 255))
        self.Current_word = font_standart.render("Current:", True, (255, 255, 255))
        self.Till_next_word = font_standart.render("Till next:", True, (255, 255, 255))
        self.current_xp_value = font_standart.render(self.zero_adder_to_number(f"{self.current_XP} XP", 12, "space"),
                                                     True, (255, 255, 255))
        self.till_next_value = font_standart.render(self.zero_adder_to_number(f"{self.till_next} XP", 12, "space"),
                                                    True, (255, 255, 255))
        self.atk_word = font_standart.render("ATK", True, (255, 255, 255))
        self.def_word = font_standart.render("DEF", True, (255, 255, 255))
        self.spd_word = font_standart.render("SPD", True, (255, 255, 255))
        self.spatk_word = font_standart.render("SPATK", True, (255, 255, 255))
        self.spdef_word = font_standart.render("SPDEF", True, (255, 255, 255))
        self.hp_word = font_standart.render("HP", True, (255, 255, 255))
        self.IV_ATK_value = font_standart.render(str(self.IVATK), True, (255, 145, 0))
        self.IV_DEF_value = font_standart.render(str(self.IVDEF), True, (255, 145, 0))
        self.IV_SPD_value = font_standart.render(str(self.IVSPD), True, (255, 145, 0))
        self.IV_SPATK_value = font_standart.render(str(self.IVSPATK), True, (255, 145, 0))
        self.IV_SPDEF_value = font_standart.render(str(self.IVSPDEF), True, (255, 145, 0))
        self.IV_HP_value = font_standart.render(str(self.IVHP), True, (255, 145, 0))
        self.EV_ATK_value = font_standart.render(str(self.EVATK), True, (0, 213, 255))
        self.EV_DEF_value = font_standart.render(str(self.EVDEF), True, (0, 213, 255))
        self.EV_SPD_value = font_standart.render(str(self.EVSPD), True, (0, 213, 255))
        self.EV_SPATK_value = font_standart.render(str(self.EVSPATK), True, (0, 213, 255))
        self.EV_SPDEF_value = font_standart.render(str(self.EVSPDEF), True, (0, 213, 255))
        self.EV_HP_value = font_standart.render(str(self.EVHP), True, (0, 213, 255))
        self.STAT_ATK_value = font_standart.render(self.zero_adder_to_number(self.STAT_ATK, 3, "space"),
                                                   True, (255, 255, 255))
        self.STAT_DEF_value = font_standart.render(self.zero_adder_to_number(self.STAT_DEF, 3, "space"),
                                                   True, (255, 255, 255))
        self.STAT_SPD_value = font_standart.render(self.zero_adder_to_number(self.STAT_SPD, 3, "space"),
                                                   True, (255, 255, 255))
        self.STAT_SPATK_value = font_standart.render(self.zero_adder_to_number(self.STAT_SPATK, 3, "space"),
                                                     True, (255, 255, 255))
        self.STAT_SPDEF_value = font_standart.render(self.zero_adder_to_number(self.STAT_SPDEF, 3, "space"),
                                                     True, (255, 255, 255))
        self.STAT_HP_value = font_standart.render(self.zero_adder_to_number(self.STAT_HP, 3, "space"),
                                                  True, (255, 255, 255))

        self.HP_line_percentage = 30 + (148 * (self.HP / self.STAT_HP))
        if (self.HP / self.STAT_HP) >= 0.66:
            self.HP_field = font_standart.render(f"{self.zero_adder_to_number(self.HP, 3, 0)}/"
                                                 f"{self.zero_adder_to_number(self.STAT_HP, 3, 0)}",
                                                 True, (0, 200, 64))
        elif (self.HP / self.STAT_HP) <= 0.33:
            self.HP_field = font_standart.render(f"{self.zero_adder_to_number(self.HP, 3, 0)}/"
                                                 f"{self.zero_adder_to_number(self.STAT_HP, 3, 0)}",
                                                 True, (220, 50, 50))
        else:
            self.HP_field = font_standart.render(f"{self.zero_adder_to_number(self.HP, 3, 0)}/"
                                                 f"{self.zero_adder_to_number(self.STAT_HP, 3, 0)}",
                                                 True, (255, 255, 0))
        self.ability = font_standart.render(self.ability_poke, True, (255, 255, 255))
        self.poke_character_word = font_standart.render(self.poke_character, True, (255, 255, 255))
        self.OT = font_standart.render(pokedex[self.id_pokedex]["Name"], True, (255, 255, 255))

        self.image.blit(self.info_background, (0, 0))  # bliting background image for icons
        self.image.blit(self.poke_name, (50, 16))  # bliting poke name
        self.image.blit(self.LV, (180, 22))  # bliting lv of poke
        self.image.blit(self.type_font, (220, 22))  # bliting type of poke
        self.image.blit(self.ID, (270, 22))  # bliting id of poke (database)
        self.image.blit(self.poke_img, (325, 5))  # bliting poke image on poke_info
        self.image.blit(self.ability_word, (220, 78))  # bliting "Ability" word
        self.image.blit(self.nature_word, (220, 120))  # bliting "Nature" word
        self.image.blit(self.OT_word, (220, 163))  # bliting "OT" word
        self.image.blit(self.Exp_word, (35, 120))  # bliting "Exp" word

        if (self.HP / self.STAT_HP) >= 0.66:
            self.line_of_HP = pygame.draw.line(self.image, (0, 200, 64), [30, 88], [self.HP_line_percentage, 88], 2)
        elif (self.HP / self.STAT_HP) <= 0.33:
            self.line_of_HP = pygame.draw.line(self.image, (220, 50, 50), [30, 88], [self.HP_line_percentage, 88], 2)
        else:
            self.line_of_HP = pygame.draw.line(self.image, (255, 255, 64), [30, 88], [self.HP_line_percentage, 88], 2)

        self.move_1_buttons_status = False
        self.move_2_buttons_status = False
        self.move_3_buttons_status = False
        self.move_4_buttons_status = False
        self.move_button_up = pygame.Surface((24, 24), pygame.SRCALPHA)
        self.move_button_down = pygame.Surface((24, 24), pygame.SRCALPHA)
        self.move_button_up.blit(system_photo_resized, (0, 0), [430, 242, 12, 12])
        self.move_button_down.blit(system_photo_resized, (0, 0), [430, 218, 12, 12])

        try:
            # getting moves and pp of Pokémon
            sqlite_connection = sqlite3.connect(resource_path('resources/system/database/POKE_DB.db'))
            cursor = sqlite_connection.cursor()
            sqlite_select_query_moves = [f'SELECT identifier FROM moves WHERE id like {self.move_1}',
                                         f'SELECT identifier FROM moves WHERE id like {self.move_2}',
                                         f'SELECT identifier FROM moves WHERE id like {self.move_3}',
                                         f'SELECT identifier FROM moves WHERE id like {self.move_4}']
            sqlite_select_query_pp = [f'SELECT pp FROM moves WHERE id like {self.move_1}',
                                      f'SELECT pp FROM moves WHERE id like {self.move_2}',
                                      f'SELECT pp FROM moves WHERE id like {self.move_3}',
                                      f'SELECT pp FROM moves WHERE id like {self.move_4}']

            if self.move_1:
                # move_name process
                cursor.execute(sqlite_select_query_moves[0])
                move_name = cursor.fetchone()
                self.move_1_name = self.string_uppercase(move_name[0])  # correcting move name
                self.move_1_word = font_standart.render(self.move_1_name, True, (255, 255, 255))  # recover to font
                self.image.blit(self.move_1_word, (40, 204))  # bliting move name to poke_info

                # pp count process
                cursor.execute(sqlite_select_query_pp[0])
                pp_count = cursor.fetchone()
                self.pp_1_name = f"{str(self.pp_1)}/{str(pp_count[0])}"
                self.pp_1_word = font_standart.render(self.zero_adder_to_number(self.pp_1_name, 5, 'space'),
                                                      True, (255, 255, 255))
                self.image.blit(self.pp_1_word, (220, 204))  # bliting pp count to poke_info

                self.move_1_buttons_status = True  # status of button "true"

                # setting buttons pos ( for pressing mechanics )
                self.move_1_button_up_x = [self.rect.x + 266, self.rect.x + 278]
                self.move_1_button_up_y = [self.rect.y + 204, self.rect.y + 216]
                self.move_1_button_down_x = [self.rect.x + 280, self.rect.x + 292]
                self.move_1_button_down_y = [self.rect.y + 204, self.rect.y + 216]
                self.image.blit(self.move_button_up, (266, 204))  # bliting up button
                self.image.blit(self.move_button_down, (280, 204))  # bliting down button
            if self.move_2:
                # move_name process
                cursor.execute(sqlite_select_query_moves[1])
                move_name = cursor.fetchone()
                self.move_2_name = self.string_uppercase(move_name[0])
                self.move_2_word = font_standart.render(self.move_2_name, True, (255, 255, 255))
                self.image.blit(self.move_2_word, (40, 218))

                # pp count process
                cursor.execute(sqlite_select_query_pp[1])
                pp_count = cursor.fetchone()
                self.pp_2_name = f"{str(self.pp_2)}/{str(pp_count[0])}"
                self.pp_2_word = font_standart.render(self.zero_adder_to_number(self.pp_2_name, 5, 'space'),
                                                      True, (255, 255, 255))
                self.image.blit(self.pp_2_word, (220, 218))  # bliting pp count to poke_info

                self.move_2_buttons_status = True

                # setting buttons pos ( for pressing mechanics )
                self.move_2_button_up_x = [self.rect.x + 266, self.rect.x + 278]
                self.move_2_button_up_y = [self.rect.y + 218, self.rect.y + 230]
                self.move_2_button_down_x = [self.rect.x + 280, self.rect.x + 292]
                self.move_2_button_down_y = [self.rect.y + 218, self.rect.y + 230]
                self.image.blit(self.move_button_up, (266, 218))
                self.image.blit(self.move_button_down, (280, 218))
            if self.move_3:
                cursor.execute(sqlite_select_query_moves[2])
                move_name = cursor.fetchone()
                self.move_3_name = self.string_uppercase(move_name[0])
                self.move_3_word = font_standart.render(self.move_3_name, True, (255, 255, 255))
                self.image.blit(self.move_3_word, (40, 232))

                # pp count process
                cursor.execute(sqlite_select_query_pp[2])
                pp_count = cursor.fetchone()
                self.pp_3_name = f"{str(self.pp_3)}/{str(pp_count[0])}"
                self.pp_3_word = font_standart.render(self.zero_adder_to_number(self.pp_3_name, 5, 'space'),
                                                      True, (255, 255, 255))
                self.image.blit(self.pp_3_word, (220, 232))  # bliting pp count to poke_info

                self.move_3_buttons_status = True

                # setting buttons pos ( for pressing mechanics )
                self.move_3_button_up_x = [self.rect.x + 266, self.rect.x + 278]
                self.move_3_button_up_y = [self.rect.y + 232, self.rect.y + 244]
                self.move_3_button_down_x = [self.rect.x + 280, self.rect.x + 292]
                self.move_3_button_down_y = [self.rect.y + 232, self.rect.y + 244]
                self.image.blit(self.move_button_up, (266, 232))
                self.image.blit(self.move_button_down, (280, 232))
            if self.move_4:
                cursor.execute(sqlite_select_query_moves[3])
                move_name = cursor.fetchone()
                self.move_4_name = self.string_uppercase(move_name[0])
                self.move_4_word = font_standart.render(self.move_4_name, True, (255, 255, 255))
                self.image.blit(self.move_4_word, (40, 246))

                # pp count process
                cursor.execute(sqlite_select_query_pp[3])
                pp_count = cursor.fetchone()
                self.pp_4_name = f"{str(self.pp_4)}/{str(pp_count[0])}"
                self.pp_4_word = font_standart.render(self.zero_adder_to_number(self.pp_4_name, 5, 'space'),
                                                      True, (255, 255, 255))
                self.image.blit(self.pp_4_word, (220, 246))  # bliting pp count to poke_info

                self.move_4_buttons_status = True

                # setting buttons pos ( for pressing mechanics )
                self.move_4_button_up_x = [self.rect.x + 266, self.rect.x + 278]
                self.move_4_button_up_y = [self.rect.y + 246, self.rect.y + 258]
                self.move_4_button_down_x = [self.rect.x + 280, self.rect.x + 292]
                self.move_4_button_down_y = [self.rect.y + 246, self.rect.y + 258]
                self.image.blit(self.move_button_up, (266, 246))
                self.image.blit(self.move_button_down, (280, 246))

            cursor.close()
            sqlite_connection.close()
        except sqlite3.Error as error:
            print("Ошибка при работе с SQLite:", error)

        self.image.blit(self.Moves_word, (35, 182))  # bliting "Moves.py" word
        self.image.blit(self.Current_word, (35, 138))  # bliting "Current" word
        self.image.blit(self.current_xp_value, (100, 138))  # bliting current xp
        self.image.blit(self.Till_next_word, (35, 154))  # bliting "Till next" word
        self.image.blit(self.till_next_value, (100, 154))  # bliting till next XP
        self.image.blit(self.atk_word, (340, 167))  # bliting "Current" word
        self.image.blit(self.def_word, (340, 182))  # bliting "Current" word
        self.image.blit(self.spd_word, (340, 197))  # bliting "Current" word
        self.image.blit(self.spatk_word, (340, 212))  # bliting "Current" word
        self.image.blit(self.spdef_word, (340, 227))  # bliting "Current" word
        self.image.blit(self.hp_word, (340, 242))  # bliting "Current" word
        self.image.blit(self.IV_ATK_value, (404, 167))  # bliting iv value
        self.image.blit(self.IV_DEF_value, (404, 182))  # bliting iv value
        self.image.blit(self.IV_SPD_value, (404, 197))  # bliting iv value
        self.image.blit(self.IV_SPATK_value, (404, 212))  # bliting iv value
        self.image.blit(self.IV_SPDEF_value, (404, 227))  # bliting iv value
        self.image.blit(self.IV_HP_value, (404, 242))  # bliting iv value
        self.image.blit(self.EV_ATK_value, (420, 167))  # bliting iv value
        self.image.blit(self.EV_DEF_value, (420, 182))  # bliting ev value
        self.image.blit(self.EV_SPD_value, (420, 197))  # bliting ev value
        self.image.blit(self.EV_SPATK_value, (420, 212))  # bliting ev value
        self.image.blit(self.EV_SPDEF_value, (420, 227))  # bliting ev value
        self.image.blit(self.EV_HP_value, (420, 242))  # bliting ev value
        self.image.blit(self.STAT_ATK_value, (382, 167))  # bliting stat value
        self.image.blit(self.STAT_DEF_value, (382, 182))  # bliting stat value
        self.image.blit(self.STAT_SPD_value, (382, 197))  # bliting stat value
        self.image.blit(self.STAT_SPATK_value, (382, 212))  # bliting stat value
        self.image.blit(self.STAT_SPDEF_value, (382, 227))  # bliting stat value
        self.image.blit(self.STAT_HP_value, (382, 242))  # bliting stat value
        self.image.blit(self.HP_field, (137, 68))
        self.element_poke_getter(self.id_pokedex, self.image)  # bliting elements (type) of poke
        if self.type_poke == "shiny":
            self.image.blit(shiny_icon_s, (23, 22))
        self.image.blit(self.ability, (220, 98))  # bliting poke ability
        self.image.blit(self.poke_character_word, (220, 140))  # bliting poke character
        self.image.blit(self.OT, (220, 183))  # bliting "original poke name" word
        # self.line_of_HP = pygame.draw.line(self.image, (0, 200, 64), [57, 32], [self.HP_line_percentage, 32])

    def update(self, screen, *args):
        self.close_button_x = [self.rect.x + 430, self.rect.x + 450]
        self.close_button_y = [self.rect.y + 20, self.rect.y + 40]
        if self.move_1_buttons_status:
            self.move_1_button_up_x = [self.rect.x + 266, self.rect.x + 278]
            self.move_1_button_up_y = [self.rect.y + 204, self.rect.y + 216]
            self.move_1_button_down_x = [self.rect.x + 280, self.rect.x + 292]
            self.move_1_button_down_y = [self.rect.y + 204, self.rect.y + 216]
        if self.move_2_buttons_status:
            self.move_2_button_up_x = [self.rect.x + 266, self.rect.x + 278]
            self.move_2_button_up_y = [self.rect.y + 218, self.rect.y + 230]
            self.move_2_button_down_x = [self.rect.x + 280, self.rect.x + 292]
            self.move_2_button_down_y = [self.rect.y + 218, self.rect.y + 230]
        if self.move_3_buttons_status:
            self.move_3_button_up_x = [self.rect.x + 266, self.rect.x + 278]
            self.move_3_button_up_y = [self.rect.y + 232, self.rect.y + 244]
            self.move_3_button_down_x = [self.rect.x + 280, self.rect.x + 292]
            self.move_3_button_down_y = [self.rect.y + 232, self.rect.y + 244]
        if self.move_4_buttons_status:
            self.move_4_button_up_x = [self.rect.x + 266, self.rect.x + 278]
            self.move_4_button_up_y = [self.rect.y + 246, self.rect.y + 258]
            self.move_4_button_down_x = [self.rect.x + 280, self.rect.x + 292]
            self.move_4_button_down_y = [self.rect.y + 246, self.rect.y + 258]
        screen.blit(self.image, (self.rect.x, self.rect.y))

    #  def for getting pressed button
    def press_checker(self, e_pos_x, e_pos_y):
        # close button condition
        if self.close_button_x[0] <= e_pos_x <= self.close_button_x[1] and \
                self.close_button_y[0] <= e_pos_y <= self.close_button_y[1]:
            return "close_sprite"

        # move change buttons condition
        if self.move_1_buttons_status:
            if self.move_1_button_up_x[0] <= e_pos_x <= self.move_1_button_up_x[1] and \
                    self.move_1_button_up_y[0] <= e_pos_y <= self.move_1_button_up_y[1]:
                try:
                    # checking how many moves has Pokémon
                    if self.move_4_buttons_status:
                        sqlite_select_query_1_move = \
                            f'UPDATE poke SET move_4={self.move_1} WHERE id_db = {self.id_db_poke};'
                        sqlite_select_query_2_move = \
                            f'UPDATE poke SET move_1={self.move_4} WHERE id_db = {self.id_db_poke};'
                        sqlite_select_query_1_pp = \
                            f'UPDATE poke SET pp_4={self.pp_1} WHERE id_db = {self.id_db_poke};'
                        sqlite_select_query_2_pp = \
                            f'UPDATE poke SET pp_1={self.pp_4} WHERE id_db = {self.id_db_poke};'
                    else:
                        if self.move_3_buttons_status:
                            sqlite_select_query_1_move = \
                                f'UPDATE poke SET move_3={self.move_1} WHERE id_db = {self.id_db_poke}; '
                            sqlite_select_query_2_move = \
                                f'UPDATE poke SET move_1={self.move_3} WHERE id_db = {self.id_db_poke};'
                            sqlite_select_query_1_pp = \
                                f'UPDATE poke SET pp_3={self.pp_1} WHERE id_db = {self.id_db_poke}; '
                            sqlite_select_query_2_pp = \
                                f'UPDATE poke SET pp_1={self.pp_3} WHERE id_db = {self.id_db_poke};'
                        else:
                            if self.move_2_buttons_status:
                                sqlite_select_query_1_move = \
                                    f'UPDATE poke SET move_2={self.move_1} WHERE id_db = {self.id_db_poke};'
                                sqlite_select_query_2_move = \
                                    f'UPDATE poke SET move_1={self.move_2} WHERE id_db = {self.id_db_poke};'
                                sqlite_select_query_1_pp = \
                                    f'UPDATE poke SET pp_2={self.pp_1} WHERE id_db = {self.id_db_poke};'
                                sqlite_select_query_2_pp = \
                                    f'UPDATE poke SET pp_1={self.pp_2} WHERE id_db = {self.id_db_poke};'
                            else:
                                sqlite_select_query_1_move = \
                                    f'UPDATE poke SET move_1={self.move_1} WHERE id_db = {self.id_db_poke};'
                                sqlite_select_query_2_move = \
                                    f'UPDATE poke SET move_1={self.move_1} WHERE id_db = {self.id_db_poke};'
                                sqlite_select_query_1_pp = \
                                    f'UPDATE poke SET pp_1={self.pp_1} WHERE id_db = {self.id_db_poke};'
                                sqlite_select_query_2_pp = \
                                    f'UPDATE poke SET pp_1={self.pp_1} WHERE id_db = {self.id_db_poke};'

                    sqlite_connection_for_move = sqlite3.connect(
                        resource_path(f'resources/system/database/player_pokes.db'))
                    cursor = sqlite_connection_for_move.cursor()

                    cursor.execute(sqlite_select_query_1_move)
                    cursor.execute(sqlite_select_query_2_move)
                    cursor.execute(sqlite_select_query_1_pp)
                    cursor.execute(sqlite_select_query_2_pp)

                    sqlite_connection_for_move.commit()
                    cursor.close()
                    sqlite_connection_for_move.close()

                except sqlite3.Error as error:
                    print("Ошибка при работе с SQLite", error)

                return "update_sprite"

            if self.move_1_button_down_x[0] <= e_pos_x <= self.move_1_button_down_x[1] and \
                    self.move_1_button_down_y[0] <= e_pos_y <= self.move_1_button_down_y[1]:
                try:
                    if self.move_2_buttons_status:
                        sqlite_select_query_1_move = \
                            f'UPDATE poke SET move_2={self.move_1} WHERE id_db = {self.id_db_poke};'
                        sqlite_select_query_2_move = \
                            f'UPDATE poke SET move_1={self.move_2} WHERE id_db = {self.id_db_poke};'
                        sqlite_select_query_1_pp = \
                            f'UPDATE poke SET pp_2={self.pp_1} WHERE id_db = {self.id_db_poke};'
                        sqlite_select_query_2_pp = \
                            f'UPDATE poke SET pp_1={self.pp_2} WHERE id_db = {self.id_db_poke};'
                    else:
                        sqlite_select_query_1_move = \
                            f'UPDATE poke SET move_1={self.move_1} WHERE id_db = {self.id_db_poke};'
                        sqlite_select_query_2_move = \
                            f'UPDATE poke SET move_1={self.move_1} WHERE id_db = {self.id_db_poke};'
                        sqlite_select_query_1_pp = \
                            f'UPDATE poke SET pp_1={self.pp_1} WHERE id_db = {self.id_db_poke};'
                        sqlite_select_query_2_pp = \
                            f'UPDATE poke SET pp_1={self.pp_1} WHERE id_db = {self.id_db_poke};'

                    sqlite_connection_for_move = sqlite3.connect(
                        resource_path(f'resources/system/database/player_pokes.db'))
                    cursor = sqlite_connection_for_move.cursor()

                    cursor.execute(sqlite_select_query_1_move)
                    cursor.execute(sqlite_select_query_2_move)
                    cursor.execute(sqlite_select_query_1_pp)
                    cursor.execute(sqlite_select_query_2_pp)

                    sqlite_connection_for_move.commit()
                    cursor.close()
                    sqlite_connection_for_move.close()

                except sqlite3.Error as error:
                    print("Ошибка при работе с SQLite", error)
                return "update_sprite"
        if self.move_2_buttons_status:
            if self.move_2_button_up_x[0] <= e_pos_x <= self.move_2_button_up_x[1] and \
                    self.move_2_button_up_y[0] <= e_pos_y <= self.move_2_button_up_y[1]:
                sqlite_select_query_1_move = \
                    f'UPDATE poke SET move_1={self.move_2} WHERE id_db = {self.id_db_poke};'
                sqlite_select_query_2_move = \
                    f'UPDATE poke SET move_2={self.move_1} WHERE id_db = {self.id_db_poke};'
                sqlite_select_query_1_pp = \
                    f'UPDATE poke SET pp_1={self.pp_2} WHERE id_db = {self.id_db_poke};'
                sqlite_select_query_2_pp = \
                    f'UPDATE poke SET pp_2={self.pp_1} WHERE id_db = {self.id_db_poke};'

                try:
                    sqlite_connection_for_move = sqlite3.connect(
                        resource_path(f'resources/system/database/player_pokes.db'))
                    cursor = sqlite_connection_for_move.cursor()

                    cursor.execute(sqlite_select_query_1_move)
                    cursor.execute(sqlite_select_query_2_move)
                    cursor.execute(sqlite_select_query_1_pp)
                    cursor.execute(sqlite_select_query_2_pp)

                    sqlite_connection_for_move.commit()
                    cursor.close()
                    sqlite_connection_for_move.close()

                except sqlite3.Error as error:
                    print("Ошибка при работе с SQLite", error)
                return "update_sprite"
            if self.move_2_button_down_x[0] <= e_pos_x <= self.move_2_button_down_x[1] and \
                    self.move_2_button_down_y[0] <= e_pos_y <= self.move_2_button_down_y[1]:
                try:
                    if self.move_3_buttons_status:
                        sqlite_select_query_1_move = \
                            f'UPDATE poke SET move_3={self.move_2} WHERE id_db = {self.id_db_poke};'
                        sqlite_select_query_2_move = \
                            f'UPDATE poke SET move_2={self.move_3} WHERE id_db = {self.id_db_poke};'
                        sqlite_select_query_1_pp = \
                            f'UPDATE poke SET pp_3={self.pp_2} WHERE id_db = {self.id_db_poke};'
                        sqlite_select_query_2_pp = \
                            f'UPDATE poke SET pp_2={self.pp_3} WHERE id_db = {self.id_db_poke};'
                    else:
                        sqlite_select_query_1_move = \
                            f'UPDATE poke SET move_1={self.move_2} WHERE id_db = {self.id_db_poke};'
                        sqlite_select_query_2_move = \
                            f'UPDATE poke SET move_2={self.move_1} WHERE id_db = {self.id_db_poke};'
                        sqlite_select_query_1_pp = \
                            f'UPDATE poke SET pp_1={self.pp_2} WHERE id_db = {self.id_db_poke};'
                        sqlite_select_query_2_pp = \
                            f'UPDATE poke SET pp_2={self.pp_1} WHERE id_db = {self.id_db_poke};'

                    sqlite_connection_for_move = sqlite3.connect(
                        resource_path(f'resources/system/database/player_pokes.db'))
                    cursor = sqlite_connection_for_move.cursor()

                    cursor.execute(sqlite_select_query_1_move)
                    cursor.execute(sqlite_select_query_2_move)
                    cursor.execute(sqlite_select_query_1_pp)
                    cursor.execute(sqlite_select_query_2_pp)

                    sqlite_connection_for_move.commit()
                    cursor.close()
                    sqlite_connection_for_move.close()

                except sqlite3.Error as error:
                    print("Ошибка при работе с SQLite", error)
                return "update_sprite"
        if self.move_3_buttons_status:
            if self.move_3_button_up_x[0] <= e_pos_x <= self.move_3_button_up_x[1] and \
                    self.move_3_button_up_y[0] <= e_pos_y <= self.move_3_button_up_y[1]:
                sqlite_select_query_1_move = \
                    f'UPDATE poke SET move_2={self.move_3} WHERE id_db = {self.id_db_poke};'
                sqlite_select_query_2_move = \
                    f'UPDATE poke SET move_3={self.move_2} WHERE id_db = {self.id_db_poke};'
                sqlite_select_query_1_pp = \
                    f'UPDATE poke SET pp_2={self.pp_3} WHERE id_db = {self.id_db_poke};'
                sqlite_select_query_2_pp = \
                    f'UPDATE poke SET pp_3={self.pp_2} WHERE id_db = {self.id_db_poke};'

                try:
                    sqlite_connection_for_move = sqlite3.connect(
                        resource_path(f'resources/system/database/player_pokes.db'))
                    cursor = sqlite_connection_for_move.cursor()

                    cursor.execute(sqlite_select_query_1_move)
                    cursor.execute(sqlite_select_query_2_move)
                    cursor.execute(sqlite_select_query_1_pp)
                    cursor.execute(sqlite_select_query_2_pp)

                    sqlite_connection_for_move.commit()
                    cursor.close()
                    sqlite_connection_for_move.close()

                except sqlite3.Error as error:
                    print("Ошибка при работе с SQLite", error)
                return "update_sprite"
            if self.move_3_button_down_x[0] <= e_pos_x <= self.move_3_button_down_x[1] and \
                    self.move_3_button_down_y[0] <= e_pos_y <= self.move_3_button_down_y[1]:
                try:
                    if self.move_4_buttons_status:
                        sqlite_select_query_1_move = \
                            f'UPDATE poke SET move_4={self.move_3} WHERE id_db = {self.id_db_poke};'
                        sqlite_select_query_2_move = \
                            f'UPDATE poke SET move_3={self.move_4} WHERE id_db = {self.id_db_poke};'
                        sqlite_select_query_1_pp = \
                            f'UPDATE poke SET pp_4={self.pp_3} WHERE id_db = {self.id_db_poke};'
                        sqlite_select_query_2_pp = \
                            f'UPDATE poke SET pp_3={self.pp_4} WHERE id_db = {self.id_db_poke};'
                    else:
                        sqlite_select_query_1_move = \
                            f'UPDATE poke SET move_1={self.move_3} WHERE id_db = {self.id_db_poke};'
                        sqlite_select_query_2_move = \
                            f'UPDATE poke SET move_3={self.move_1} WHERE id_db = {self.id_db_poke};'
                        sqlite_select_query_1_pp = \
                            f'UPDATE poke SET pp_1={self.pp_3} WHERE id_db = {self.id_db_poke};'
                        sqlite_select_query_2_pp = \
                            f'UPDATE poke SET pp_3={self.pp_1} WHERE id_db = {self.id_db_poke};'

                    sqlite_connection_for_move = sqlite3.connect(
                        resource_path(f'resources/system/database/player_pokes.db'))
                    cursor = sqlite_connection_for_move.cursor()

                    cursor.execute(sqlite_select_query_1_move)
                    cursor.execute(sqlite_select_query_2_move)
                    cursor.execute(sqlite_select_query_1_pp)
                    cursor.execute(sqlite_select_query_2_pp)

                    sqlite_connection_for_move.commit()
                    cursor.close()
                    sqlite_connection_for_move.close()

                except sqlite3.Error as error:
                    print("Ошибка при работе с SQLite", error)
                return "update_sprite"
        if self.move_4_buttons_status:
            if self.move_4_button_up_x[0] <= e_pos_x <= self.move_4_button_up_x[1] and \
                    self.move_4_button_up_y[0] <= e_pos_y <= self.move_4_button_up_y[1]:
                sqlite_select_query_1_move = \
                    f'UPDATE poke SET move_3={self.move_4} WHERE id_db = {self.id_db_poke};'
                sqlite_select_query_2_move = \
                    f'UPDATE poke SET move_4={self.move_3} WHERE id_db = {self.id_db_poke};'
                sqlite_select_query_1_pp = \
                    f'UPDATE poke SET pp_3={self.pp_4} WHERE id_db = {self.id_db_poke};'
                sqlite_select_query_2_pp = \
                    f'UPDATE poke SET pp_4={self.pp_3} WHERE id_db = {self.id_db_poke};'

                try:
                    sqlite_connection_for_move = sqlite3.connect(
                        resource_path(f'resources/system/database/player_pokes.db'))
                    cursor = sqlite_connection_for_move.cursor()

                    cursor.execute(sqlite_select_query_1_move)
                    cursor.execute(sqlite_select_query_2_move)
                    cursor.execute(sqlite_select_query_1_pp)
                    cursor.execute(sqlite_select_query_2_pp)

                    sqlite_connection_for_move.commit()
                    cursor.close()
                    sqlite_connection_for_move.close()

                except sqlite3.Error as error:
                    print("Ошибка при работе с SQLite", error)
                return "update_sprite"
            if self.move_4_button_down_x[0] <= e_pos_x <= self.move_4_button_down_x[1] and \
                    self.move_4_button_down_y[0] <= e_pos_y <= self.move_4_button_down_y[1]:
                sqlite_select_query_1_move = \
                    f'UPDATE poke SET move_1={self.move_4} WHERE id_db = {self.id_db_poke};'
                sqlite_select_query_2_move = \
                    f'UPDATE poke SET move_4={self.move_1} WHERE id_db = {self.id_db_poke};'
                sqlite_select_query_1_pp = \
                    f'UPDATE poke SET pp_1={self.pp_4} WHERE id_db = {self.id_db_poke};'
                sqlite_select_query_2_pp = \
                    f'UPDATE poke SET pp_4={self.pp_1} WHERE id_db = {self.id_db_poke};'

                try:
                    sqlite_connection_for_move = sqlite3.connect(
                        resource_path(f'resources/system/database/player_pokes.db'))
                    cursor = sqlite_connection_for_move.cursor()

                    cursor.execute(sqlite_select_query_1_move)
                    cursor.execute(sqlite_select_query_2_move)
                    cursor.execute(sqlite_select_query_1_pp)
                    cursor.execute(sqlite_select_query_2_pp)

                    sqlite_connection_for_move.commit()
                    cursor.close()
                    sqlite_connection_for_move.close()

                except sqlite3.Error as error:
                    print("Ошибка при работе с SQLite", error)
                return "update_sprite"

    @staticmethod
    def hp_formula(base, iv, ev, level):
        hp = ((2 * base + int(iv) + (int(ev) / 4)) * level / 100) + level + 10
        return int(hp)

    @staticmethod
    def stat_formula(base, iv, ev, level, nature_poke, STAT):
        with open(resource_path('./resources/system/database/Natures.json')) as d:
            natures = json.load(d)
            nature_cof = 1
            for nature in natures:
                if nature["name"] == nature_poke:
                    for item, value in nature.items():
                        if item == STAT:
                            nature_cof = value
        stat = (((2 * base + int(iv) + (int(ev) / 4)) * level / 100) + 5) * nature_cof
        return int(stat)

    @staticmethod
    def image_getter(type_poke, id_pokedex):
        source_poke_img = resource_path(f"resources/pokemon/{type_poke}/{id_pokedex}/foe.png")
        poke_img = pygame.image.load(source_poke_img)
        return poke_img

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
    def element_poke_getter(id_pokedex, self_image):
        def element_drawer(element):
            if element == "Flying":
                return flying_type
            elif element == "Fairy":
                return fairy_type
            elif element == "Steel":
                return steel_type
            elif element == "Poison":
                return poison_type
            elif element == "Ghost":
                return ghost_type
            elif element == "Electric":
                return electric_type
            elif element == "Ice":
                return ice_type
            elif element == "Psychic":
                return psychic_type
            elif element == "Dragon":
                return dragon_type
            elif element == "Grass":
                return grass_type
            elif element == "Rock":
                return rock_type
            elif element == "Normal":
                return normal_type
            elif element == "Water":
                return water_type
            elif element == "Dark":
                return dark_type
            elif element == "Bug":
                return bug_type
            elif element == "Fight":
                return fight_type
            elif element == "Fire":
                return fire_type
            elif element == "Ground":
                return ground_type

        if pokedex[id_pokedex]["Types"][1] == "":
            self_image.blit(element_drawer(pokedex[id_pokedex]["Types"][0]), (370, 147))
        else:
            self_image.blit(element_drawer(pokedex[id_pokedex]["Types"][0]), (355, 147))
            self_image.blit(element_drawer(pokedex[id_pokedex]["Types"][1]), (390, 147))

    @staticmethod
    def string_uppercase(string):
        str_list = string.split("-")
        new_list = []
        for i in str_list:
            new_word = i.title()
            new_list.append(new_word)
        return " ".join(new_list)


class Player_poke:
    def __init__(self):
        self.poke_1 = Pokemon(1, "player_pokes.db")
        self.poke_2 = Pokemon(2, "player_pokes.db")
        self.poke_3 = Pokemon(3, "player_pokes.db")
        self.poke_4 = Pokemon(4, "player_pokes.db")
        self.poke_5 = Pokemon(5, "player_pokes.db")
        self.poke_6 = Pokemon(6, "player_pokes.db")

        # setting standart icons (without poke)
        self.poke_icons_b = pygame.sprite.Group()
        self.poke_1_icon_b = Poke_icon(30, 10, self.poke_1)
        self.poke_2_icon_b = Poke_icon(30, 55, self.poke_2)
        self.poke_3_icon_b = Poke_icon(30, 100, self.poke_3)
        self.poke_4_icon_b = Poke_icon(30, 145, self.poke_4)
        self.poke_5_icon_b = Poke_icon(30, 190, self.poke_5)
        self.poke_6_icon_b = Poke_icon(30, 235, self.poke_6)

        self.poke_icons_b.add(self.poke_1_icon_b, self.poke_2_icon_b, self.poke_3_icon_b,
                              self.poke_4_icon_b, self.poke_5_icon_b, self.poke_6_icon_b)

    # func, when player is changing his active poke list
    def changer_poke_icon(self, poke_a, poke_b, system_mech_group):
        if poke_a.poke_exist and poke_b.poke_exist:
            # changing SQL data about player pokes
            sqlite_select_query_1 = f'UPDATE poke SET id_db=9999999 WHERE id_db = {poke_a.id_db_poke};'
            sqlite_select_query_2 = f'UPDATE poke SET id_db={poke_a.id_db_poke} WHERE id_db = {poke_b.id_db_poke};'
            sqlite_select_query_3 = f'UPDATE poke SET id_db={poke_b.id_db_poke} WHERE id_db = 9999999'

            try:
                sqlite_connection = sqlite3.connect(resource_path(f'resources/system/database/{poke_a.db}'))
                cursor = sqlite_connection.cursor()

                cursor.execute(sqlite_select_query_1)
                cursor.execute(sqlite_select_query_2)
                cursor.execute(sqlite_select_query_3)

                sqlite_connection.commit()
                cursor.close()
                sqlite_connection.close()

            except sqlite3.Error as error:
                print("Ошибка при работе с SQLite", error)

            def updater_self_structure(poke_n, System_mech_group):
                if poke_n == self.poke_1_icon_b:  # checking position of player's pokes
                    self.poke_1_icon_b.kill()  # killing current Poke_icon
                    del self.poke_1  # delete player Pokemon
                    self.poke_1 = Pokemon(poke_n.id_db_poke, "player_pokes.db")
                    self.poke_1_icon_b = Poke_icon(30, 10, self.poke_1)
                    self.poke_icons_b.add(self.poke_1_icon_b)  # adding again sprite in group
                    System_mech_group.add(self.poke_1_icon_b)  # adding again sprite in system_mech
                elif poke_n == self.poke_2_icon_b:  # checking position of player's pokes
                    self.poke_2_icon_b.kill()  # killing current Poke_icon
                    del self.poke_2  # delete player Pokemon
                    self.poke_2 = Pokemon(poke_n.id_db_poke, "player_pokes.db")
                    self.poke_2_icon_b = Poke_icon(30, 55, self.poke_2)
                    self.poke_icons_b.add(self.poke_2_icon_b)  # adding again sprite in group
                    System_mech_group.add(self.poke_2_icon_b)  # adding again sprite in system_mech
                elif poke_n == self.poke_3_icon_b:  # checking position of player's pokes
                    self.poke_3_icon_b.kill()  # killing current Poke_icon
                    del self.poke_3  # delete player Pokemon
                    self.poke_3 = Pokemon(poke_n.id_db_poke, "player_pokes.db")
                    self.poke_3_icon_b = Poke_icon(30, 100, self.poke_3)
                    self.poke_icons_b.add(self.poke_3_icon_b)  # adding again sprite in group
                    System_mech_group.add(self.poke_3_icon_b)  # adding again sprite in system_mech
                elif poke_n == self.poke_4_icon_b:  # checking position of player's pokes
                    self.poke_4_icon_b.kill()  # killing current Poke_icon
                    del self.poke_4  # delete player Pokemon
                    self.poke_4 = Pokemon(poke_n.id_db_poke, "player_pokes.db")
                    self.poke_4_icon_b = Poke_icon(30, 145, self.poke_4)
                    self.poke_icons_b.add(self.poke_4_icon_b)  # adding again sprite in group
                    System_mech_group.add(self.poke_4_icon_b)  # adding again sprite in system_mech
                elif poke_n == self.poke_5_icon_b:  # checking position of player's pokes
                    self.poke_5_icon_b.kill()  # killing current Poke_icon
                    del self.poke_5  # delete player Pokemon
                    self.poke_5 = Pokemon(poke_n.id_db_poke, "player_pokes.db")
                    self.poke_5_icon_b = Poke_icon(30, 190, self.poke_5)
                    self.poke_icons_b.add(self.poke_5_icon_b)  # adding again sprite in group
                    System_mech_group.add(self.poke_5_icon_b)  # adding again sprite in system_mech
                elif poke_n == self.poke_6_icon_b:  # checking position of player's pokes
                    self.poke_6_icon_b.kill()  # killing current Poke_icon
                    del self.poke_6  # delete player Pokemon
                    self.poke_6 = Pokemon(poke_n.id_db_poke, "player_pokes.db")
                    self.poke_6_icon_b = Poke_icon(30, 235, self.poke_6)
                    self.poke_icons_b.add(self.poke_6_icon_b)  # adding again sprite in group
                    System_mech_group.add(self.poke_6_icon_b)  # adding again sprite in system_mech

            # update old Poke_icon sprites
            updater_self_structure(poke_a, system_mech_group)
            updater_self_structure(poke_b, system_mech_group)


class Setting:
    def __init__(self, player_x=None, player_y=None, current_location=None):
        self.WIDTH = 1248
        self.HEIGHT = 736
        self.FPS = 30
        self.block_size = 32
        self.world_status = "MAIN"

        # color constants
        self.WHITE = (255, 255, 255)
        self.BLACK = (0, 0, 0)

        if player_x is None:
            self.player_x = 19 * 32
            self.player_y = 12 * 32
        else:
            self.player_x = player_x
            self.player_y = player_y

        if current_location is None:
            self.current_location = "TestHouse"
        else:
            self.current_location = current_location

        self.last_move = "down"
        self.world_status = "MAIN"

        # creating player pokes
        self.player_pokes = Player_poke()
        self.poke_info = False  # we can see only 1 poke info on time, and set True when its showing
        self.poke_info_sprite = None  # poke info sprite
        self.poke_info_sprite_x = None  # poke info sprite x pos
        self.poke_info_sprite_y = None  # poke info sprite y pos
        system_mech.add(self.player_pokes.poke_icons_b)

    def world_status_changer(self, status):
        self.world_status = status

    def last_move_setter(self, last_move):
        self.last_move = last_move
