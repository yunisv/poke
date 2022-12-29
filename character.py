import sys
import os
from pygame import *
import pygame
import pyganim
from pokemons import pokemons
from places import stars_animation, stars_animation_big
from setting import *


def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


character_spritesheet = pygame.image.load(resource_path("resources/img/main_character/character_spritesheet.png"))

main_character_up_0 = pygame.Surface([32, 48], pygame.SRCALPHA)
main_character_up_0.blit(character_spritesheet, (0, 0), [80, 16, 32, 48])
main_character_up_1 = pygame.Surface([32, 48], pygame.SRCALPHA)
main_character_up_1.blit(character_spritesheet, (0, 0), [16, 16, 32, 48])
main_character_up_2 = pygame.Surface([32, 48], pygame.SRCALPHA)
main_character_up_2.blit(character_spritesheet, (0, 0), [80, 16, 32, 48])
main_character_up_3 = pygame.Surface([32, 48], pygame.SRCALPHA)
main_character_up_3.blit(character_spritesheet, (0, 0), [144, 16, 32, 48])
main_character_right_0 = pygame.Surface([32, 48], pygame.SRCALPHA)
main_character_right_0.blit(character_spritesheet, (0, 0), [80, 80, 32, 48])
main_character_right_1 = pygame.Surface([32, 48], pygame.SRCALPHA)
main_character_right_1.blit(character_spritesheet, (0, 0), [16, 80, 32, 48])
main_character_right_2 = pygame.Surface([32, 48], pygame.SRCALPHA)
main_character_right_2.blit(character_spritesheet, (0, 0), [80, 80, 32, 48])
main_character_right_3 = pygame.Surface([32, 48], pygame.SRCALPHA)
main_character_right_3.blit(character_spritesheet, (0, 0), [144, 80, 32, 48])
main_character_down_0 = pygame.Surface([32, 48], pygame.SRCALPHA)
main_character_down_0.blit(character_spritesheet, (0, 0), [80, 144, 32, 48])
main_character_down_1 = pygame.Surface([32, 48], pygame.SRCALPHA)
main_character_down_1.blit(character_spritesheet, (0, 0), [16, 144, 32, 48])
main_character_down_2 = pygame.Surface([32, 48], pygame.SRCALPHA)
main_character_down_2.blit(character_spritesheet, (0, 0), [80, 144, 32, 48])
main_character_down_3 = pygame.Surface([32, 48], pygame.SRCALPHA)
main_character_down_3.blit(character_spritesheet, (0, 0), [144, 144, 32, 48])
main_character_left_0 = pygame.Surface([32, 48], pygame.SRCALPHA)
main_character_left_0.blit(character_spritesheet, (0, 0), [80, 208, 32, 48])
main_character_left_1 = pygame.Surface([32, 48], pygame.SRCALPHA)
main_character_left_1.blit(character_spritesheet, (0, 0), [16, 208, 32, 48])
main_character_left_2 = pygame.Surface([32, 48], pygame.SRCALPHA)
main_character_left_2.blit(character_spritesheet, (0, 0), [80, 208, 32, 48])
main_character_left_3 = pygame.Surface([32, 48], pygame.SRCALPHA)
main_character_left_3.blit(character_spritesheet, (0, 0), [144, 208, 32, 48])

# setting player's animation
CHARACTER_ANIMATION_RIGHT = pyganim.PygAnimation([
    (main_character_right_1, 0.2),
    (main_character_right_2, 0.2),
    (main_character_right_3, 0.2),
    (main_character_right_0, 0.2)])
CHARACTER_ANIMATION_LEFT = pyganim.PygAnimation([
    (main_character_left_1, 0.2),
    (main_character_left_2, 0.2),
    (main_character_left_3, 0.2),
    (main_character_left_0, 0.2)])
CHARACTER_ANIMATION_UP = pyganim.PygAnimation([
    (main_character_up_1, 0.2),
    (main_character_up_2, 0.2),
    (main_character_up_3, 0.2),
    (main_character_up_0, 0.2)])
CHARACTER_ANIMATION_DOWN = pyganim.PygAnimation([
    (main_character_down_1, 0.2),
    (main_character_down_2, 0.2),
    (main_character_down_3, 0.2),
    (main_character_down_0, 0.2)])

MOVE_SPEED = 8


