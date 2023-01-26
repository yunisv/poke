import sys
import os
import pygame.sprite
import json
from pygame import *


# noinspection PyBroadException
def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


img_1_33917 = pygame.image.load(resource_path('resources/img/places/1 #33917.png'))
img_2_32112 = pygame.image.load(resource_path('resources/img/places/2 #32112.png'))
img_3_37472 = pygame.image.load(resource_path('resources/img/places/3 #37472.png'))
img_6_43893 = pygame.image.load(resource_path('resources/img/places/6 #43893.png'))
img_7_29287 = pygame.image.load(resource_path('resources/img/places/7 #29287.png'))
img_8_36737 = pygame.image.load(resource_path('resources/img/places/8 #36737.png'))
img_10_24308 = pygame.image.load(resource_path('resources/img/places/10 #24308.png'))
img_11_36108 = pygame.image.load(resource_path('resources/img/places/11 #36108.png'))
img_12_23703 = pygame.image.load(resource_path('resources/img/places/12 #23703.png'))
img_14_28669 = pygame.image.load(resource_path("resources/img/places/14 #28669.png"))
img_25_38630 = pygame.image.load(resource_path("resources/img/places/25 #38630.png"))
img_31_34045 = pygame.image.load(resource_path("resources/img/places/31 #34045.png"))
img_38_31813 = pygame.image.load(resource_path("resources/img/places/38 #31813.png"))
img_40 = pygame.image.load(resource_path("resources/img/places/40.png"))
img_47_41514 = pygame.image.load(resource_path("resources/img/places/47 #41514.png"))


class Tile(pygame.sprite.Sprite):
    def __init__(self, x, y, id_of_item, tilesets, layer_rect):
        super(Tile, self).__init__()
        self.x = x
        self.y = y
        self.rect_y_on_image = None  # need y-pos for cutting image from spritesheet
        self.rect_x_on_image = None  # need x-pos for cutting image from spritesheet

        self.first_id = None  # first id from layer's list
        self.real_id = None  # item's id from spritesheet
        self.source = None  # source (path to) spritesheet
        self.layer_rect = layer_rect  # getting role of item  !!! NEED DO !!!(ДЛЯ ЭФФЕКТА ПРОХОЖДЕНИЯ)
        self.id_item = id_of_item  # getting current id of item from layer
        self.weight = 32  # getting W for image (parse)
        self.height = 32  # getting H for image (parse)
        self.image = pygame.Surface((self.weight, self.height),
                                    pygame.SRCALPHA)  # create surface for image
        self.set_rect()  # setting rect of image

        for tileset in tilesets:  # here cycle for getting first_id and source
            if self.id_item > tileset["firstgid"]:
                self.first_id = tileset["firstgid"]
                self.source = tileset["source"]
            elif self.id_item == 0:
                self.id_item = 0
                self.first_id = 0

        self.real_id = self.id_item - self.first_id  # setting real_id
        self.set_x_and_y_on_spritesheet()  # setting image's position from spritesheet

        self.sprite_from_spritesheet = pygame.Surface((self.weight, self.height), pygame.HWSURFACE)  # create surface
        self.sprite_from_spritesheet.set_colorkey((0, 0, 0))
        self.sprite_from_spritesheet = self.sprite_from_spritesheet.convert_alpha()
        self.set_sprite_image()  # getting image from spritesheet and bliting on sprite_from_spritesheet

    def set_x_and_y_on_spritesheet(self):  # function for getting image's position from spritesheet
        b = (self.id_item - self.first_id) // 32
        a = (self.id_item - self.first_id) % 32
        self.rect_x_on_image = a * 32
        self.rect_y_on_image = b * 32

    def set_sprite_image(self):  # function which return ready sprite of item from spritesheet
        if self.source == "1 #33917.tsx":
            self.sprite_from_spritesheet.blit(img_1_33917, (0, 0), (self.rect_x_on_image, self.rect_y_on_image,
                                                                    self.weight, self.height))
        elif self.source == "2 #32112.tsx":
            self.sprite_from_spritesheet.blit(img_2_32112, (0, 0), (self.rect_x_on_image, self.rect_y_on_image,
                                                                    self.weight, self.height))
        elif self.source == "3 #37472.tsx":
            self.sprite_from_spritesheet.blit(img_3_37472, (0, 0), (self.rect_x_on_image, self.rect_y_on_image,
                                                                    self.weight, self.height))
        elif self.source == "6 #43893.tsx":
            self.sprite_from_spritesheet.blit(img_6_43893, (0, 0), (self.rect_x_on_image, self.rect_y_on_image,
                                                                    self.weight, self.height))
        elif self.source == "7 #29287.tsx":
            self.sprite_from_spritesheet.blit(img_7_29287, (0, 0), (self.rect_x_on_image, self.rect_y_on_image,
                                                                    self.weight, self.height))
        elif self.source == "8 #36737.tsx":
            self.sprite_from_spritesheet.blit(img_8_36737, (0, 0), (self.rect_x_on_image, self.rect_y_on_image,
                                                                    self.weight, self.height))
        elif self.source == "10 #24308.tsx":
            self.sprite_from_spritesheet.blit(img_10_24308, (0, 0), (self.rect_x_on_image, self.rect_y_on_image,
                                                                     self.weight, self.height))
        elif self.source == "11 #36108.tsx":
            self.sprite_from_spritesheet.blit(img_11_36108, (0, 0), (self.rect_x_on_image, self.rect_y_on_image,
                                                                     self.weight, self.height))
        elif self.source == "12 #23703.tsx":
            self.sprite_from_spritesheet.blit(img_12_23703, (0, 0), (self.rect_x_on_image, self.rect_y_on_image,
                                                                     self.weight, self.height))
        elif self.source == "14 #28669.tsx":
            self.sprite_from_spritesheet.blit(img_14_28669, (0, 0), (self.rect_x_on_image, self.rect_y_on_image,
                                                                     self.weight, self.height))
        elif self.source == "25 #38630.tsx":
            self.sprite_from_spritesheet.blit(img_25_38630, (0, 0), (self.rect_x_on_image, self.rect_y_on_image,
                                                                     self.weight, self.height))
        elif self.source == "31 #34045.tsx":
            self.sprite_from_spritesheet.blit(img_31_34045, (0, 0), (self.rect_x_on_image, self.rect_y_on_image,
                                                                     self.weight, self.height))
        elif self.source == "38 #31813.tsx":
            self.sprite_from_spritesheet.blit(img_38_31813, (0, 0), (self.rect_x_on_image, self.rect_y_on_image,
                                                                     self.weight, self.height))
        elif self.source == "40.tsx":
            self.sprite_from_spritesheet.blit(img_40, (0, 0), (self.rect_x_on_image, self.rect_y_on_image,
                                                               self.weight, self.height))
        elif self.source == "47 #41514.tsx":
            self.sprite_from_spritesheet.blit(img_47_41514, (0, 0), (self.rect_x_on_image, self.rect_y_on_image,
                                                                     self.weight, self.height))

    def set_rect(self):
        layer = self.layer_rect.split("/")
        layer = layer[0]
        if layer == "background":
            self.rect = Rect(self.x, self.y, 0, 0)
        elif layer == "background_items":
            self.rect = Rect(self.x, self.y, 0, 0)
        elif layer == "background_rect":
            self.rect = Rect(self.x, self.y, 32, 32)
        elif layer == "item_with_rect":
            self.rect = Rect(self.x, self.y, 32, 32)
        elif layer == "external_item":
            self.rect = Rect(self.x, self.y, 0, 0)

    def set_position_in_map(self):
        pass

    def draw(self, screen):  # draw to map
        self.image.fill((0, 0, 0, 0))
        self.image.blit(self.sprite_from_spritesheet, (0, 0))
        screen.blit(self.image, (self.rect.x, self.rect.y))


