import sys
import os
import pygame.image
from pygame import *
from moviepy.editor import *
from moviepy.video.fx.resize import resize
import pyganim
from dialog import Dialog_box
from npc import NPC, Dialogue, sans_sound


def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


# stars animation (teleporter)
stars_01_original = pygame.image.load(resource_path("resources/img/animations/stars/stars_0.png"))
stars_02_original = pygame.image.load(resource_path("resources/img/animations/stars/stars_1.png"))
stars_03_original = pygame.image.load(resource_path("resources/img/animations/stars/stars_2.png"))
stars_04_original = pygame.image.load(resource_path("resources/img/animations/stars/stars_3.png"))
stars_01 = pygame.transform.scale(stars_01_original, (30, 30))
stars_02 = pygame.transform.scale(stars_02_original, (30, 30))
stars_03 = pygame.transform.scale(stars_03_original, (30, 30))
stars_04 = pygame.transform.scale(stars_04_original, (30, 30))
stars_01_big = pygame.transform.scale(stars_01_original, (64, 64))
stars_02_big = pygame.transform.scale(stars_02_original, (64, 64))
stars_03_big = pygame.transform.scale(stars_03_original, (64, 64))
stars_04_big = pygame.transform.scale(stars_04_original, (64, 64))

stars_animation = pyganim.PygAnimation([
    (stars_01, 0.2),
    (stars_02, 0.2),
    (stars_03, 0.2),
    (stars_04, 0.2)])

stars_animation_big = pyganim.PygAnimation([
    (stars_01_big, 0.2),
    (stars_02_big, 0.2),
    (stars_03_big, 0.2),
    (stars_04_big, 0.2)])

# "loading" video animation
loading_video_original = VideoFileClip(resource_path("resources/img/animations/loading/loading_yun_video_small.mp4"))
loading_video = loading_video_original.resize((1248, 736))


def place_loading(items, place):  # loading items for any map
    items.empty()
    if place == "TestHouse":
        # drawing items
        items.add(Stars(19, 16, "from_TestHouse_to_TestMap", 39 * 32, 15 * 32, 'down'))
        items.add(Stars(23, 8, "from_TestHouse_to_TestHouse2", 20 * 32, 10 * 32, 'left'))
        text = ["· hi|· my name is Johns!|· I love poke very much! Do you know, that|"
                "· Which type of poke you prefer?| | ",
                " | |  fire poke can win ice type!| | | ",
                " | | -ps: i've hear this from Pr.Oak| | | ",
                " | | -pss: but i know this myself too| | | "]
        q1 = {
            "index": 3,
            "answer_count": 3,
            "answer": ["- i love fire poke", "- i love ice poke", "- i love grass type poke"],
            "text_after": ["· oh, yeah, fire type pokes are strong/ against to ice and grass",
                           "· i will battle you soon!"],
            "text_after_2": ["· i love ice poke too!"],
            "text_after_3": ["· hmm, grass type is strong type,/ i agree with you"]
        }
        boy = NPC("sprite2", 24 * 32, 13 * 32, "d", 10, text, q1)
        boy.movement(32, 1, 1, 'd', 'l', 'r', 'u', 80, 60, 60, 60)
        items.add(boy)
        text_fridge = ["There are a lot of interesting things inside.",
                       "But the cake in the middle attracts the most.",
                       "It looks very tasty.",
                       " "]
        fridge = Dialog_box(17 * 32, 8 * 32, text_fridge)
        fridge2 = Dialog_box(16 * 32, 8 * 32, text_fridge)
        items.add(fridge)
        items.add(fridge2)
        tv_text = ["\"TOP-5 Epic Pokemon Battle\" show is on TV", " ", " ", " "]
        tv = Dialog_box(19 * 32, 11 * 32, tv_text)
        items.add(tv)
    elif place == "TestMap":
        items.add(Stars(39, 14, "from_TestMap_to_TestHouse", 19 * 32, 15 * 32, 'up'))
    elif place == "TestHouse2":
        items.add(Stars(21, 10, "from_TestHouse2_to_TestHouse", 24 * 32, 8 * 32, 'right'))


class Stars(sprite.Sprite):
    def __init__(self, x, y, place_to_go, coordinate_for_map_x, coordinate_for_map_y, player_standing_animation):
        super(Stars, self).__init__()
        self.type = "teleporter"
        self.action = False  # npc can't action with this
        self.place_to_go = place_to_go
        self.player_standing_animation = player_standing_animation
        self.coordinate_for_map_x = coordinate_for_map_x
        self.coordinate_for_map_y = coordinate_for_map_y
        self.x = x * 32
        self.y = y * 32
        self.image = Surface([32, 32], pygame.SRCALPHA)
        self.rect = Rect(self.x, self.y, 32, 32)

    def update(self, player, screen, *args):  # !!! TEST ANIMATION ITEM !!! use for animation items
        self.image.fill((255, 255, 255, 0))
        stars_animation.play()
        stars_animation.blit(self.image, (0, 0))
        screen.blit(self.image, (self.x, self.y))

    def draw(self, screen):
        stars_animation.play()
        stars_animation.blit(self.image, (0, 0))
        screen.blit(self.image, (self.x, self.y))

    def teleport(self, world):  # teleport function
        world.map_changer(self.place_to_go, self.player_standing_animation,
                          player_x_pos=self.coordinate_for_map_x, player_y_pos=self.coordinate_for_map_y)