class CharacterMain(pygame.sprite.Sprite):
    def __init__(self, x, y, last_move=None):
        super(CharacterMain, self).__init__()
        self.animation_on = None  # component for moving function
        self.last_move = last_move  # component for moving function
        self.count = 0  # component for moving function
        self.speed_walk = 4  # component for moving function (walk speed)
        self.bike_walk = 8  # component for moving function (bike speed)
        self.speed = 0  # start speed 0
        self.action = False  # setting action with anything
        self.action_delay = 0  # setting time between action

        self.poke_move = False  # component for poke (land) moving
        self.poke_last_move = self.last_move  # component for poke vector (moving)
        self.stop_field_right = False  # component for moving field
        self.stop_field_left = False  # component for moving field
        self.stop_field_up = False  # component for moving field
        self.stop_field_down = False  # component for moving field

        self.image = Surface([32, 48], pygame.SRCALPHA)  # our player Surface

        # setting rect and coordinates of player
        self.rect = Rect(x, y - 16, 32, 48)
        self.cord_of_player = [self.rect.x, self.rect.y + 16]
        self.right_cord_of_player = [self.rect.x + 32, self.rect.y + 32]
        self.left_cord_of_player = [self.rect.x, self.rect.y + 32]
        self.up_cord_of_player = [self.rect.x + 16, self.rect.y + 16]
        self.down_cord_of_player = [self.rect.x + 16, self.rect.y + 48]
        self.center_cord_of_player = [self.rect.x + 16, self.rect.y + 32]

        self.xvel = 0  # x-coordinate speed
        self.yvel = 0  # y-coordinate speed

    def update(self, world,
               left, right, up, down, f,
               top_cord, left_cord, right_cord, bottom_cord,
               items_rect, items, game, settings):

        if self.animation_on:  # if animation is ON (player moving == True)
            if self.count != 0:  # if animation is continuing
                self.poke_move = True  # start poke moving  (poke moving == True)
                if self.last_move == "left":
                    if world.type_of_map == "MAX":  # if map is "MAX" we also move field cords
                        if not self.stop_field_left:
                            self.count -= 4
                            world.field_x = world.field_x - self.speed
                            self.rect.x = self.rect.x - self.speed
                        else:
                            self.count -= 4
                            self.rect.x = self.rect.x - self.speed
                    else:
                        self.count -= 4
                        self.rect.x = self.rect.x - self.speed
                if self.last_move == "right":
                    if world.type_of_map == "MAX":
                        if not self.stop_field_right:
                            self.count -= 4
                            world.field_x = world.field_x + self.speed
                            self.rect.x = self.rect.x + self.speed
                        else:
                            self.count -= 4
                            self.rect.x = self.rect.x + self.speed
                    else:
                        self.count -= 4
                        self.rect.x = self.rect.x + self.speed
                if self.last_move == "up":
                    if world.type_of_map == "MAX":
                        if not self.stop_field_up:
                            self.count -= 4
                            world.field_y = world.field_y - self.speed
                            self.rect.y = self.rect.y - self.speed
                        else:
                            self.count -= 4
                            self.rect.y = self.rect.y - self.speed
                    else:
                        self.count -= 4
                        self.rect.y = self.rect.y - self.speed
                if self.last_move == "down":
                    if world.type_of_map == "MAX":
                        if not self.stop_field_down:
                            self.count -= 4
                            world.field_y = world.field_y + self.speed
                            self.rect.y = self.rect.y + self.speed
                        else:
                            self.count -= 4
                            self.rect.y = self.rect.y + self.speed
                    else:
                        self.count -= 4
                        self.rect.y = self.rect.y + self.speed
            else:
                # In this condition, we check the correctness character's position
                # (for the right collide with other objects)
                if self.rect.x % 32 >= 16:
                    self.rect.x = int(self.rect.x + (32 - (self.rect.x % 32)))
                elif self.rect.x % 32 < 16:
                    self.rect.x = int(self.rect.x - (self.rect.x % 32))
                if (self.rect.y + 16) % 32 >= 16:
                    self.rect.y = int((self.rect.y + 16) + (32 - ((self.rect.y + 16) % 32))) - 16
                elif (self.rect.y + 16) % 32 < 16:
                    self.rect.y = int((self.rect.y + 16) - ((self.rect.y + 16) % 32)) - 16
                self.animation_on = False  # stop player moving
                self.poke_move = False  # stop poke moving

        # updating players cords (his rect cords)
        self.cord_of_player = [self.rect.x, self.rect.y + 16]
        self.right_cord_of_player = [self.rect.x + 32, self.rect.y + 32]
        self.left_cord_of_player = [self.rect.x, self.rect.y + 32]
        self.up_cord_of_player = [self.rect.x + 16, self.rect.y + 16]
        self.down_cord_of_player = [self.rect.x + 16, self.rect.y + 48]
        self.center_cord_of_player = [self.rect.x + 16, self.rect.y + 32]

        if left:
            if settings.world_status == "MAIN":
                if not self.animation_on:
                    if self.speed == 4:
                        self.poke_last_move = self.last_move  # set last player move for poke moving (vector)
                if world.type_of_map == "MAX":
                    if world.field_x == 0:  # if field in top left
                        self.stop_field_left = True
                    elif self.cord_of_player[0] >= (world.current_map.width - 20) * settings.block_size:  # if field in top right
                        self.stop_field_left = True
                    else:
                        self.stop_field_left = False
                for i in items_rect:
                    if (i.rect.x + 32) == self.left_cord_of_player[0] and (i.rect.y + 16) == self.left_cord_of_player[1]:
                        if not self.animation_on:
                            self.speed = 0
                            self.count = 32  # setting count (of moving)
                            self.animation_on = True  # start animation move
                            self.last_move = "left"  # setting last_move

                for i in items:  # checking collide player with other items
                    if i.type == "npc":
                        if self.left_cord_of_player == i.right_cord_of_item:
                            if not self.animation_on:
                                self.speed = 0
                                self.count = 32  # setting count (of moving)
                                self.animation_on = True  # start animation move
                                self.last_move = "left"  # setting last_move

                if self.left_cord_of_player[0] == left_cord:  # check collide with borders of map
                    if not self.animation_on:
                        self.speed = 0
                        self.count = 32  # setting count (of moving)
                        self.animation_on = True  # start animation move
                        self.last_move = "left"  # setting last_move
                else:
                    if not self.animation_on:
                        self.speed = 4
                        self.count = 32  # setting count (of moving)
                        self.animation_on = True  # start animation move
                        self.last_move = "left"  # setting last_move
                self.image.fill((255, 255, 255, 0))

                # setting correct animation move
                if self.last_move == "right":
                    CHARACTER_ANIMATION_RIGHT.play()
                    CHARACTER_ANIMATION_RIGHT.blit(self.image, (0, 0))
                elif self.last_move == "down":
                    CHARACTER_ANIMATION_DOWN.play()
                    CHARACTER_ANIMATION_DOWN.blit(self.image, (0, 0))
                elif self.last_move == "up":
                    CHARACTER_ANIMATION_UP.play()
                    CHARACTER_ANIMATION_UP.blit(self.image, (0, 0))
                elif self.last_move == "left":
                    CHARACTER_ANIMATION_LEFT.play()
                    CHARACTER_ANIMATION_LEFT.blit(self.image, (0, 0))

                up = False  # when we are moving left or right, we can't move up or down
                down = False

        if right:
            if settings.world_status == "MAIN":
                if not self.animation_on:
                    if self.speed == 4:
                        self.poke_last_move = self.last_move  # set last player move for poke moving (vector)
                if world.type_of_map == "MAX":
                    if world.field_x + (39 * settings.block_size) == world.current_map.width * settings.block_size:
                        self.stop_field_right = True
                    elif self.cord_of_player[0] <= 19 * settings.block_size:
                        self.stop_field_right = True
                    else:
                        self.stop_field_right = False
                for i in items_rect:
                    if i.rect.x == self.right_cord_of_player[0] and (i.rect.y + 16) == self.right_cord_of_player[1]:
                        if not self.animation_on:
                            self.speed = 0
                            self.count = 32  # setting count (of moving)
                            self.animation_on = True  # start animation move
                            self.last_move = "right"  # setting last_move

                for i in items:  # checking collide player with other items
                    if i.type == "npc":
                        if self.right_cord_of_player == i.left_cord_of_item:
                            if not self.animation_on:
                                self.speed = 0
                                self.count = 32  # setting count (of moving)
                                self.animation_on = True  # start animation move
                                self.last_move = "right"  # setting last_move

                if self.right_cord_of_player[0] == right_cord:
                    if not self.animation_on:
                        self.speed = 0
                        self.count = 32  # setting count (of moving)
                        self.animation_on = True  # start animation move
                        self.last_move = "right"  # setting last_move
                else:
                    if not self.animation_on:
                        self.speed = 4
                        self.count = 32  # setting count (of moving)
                        self.animation_on = True  # start animation move
                        self.last_move = "right"  # setting last_move
                self.image.fill((255, 255, 255, 0))

                # setting correct animation move
                if self.last_move == "right":
                    CHARACTER_ANIMATION_RIGHT.play()
                    CHARACTER_ANIMATION_RIGHT.blit(self.image, (0, 0))
                elif self.last_move == "down":
                    CHARACTER_ANIMATION_DOWN.play()
                    CHARACTER_ANIMATION_DOWN.blit(self.image, (0, 0))
                elif self.last_move == "up":
                    CHARACTER_ANIMATION_UP.play()
                    CHARACTER_ANIMATION_UP.blit(self.image, (0, 0))
                elif self.last_move == "left":
                    CHARACTER_ANIMATION_LEFT.play()
                    CHARACTER_ANIMATION_LEFT.blit(self.image, (0, 0))

                up = False
                down = False

        if up:
            if settings.world_status == "DIALOG_ANSWER":
                for i in items:
                    if i.action:
                        i.up_answer = True

            if settings.world_status == "MAIN":
                if not self.animation_on:
                    if self.speed == 4:
                        self.poke_last_move = self.last_move  # set last player move for poke moving (vector)
                if world.type_of_map == "MAX":
                    if world.field_y == 0:
                        self.stop_field_up = True
                    elif self.cord_of_player[1] >= (world.current_map.height - 12) * settings.block_size:
                        self.stop_field_up = True
                    else:
                        self.stop_field_up = False
                for i in items_rect:
                    if (i.rect.x + 16) == self.up_cord_of_player[0] and (i.rect.y + 32) == self.up_cord_of_player[1]:
                        if not self.animation_on:
                            self.speed = 0
                            self.count = 32  # setting count (of moving)
                            self.animation_on = True  # start animation move
                            self.last_move = "up"  # setting last_move

                for i in items:  # checking collide player with other items
                    if i.type == "npc":
                        if self.up_cord_of_player == i.down_cord_of_item:
                            if not self.animation_on:
                                self.speed = 0
                                self.count = 32  # setting count (of moving)
                                self.animation_on = True  # start animation move
                                self.last_move = "up"  # setting last_move

                if self.up_cord_of_player[1] == top_cord:
                    if not self.animation_on:
                        self.speed = 0
                        self.count = 32  # setting count (of moving)
                        self.animation_on = True  # start animation move
                        self.last_move = "up"  # setting last_move
                else:
                    if not self.animation_on:
                        self.speed = 4
                        self.count = 32  # setting count (of moving)
                        self.animation_on = True  # start animation move
                        self.last_move = "up"  # setting last_move
                self.image.fill((255, 255, 255, 0))

                # setting correct animation move
                if self.last_move == "right":
                    CHARACTER_ANIMATION_RIGHT.play()
                    CHARACTER_ANIMATION_RIGHT.blit(self.image, (0, 0))
                elif self.last_move == "down":
                    CHARACTER_ANIMATION_DOWN.play()
                    CHARACTER_ANIMATION_DOWN.blit(self.image, (0, 0))
                elif self.last_move == "up":
                    CHARACTER_ANIMATION_UP.play()
                    CHARACTER_ANIMATION_UP.blit(self.image, (0, 0))
                elif self.last_move == "left":
                    CHARACTER_ANIMATION_LEFT.play()
                    CHARACTER_ANIMATION_LEFT.blit(self.image, (0, 0))

                right = False
                left = False

        if down:
            if settings.world_status == "DIALOG_ANSWER":
                for i in items:
                    if i.action:
                        i.down_answer = True

            if settings.world_status == "MAIN":
                if not self.animation_on:
                    if self.speed == 4:
                        self.poke_last_move = self.last_move  # set last player move for poke moving (vector)
                if world.type_of_map == "MAX":
                    if world.field_y + (23 * settings.block_size) == world.current_map.height * settings.block_size:
                        self.stop_field_down = True
                    elif self.cord_of_player[1] <= 11 * settings.block_size:
                        self.stop_field_down = True
                    else:
                        self.stop_field_down = False
                for i in items_rect:
                    if (i.rect.x + 16) == self.down_cord_of_player[0] and i.rect.y == self.down_cord_of_player[1]:
                        if not self.animation_on:
                            self.speed = 0
                            self.count = 32  # setting count (of moving)
                            self.animation_on = True  # start animation move
                            self.last_move = "down"  # setting last_move

                for i in items:  # checking collide player with other items
                    if i.type == "npc":
                        if self.down_cord_of_player == i.up_cord_of_item:
                            if not self.animation_on:
                                self.speed = 0
                                self.count = 32  # setting count (of moving)
                                self.animation_on = True  # start animation move
                                self.last_move = "down"  # setting last_move

                if self.down_cord_of_player[1] == bottom_cord:
                    if not self.animation_on:
                        self.speed = 0
                        self.count = 32  # setting count (of moving)
                        self.animation_on = True  # start animation move
                        self.last_move = "down"  # setting last_move
                else:
                    if not self.animation_on:
                        self.speed = 4
                        self.count = 32  # setting count (of moving)
                        self.animation_on = True  # start animation move
                        self.last_move = "down"  # setting last_move
                self.image.fill((255, 255, 255, 0))

                # setting correct animation move
                if self.last_move == "right":
                    CHARACTER_ANIMATION_RIGHT.play()
                    CHARACTER_ANIMATION_RIGHT.blit(self.image, (0, 0))
                elif self.last_move == "down":
                    CHARACTER_ANIMATION_DOWN.play()
                    CHARACTER_ANIMATION_DOWN.blit(self.image, (0, 0))
                elif self.last_move == "up":
                    CHARACTER_ANIMATION_UP.play()
                    CHARACTER_ANIMATION_UP.blit(self.image, (0, 0))
                elif self.last_move == "left":
                    CHARACTER_ANIMATION_LEFT.play()
                    CHARACTER_ANIMATION_LEFT.blit(self.image, (0, 0))

                    right = False
                    left = False

        if f:
            if self.action_delay != 0:
                self.action_delay -= 1
            else:
                self.action_delay = 3
                for i in items:
                    if i.action:
                        if settings.world_status == "MAIN" or settings.world_status == "DIALOG":
                            if (self.right_cord_of_player == i.left_cord_of_item) or \
                                    (self.left_cord_of_player == i.right_cord_of_item) or \
                                    (self.up_cord_of_player == i.down_cord_of_item) or \
                                    (self.down_cord_of_player == i.up_cord_of_item):
                                i.action_on = True
                                i.change = True
                        elif settings.world_status == "DIALOG_ANSWER":
                            i.change_with_active = True

        for i in items:  # checking collide player with other items
            if i.type == "teleporter":  # !!! TEST teleport method !!!
                if i.rect.collidepoint(self.center_cord_of_player):  # !!! TEST teleport method !!!
                    self.count = 0  # stop moving when teleporting
                    self.poke_move = False
                    i.teleport(game)

        if settings.world_status == "MAIN":
            if not (left or right):  # стоим, когда нет указаний идти
                CHARACTER_ANIMATION_LEFT.stop()
                CHARACTER_ANIMATION_RIGHT.stop()

            if not (up or down):  # стоим, когда нет указаний идти
                CHARACTER_ANIMATION_UP.stop()
                CHARACTER_ANIMATION_DOWN.stop()

    def draw(self, screen):  # draw player to map
        screen.blit(self.image, (self.rect.x, self.rect.y))

    def standing_animation(self, position):
        if position == "left":
            self.image.fill((255, 255, 255, 0))  # clear image with transparent color for next animation
            self.image.blit(main_character_left_0, (0, 0))  # positioning and bliting (rendering) player
        elif position == "right":
            self.image.fill((255, 255, 255, 0))
            self.image.blit(main_character_right_0, (0, 0))
        elif position == "up":
            self.image.fill((255, 255, 255, 0))
            self.image.blit(main_character_up_0, (0, 0))
        elif position == "down":
            self.image.fill((255, 255, 255, 0))
            self.image.blit(main_character_down_0, (0, 0))