class TileMap:
    def __init__(self, json_file):
        self.width = None  # set W
        self.height = None  # set H
        self.background_internal_items = pygame.sprite.Group()  # create group background_internal items
        self.background_external_items = pygame.sprite.Group()  # create group background_external items
        self.background_internal_items_with_rect = pygame.sprite.Group()  # create group background_internal items(rect)
        with open(resource_path(json_file), 'r') as f:  # open file (json) of map
            self.file = json.load(f)  # setting all info to file (variable)
        self.tilesets = self.file["tilesets"]  # setting tilesets
        self.layers = self.file["layers"]  # setting layers
        self.layer_setter(self.layers)  # getting layers

        # setting cords of map (for player movement)
        try:
            self.top_cord = self.file["top_cord"] * 32
            self.bottom_cord = self.file["bottom_cord"] * 32
            self.left_cord = self.file["left_cord"] * 32
            self.right_cord = self.file["right_cord"] * 32
        except KeyError:
            print("ОШИБКА:Ты не указал координаты (top_cord and etc) в json-файле карты!")
            sys.exit()

        # create background_internal surface
        self.background_internal = None
        # create background_external surface
        self.background_external = None
        self.backgrounds_setter()  # setting background's surface
        self.map_draw()  # drawing items to map

    def layer_setter(self, layers):
        for layer in layers:
            if layer["name"] == "background":
                self.width = layer["width"]
                self.height = layer["height"]
            item_index = 0
            width = layer["width"]
            height = layer["height"]
            name = layer["name"]
            list_of_data = layer["data"]
            for y in range(0, height):
                for x in range(0, width):
                    current_item = list_of_data[item_index]
                    tile = Tile(x * 32, y * 32, current_item, self.tilesets, name)  # creating simple tile
                    type_of_item = name.split("/")
                    if type_of_item[0] == "background_rect" or type_of_item[0] == "item_with_rect":
                        if current_item != 0:
                            self.background_internal_items_with_rect.add(tile)
                    elif type_of_item[0] == "external_item":
                        if current_item != 0:
                            self.background_external_items.add(tile)
                    else:
                        self.background_internal_items.add(tile)
                    item_index += 1

    def backgrounds_setter(self):
        # create background_internal surface
        self.background_internal = pygame.Surface((self.width * 32, self.height * 32), pygame.HWSURFACE)
        self.background_internal.set_colorkey((0, 0, 0))
        self.background_internal = self.background_internal.convert_alpha()
        # create background_external surface
        self.background_external = pygame.Surface((self.width * 32, self.height * 32), pygame.HWSURFACE)
        self.background_external.set_colorkey((0, 0, 0))
        self.background_external = self.background_external.convert_alpha()

    def map_draw(self):
        for y in self.background_internal_items:
            y.draw(self.background_internal)
        for y in self.background_internal_items_with_rect:
            y.draw(self.background_internal)
        for y in self.background_external_items:
            y.draw(self.background_external)