class LandPoke(pygame.sprite.Sprite):
    def __init__(self, id_of_poke, type_of_poke, character):
        super(LandPoke, self).__init__()
        poke_spritesheet = pygame.image.load(resource_path(f"resources/pokemon/{type_of_poke}/{id_of_poke}/sprite.png"))
        if poke_spritesheet.get_height() == 256:
            self.size_of_poke = "min"
            poke_spritesheet = pygame.transform.scale(poke_spritesheet, (128, 128))
            self.image = Surface([32, 32], pygame.SRCALPHA)  # our player Surface
        elif poke_spritesheet.get_height() == 512:
            self.size_of_poke = "max"
            poke_spritesheet = pygame.transform.scale(poke_spritesheet, (256, 256))
            self.image = Surface([64, 64], pygame.SRCALPHA)  # our player Surface

        if type_of_poke == "shiny":
            if self.size_of_poke == "min":
                self.shiny_stars = Surface([32, 32], pygame.SRCALPHA)
            elif self.size_of_poke == "max":
                self.shiny_stars = Surface([64, 64], pygame.SRCALPHA)
        else:
            self.shiny_stars = False

        # setting rect and coordinates of player
        if self.size_of_poke == "min":
            if character.last_move == "down":
                self.rect = Rect(character.rect.x, character.rect.y - 16, 32, 32)
            elif character.last_move == "up":
                self.rect = Rect(character.rect.x, character.rect.y + 48, 32, 32)
            elif character.last_move == "left":
                self.rect = Rect(character.rect.x + 32, character.rect.y + 16, 32, 32)
            elif character.last_move == "right":
                self.rect = Rect(character.rect.x - 32, character.rect.y + 16, 32, 32)
        elif self.size_of_poke == "max":
            if character.last_move == "down":
                self.rect = Rect(character.rect.x - 16, character.rect.y - 32, 64, 46)
            elif character.last_move == "up":
                self.rect = Rect(character.rect.x - 16, character.rect.y + 48, 64, 64)
            elif character.last_move == "left":
                self.rect = Rect(character.rect.x + 32, character.rect.y - 8, 64, 64)
            elif character.last_move == "right":
                self.rect = Rect(character.rect.x - 64, character.rect.y - 8, 64, 64)

        if self.size_of_poke == "min":
            self.land_poke_up_0 = pygame.Surface([32, 32], pygame.SRCALPHA)
            self.land_poke_up_0.blit(poke_spritesheet, (0, 0), [0, 96, 32, 32])
            self.land_poke_up_1 = pygame.Surface([32, 32], pygame.SRCALPHA)
            self.land_poke_up_1.blit(poke_spritesheet, (0, 0), [32, 96, 32, 32])
            self.land_poke_up_2 = pygame.Surface([32, 32], pygame.SRCALPHA)
            self.land_poke_up_2.blit(poke_spritesheet, (0, 0), [64, 96, 32, 32])
            self.land_poke_up_3 = pygame.Surface([32, 32], pygame.SRCALPHA)
            self.land_poke_up_3.blit(poke_spritesheet, (0, 0), [96, 96, 32, 32])

            self.land_poke_right_0 = pygame.Surface([32, 32], pygame.SRCALPHA)
            self.land_poke_right_0.blit(poke_spritesheet, (0, 0), [0, 64, 32, 32])
            self.land_poke_right_1 = pygame.Surface([32, 32], pygame.SRCALPHA)
            self.land_poke_right_1.blit(poke_spritesheet, (0, 0), [32, 64, 32, 32])
            self.land_poke_right_2 = pygame.Surface([32, 32], pygame.SRCALPHA)
            self.land_poke_right_2.blit(poke_spritesheet, (0, 0), [64, 64, 32, 32])
            self.land_poke_right_3 = pygame.Surface([32, 32], pygame.SRCALPHA)
            self.land_poke_right_3.blit(poke_spritesheet, (0, 0), [96, 64, 32, 32])

            self.land_poke_down_0 = pygame.Surface([32, 32], pygame.SRCALPHA)
            self.land_poke_down_0.blit(poke_spritesheet, (0, 0), [0, 0, 32, 32])
            self.land_poke_down_1 = pygame.Surface([32, 32], pygame.SRCALPHA)
            self.land_poke_down_1.blit(poke_spritesheet, (0, 0), [32, 0, 32, 32])
            self.land_poke_down_2 = pygame.Surface([32, 32], pygame.SRCALPHA)
            self.land_poke_down_2.blit(poke_spritesheet, (0, 0), [64, 0, 32, 32])
            self.land_poke_down_3 = pygame.Surface([32, 32], pygame.SRCALPHA)
            self.land_poke_down_3.blit(poke_spritesheet, (0, 0), [96, 0, 32, 32])

            self.land_poke_left_0 = pygame.Surface([32, 32], pygame.SRCALPHA)
            self.land_poke_left_0.blit(poke_spritesheet, (0, 0), [0, 32, 32, 32])
            self.land_poke_left_1 = pygame.Surface([32, 32], pygame.SRCALPHA)
            self.land_poke_left_1.blit(poke_spritesheet, (0, 0), [32, 32, 32, 32])
            self.land_poke_left_2 = pygame.Surface([32, 32], pygame.SRCALPHA)
            self.land_poke_left_2.blit(poke_spritesheet, (0, 0), [64, 32, 32, 32])
            self.land_poke_left_3 = pygame.Surface([32, 32], pygame.SRCALPHA)
            self.land_poke_left_3.blit(poke_spritesheet, (0, 0), [96, 32, 32, 32])

        elif self.size_of_poke == "max":
            self.land_poke_up_0 = pygame.Surface([64, 64], pygame.SRCALPHA)
            self.land_poke_up_0.blit(poke_spritesheet, (0, 0), [0, 192, 64, 64])
            self.land_poke_up_1 = pygame.Surface([64, 64], pygame.SRCALPHA)
            self.land_poke_up_1.blit(poke_spritesheet, (0, 0), [64, 192, 64, 64])
            self.land_poke_up_2 = pygame.Surface([64, 64], pygame.SRCALPHA)
            self.land_poke_up_2.blit(poke_spritesheet, (0, 0), [128, 192, 64, 64])
            self.land_poke_up_3 = pygame.Surface([64, 64], pygame.SRCALPHA)
            self.land_poke_up_3.blit(poke_spritesheet, (0, 0), [192, 192, 64, 64])

            self.land_poke_right_0 = pygame.Surface([64, 64], pygame.SRCALPHA)
            self.land_poke_right_0.blit(poke_spritesheet, (0, 0), [0, 128, 64, 64])
            self.land_poke_right_1 = pygame.Surface([64, 64], pygame.SRCALPHA)
            self.land_poke_right_1.blit(poke_spritesheet, (0, 0), [64, 128, 64, 64])
            self.land_poke_right_2 = pygame.Surface([64, 64], pygame.SRCALPHA)
            self.land_poke_right_2.blit(poke_spritesheet, (0, 0), [128, 128, 64, 64])
            self.land_poke_right_3 = pygame.Surface([64, 64], pygame.SRCALPHA)
            self.land_poke_right_3.blit(poke_spritesheet, (0, 0), [192, 128, 64, 64])

            self.land_poke_down_0 = pygame.Surface([64, 64], pygame.SRCALPHA)
            self.land_poke_down_0.blit(poke_spritesheet, (0, 0), [0, 0, 64, 64])
            self.land_poke_down_1 = pygame.Surface([64, 64], pygame.SRCALPHA)
            self.land_poke_down_1.blit(poke_spritesheet, (0, 0), [64, 0, 64, 64])
            self.land_poke_down_2 = pygame.Surface([64, 64], pygame.SRCALPHA)
            self.land_poke_down_2.blit(poke_spritesheet, (0, 0), [128, 0, 64, 64])
            self.land_poke_down_3 = pygame.Surface([64, 64], pygame.SRCALPHA)
            self.land_poke_down_3.blit(poke_spritesheet, (0, 0), [192, 0, 64, 64])

            self.land_poke_left_0 = pygame.Surface([64, 64], pygame.SRCALPHA)
            self.land_poke_left_0.blit(poke_spritesheet, (0, 0), [0, 64, 64, 64])
            self.land_poke_left_1 = pygame.Surface([64, 64], pygame.SRCALPHA)
            self.land_poke_left_1.blit(poke_spritesheet, (0, 0), [64, 64, 64, 64])
            self.land_poke_left_2 = pygame.Surface([64, 64], pygame.SRCALPHA)
            self.land_poke_left_2.blit(poke_spritesheet, (0, 0), [128, 64, 64, 64])
            self.land_poke_left_3 = pygame.Surface([64, 64], pygame.SRCALPHA)
            self.land_poke_left_3.blit(poke_spritesheet, (0, 0), [192, 64, 64, 64])

        # setting poke's animation
        self.LAND_POKE_RIGHT = pyganim.PygAnimation([
            (self.land_poke_right_1, 0.2),
            (self.land_poke_right_2, 0.2),
            (self.land_poke_right_3, 0.2),
            (self.land_poke_right_0, 0.2)])
        self.LAND_POKE_LEFT = pyganim.PygAnimation([
            (self.land_poke_left_1, 0.2),
            (self.land_poke_left_2, 0.2),
            (self.land_poke_left_3, 0.2),
            (self.land_poke_left_0, 0.2)])
        self.LAND_POKE_UP = pyganim.PygAnimation([
            (self.land_poke_up_1, 0.2),
            (self.land_poke_up_2, 0.2),
            (self.land_poke_up_3, 0.2),
            (self.land_poke_up_0, 0.2)])
        self.LAND_POKE_DOWN = pyganim.PygAnimation([
            (self.land_poke_down_1, 0.2),
            (self.land_poke_down_2, 0.2),
            (self.land_poke_down_3, 0.2),
            (self.land_poke_down_0, 0.2)])

    def update(self, left, right, up, down, poke_on, last_move_player, player_speed, character_move):
        if self.shiny_stars:
            if self.size_of_poke == "min":
                self.shiny_stars.fill((255, 255, 255, 0))
                stars_animation.play()
                stars_animation.blit(self.shiny_stars, (0, 0))
            elif self.size_of_poke == "max":
                self.shiny_stars.fill((255, 255, 255, 0))
                stars_animation_big.play()
                stars_animation_big.blit(self.shiny_stars, (0, 0))

        if left or up or down or right:
            self.image.fill((255, 255, 255, 0))  # clearing image of land poke
            if last_move_player == "right":
                self.LAND_POKE_RIGHT.play()
                self.LAND_POKE_RIGHT.blit(self.image, (0, 0))
            elif last_move_player == "left":
                self.LAND_POKE_LEFT.play()
                self.LAND_POKE_LEFT.blit(self.image, (0, 0))
            elif last_move_player == "up":
                self.LAND_POKE_UP.play()
                self.LAND_POKE_UP.blit(self.image, (0, 0))
            elif last_move_player == "down":
                self.LAND_POKE_DOWN.play()
                self.LAND_POKE_DOWN.blit(self.image, (0, 0))

        if not (left or right):  # стоим, когда нет указаний идти
            self.LAND_POKE_LEFT.stop()
            self.LAND_POKE_RIGHT.stop()

        if not (up or down):  # стоим, когда нет указаний идти
            self.LAND_POKE_UP.stop()
            self.LAND_POKE_DOWN.stop()

        if poke_on:
            if self.size_of_poke == "min":
                if last_move_player == "right":
                    self.rect.x = self.rect.x + player_speed
                elif last_move_player == "left":
                    self.rect.x = self.rect.x - player_speed
                elif last_move_player == "up":
                    self.rect.y = self.rect.y - player_speed
                elif last_move_player == "down":
                    self.rect.y = self.rect.y + player_speed
            elif self.size_of_poke == "max":
                if player_speed != 0:
                    if character_move == last_move_player:
                        if last_move_player == "right":
                            self.rect.x = self.rect.x + player_speed
                        elif last_move_player == "left":
                            self.rect.x = self.rect.x - player_speed
                        elif last_move_player == "up":
                            self.rect.y = self.rect.y - player_speed
                        elif last_move_player == "down":
                            self.rect.y = self.rect.y + player_speed
                    elif (last_move_player == "right" and character_move == "left") or \
                            (last_move_player == "left" and character_move == "right"):
                        if last_move_player == "right":
                            self.rect.x = self.rect.x + player_speed * 2
                        elif last_move_player == "left":
                            self.rect.x = self.rect.x - player_speed * 2
                        elif last_move_player == "up":
                            self.rect.y = self.rect.y - player_speed * 2
                        elif last_move_player == "down":
                            self.rect.y = self.rect.y + player_speed * 2
                    elif (last_move_player == "down" and character_move == "up") or \
                            (last_move_player == "up" and character_move == "down"):
                        if last_move_player == "up":
                            self.rect.y = self.rect.y - player_speed * 1.5
                        elif last_move_player == "down":
                            self.rect.y = self.rect.y + player_speed * 1.5
                    elif (last_move_player == "up" and character_move == "right") or \
                            (last_move_player == "up" and character_move == "left"):
                        if character_move == "right":
                            self.rect.y = self.rect.y - player_speed * 1.75
                            self.rect.x = self.rect.x - 2
                        elif character_move == "left":
                            self.rect.y = self.rect.y - player_speed * 1.75
                            self.rect.x = self.rect.x + 2
                    elif (last_move_player == "down" and character_move == "right") or \
                            (last_move_player == "down" and character_move == "left"):
                        if character_move == "right":
                            self.rect.y = self.rect.y + player_speed * 0.75
                            self.rect.x = self.rect.x - 2
                        elif character_move == "left":
                            self.rect.y = self.rect.y + player_speed * 0.75
                            self.rect.x = self.rect.x + 2
                    elif (last_move_player == "right" and character_move == "up") or \
                            (last_move_player == "right" and character_move == "down"):
                        if character_move == "up":
                            self.rect.x = self.rect.x + player_speed * 1.5
                            self.rect.y = self.rect.y + 3
                        elif character_move == "down":
                            self.rect.x = self.rect.x + player_speed * 1.5
                            self.rect.y = self.rect.y + 1
                    elif (last_move_player == "left" and character_move == "up") or \
                            (last_move_player == "left" and character_move == "down"):
                        if character_move == "up":
                            self.rect.x = self.rect.x - player_speed * 1.5
                            self.rect.y = self.rect.y + 3
                        elif character_move == "down":
                            self.rect.x = self.rect.x - player_speed * 1.5
                            self.rect.y = self.rect.y + 1
                    # else:
                    #     if last_move_player == "right":
                    #         self.rect.x = self.rect.x + player_speed * 2
                    #     elif last_move_player == "left":
                    #         self.rect.x = self.rect.x - player_speed * 2
                    #     elif last_move_player == "up":
                    #         self.rect.y = self.rect.y - player_speed * 2
                    #     elif last_move_player == "down":
                    #         self.rect.y = self.rect.y + player_speed * 2

    def standing_animation(self, position):
        if position == "left":
            self.image.fill((255, 255, 255, 0))  # clear image with transparent color for next animation
            self.image.blit(self.land_poke_left_0, (0, 0))  # positioning and bliting (rendering) player
        elif position == "right":
            self.image.fill((255, 255, 255, 0))
            self.image.blit(self.land_poke_right_0, (0, 0))
        elif position == "up":
            self.image.fill((255, 255, 255, 0))
            self.image.blit(self.land_poke_up_0, (0, 0))
        elif position == "down":
            self.image.fill((255, 255, 255, 0))
            self.image.blit(self.land_poke_down_0, (0, 0))

    def draw(self, screen):  # draw player to map
        if self.shiny_stars:
            screen.blit(self.shiny_stars, (self.rect.x, self.rect.y))
        screen.blit(self.image, (self.rect.x, self.rect.y))
