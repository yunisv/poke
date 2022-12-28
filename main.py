from pygame import *
import pygame
import sys
from tiles import *
from character import *
from places import *
import pickle
from setting import *

from battle import *

clock = pygame.time.Clock()  # setting fps (clock pygame)
items = pygame.sprite.Group()  # pygame sprite's group for maps


def window_setter(layer_wid, layer_len, type_of_map):
    if type_of_map == "MINI":
        x = (settings.WIDTH - layer_wid) / 2
        y = (settings.HEIGHT - layer_len) / 2
        return x, y
    else:
        x = (settings.WIDTH - 39 * settings.block_size) / 2
        y = (settings.HEIGHT - 23 * settings.block_size) / 2
        return x, y


def place_loading_from_file(code):
    if code == "TestHouse":
        return TileMap('resources/map/testhouse.json')
    elif code == "TestMap":
        return TileMap('resources/map/test_map.json')
    elif code == "TestHouse2":
        return TileMap('resources/map/testhouse2.json')


class CurrentGame:
    def __init__(self, place_for_map, player_x_pos=None, player_y_pos=None):
        self.current_place = CurrentMap(place_for_map, player_x_pos, player_y_pos)
        place_loading(items, settings.current_location)

    @staticmethod
    def teleport_setter(place):  # teleporting player function
        if place == "from_TestHouse_to_TestMap":
            settings.current_location = "TestMap"
        elif place == "from_TestMap_to_TestHouse":
            settings.current_location = "TestHouse"
        elif place == "from_TestHouse_to_TestHouse2":
            settings.current_location = "TestHouse2"
        elif place == "from_TestHouse2_to_TestHouse":
            settings.current_location = "TestHouse"

    def map_changer(self, place_to_move, player_standing_animation, player_x_pos=None, player_y_pos=None):
        # noinspection PyGlobalUndefined
        global player, right, left, down, up, f_button, land_poke
        del self.current_place, land_poke
        self.teleport_setter(place_to_move)  # setting new class (location)

        # setting player position
        player.rect.x = player_x_pos
        player.rect.y = player_y_pos - 16

        # updating screen
        loading_video.preview()  # start loading video
        screen.fill(settings.BLACK)  # clearing screen
        right = left = down = up = False  # stop movement player in transporting
        f_button = False
        player.standing_animation(player_standing_animation)  # staying animation
        land_poke = LandPoke(settings.player_pokes.poke_1.id_pokedex,
                             settings.player_pokes.poke_1.type_poke, player)  # creating poke (land)
        land_poke.standing_animation(player_standing_animation)  # start position of poke

        # setting current place (map)
        self.current_place = CurrentMap(place_loading_from_file(settings.current_location),
                                        player_x_pos, player_y_pos)
        place_loading(items, settings.current_location)  # loading items (additionally items)

        self.current_place.blit_background_to_layer()  # bliting layers


class CurrentMap:

    def __init__(self, place, player_x_pos=None, player_y_pos=None):
        self.type_of_map = None
        self.current_map = place  # loading current map
        self.layer_internal = Surface((place.width * settings.block_size, place.height * settings.block_size))
        self.layer_external = Surface((place.width * settings.block_size, place.height * settings.block_size),
                                      pygame.SRCALPHA)  # create external surface

        if place.width * settings.block_size > 1248 or place.height * settings.block_size > 736:
            # field for moving
            self.field = Surface((39 * settings.block_size, 23 * settings.block_size), pygame.SRCALPHA)
            self.field = Surface((39 * settings.block_size, 23 * settings.block_size), pygame.SRCALPHA)
            self.field_rect = self.field.get_rect()
            self.layer_internal.blit(self.field, (0, 0))
            self.type_of_map = "MAX"
        else:
            self.type_of_map = "MINI"

        self.coordinate = window_setter(place.width * settings.block_size, place.height * settings.block_size,
                                        self.type_of_map)
        self.field_x = None  # if max map, use this method
        self.field_y = None  # if max map, use this method
        self.player_x_pos = player_x_pos  # if max map, use this method
        self.player_y_pos = player_y_pos  # if max map, use this method
        self.field_setter()  # setting field configuration

        self.top_cord = self.current_map.top_cord
        self.bottom_cord = self.current_map.bottom_cord
        self.left_cord = self.current_map.left_cord
        self.right_cord = self.current_map.right_cord

    def field_setter(self):
        self.field_x = self.player_x_pos - (19 * settings.block_size)
        self.field_y = self.player_y_pos - (11 * settings.block_size)

        if self.field_x < 0:
            self.field_x = 0
        elif self.field_x + (39 * 32) >= self.current_map.width * 32:
            self.field_x = self.current_map.width * 32 - (39 * 32)
        if self.field_y < 0:
            self.field_y = 0
        elif self.field_y + (23 * 32) >= self.current_map.height * 32:
            self.field_y = self.current_map.height * 32 - (23 * 32)

    def blit_background_to_layer(self):
        self.layer_internal.blit(self.current_map.background_internal, (0, 0))
        self.layer_external.blit(self.current_map.background_external, (0, 0))

    def map_draw(self, window):  # draw function for mini map
        window.blit(self.layer_internal, self.coordinate)
        window.blit(self.layer_external, self.coordinate)

    def field_draw(self, window):  # draw function for max map
        self.field.blit(self.layer_internal, (0, 0), (self.field_x, self.field_y,
                                                      39 * settings.block_size, 23 * settings.block_size))
        self.field.blit(self.layer_external, (0, 0), (self.field_x, self.field_y,
                                                      39 * settings.block_size, 23 * settings.block_size))
        window.blit(self.field, self.coordinate)

    def draw_setter(self, window):  # function for choosing draw method (result depends on the map)
        if self.type_of_map == "MAX":
            return self.field_draw(window)
        else:
            return self.map_draw(window)


pygame.init()  # initialize pygame module

try:  # here we try loading save file
    with open("savepoint.pkl", "rb") as fp:  # open saved file
        current_location, player_x, player_y, last_move_p = pickle.load(
            fp)  # loading current_place where we stayed last time
        settings = Setting(player_x, player_y, current_location)
        world1 = CurrentGame(place_loading_from_file(settings.current_location),
                             player_x_pos=settings.player_x, player_y_pos=settings.player_y)
        # world creation in that place
        settings.last_move_setter(last_move_p)
except FileNotFoundError:  # if we don't save world before (or just create new world), creating new world
    settings = Setting()
    world1 = CurrentGame(place_loading_from_file(settings.current_location),
                         player_x_pos=settings.player_x, player_y_pos=settings.player_y)  # world creation

screen = pygame.display.set_mode((settings.WIDTH, settings.HEIGHT), DOUBLEBUF)  # create main window
pygame.display.set_caption("Pokemon Red")  # name of game
font_standart = pygame.font.SysFont('Times New Roman', 30)  # setting font
font = pygame.font.Font(resource_path("resources/font/Pixel_Times.ttf"), 30)  # setting font

world1.current_place.blit_background_to_layer()  # bliting items and background from layers to our world-class

player = CharacterMain(settings.player_x, settings.player_y, settings.last_move)  # creating player
player.standing_animation(settings.last_move)  # start position of player
# creating poke (land)
land_poke = LandPoke(settings.player_pokes.poke_1.id_pokedex, settings.player_pokes.poke_1.type_poke, player)
land_poke.standing_animation(settings.last_move)  # start position of poke
left = right = up = down = False  # player is staying when start game
f_button = False  # action button

mouse_cursor = None  # value for setting sprite, which will be clicked by mouse
mouse_sprite_group = pygame.sprite.Group()
x_diff = 0  # difference between clicked pos and sprite (std-0)
y_diff = 0  # difference between clicked pos and sprite (std-0)


while True:
    world1.current_place.draw_setter(screen)
    world1.current_place.layer_internal.blit(world1.current_place.current_map.background_internal,
                                             (0, 0))  # clearing image after animations

    # if the event is quit means we clicked on the close window button
    is_settled = False  # mouse set action (std-False)
    collided_item = None  # collided item ( its mean when we collide 2 system sprite )
    for e in pygame.event.get():
        # check for closing window
        if e.type == pygame.QUIT:
            with open("savepoint.pkl", "wb") as fp:  # saving our world
                player_x = player.cord_of_player[0]
                player_y = player.cord_of_player[1]
                last_move_p = player.last_move
                pickle.dump([settings.current_location, player_x, player_y, last_move_p], fp)
            pygame.quit()
            sys.exit()

        if e.type == KEYDOWN and e.key == K_LEFT:
            left = True
        if e.type == KEYDOWN and e.key == K_RIGHT:
            right = True
        if e.type == KEYDOWN and e.key == K_UP:
            up = True
        if e.type == KEYDOWN and e.key == K_DOWN:
            down = True
        if e.type == KEYDOWN and e.key == K_f:
            f_button = True

        if e.type == KEYUP and e.key == K_RIGHT:
            right = False
            if settings.world_status == "MAIN":
                player.standing_animation("right")
        if e.type == KEYUP and e.key == K_LEFT:
            left = False
            if settings.world_status == "MAIN":
                player.standing_animation("left")
        if e.type == KEYUP and e.key == K_UP:
            up = False
            if settings.world_status == "MAIN":
                player.standing_animation("up")
        if e.type == KEYUP and e.key == K_DOWN:
            down = False
            if settings.world_status == "MAIN":
                player.standing_animation("down")
        if e.type == KEYUP and e.key == K_f:
            f_button = False

        if e.type == pygame.MOUSEBUTTONDOWN:
            # Из всех имеющих спрайтов в system_mech определяется, нажата ли мышка на какой-либо спрайт.
            # если да, тов курсор записывается данный спрайт, а затем выполняется дальнейшее указания.
            for sprite in system_mech:  # getting all sprites from system_mech
                # getting sprites type="icon_poke"
                if sprite.type_system == "icon_poke" or sprite.type_system == "poke_info":
                    if sprite.rect.collidepoint(pygame.mouse.get_pos()):  # getting clicked sprite
                        mouse_cursor = sprite  # getting mouse_curso
                        x_diff = e.pos[0] - mouse_cursor.rect.x
                        y_diff = e.pos[1] - mouse_cursor.rect.y

        if pygame.mouse.get_pressed()[0] and mouse_cursor:
            if mouse_cursor.type_system == "icon_poke" or "poke_info":
                try:
                    mouse_cursor.rect.x = e.pos[0] - x_diff
                    mouse_cursor.rect.y = e.pos[1] - y_diff
                except AttributeError:
                    pass

        if e.type == pygame.MOUSEBUTTONUP:
            if mouse_cursor:
                if mouse_cursor.type_system == "icon_poke":
                    # if we just clicked on "icon_poke"
                    if mouse_cursor.rect.x == mouse_cursor.x_standart and mouse_cursor.rect.y == mouse_cursor.y_standart:
                        # if poke_info is not exist (sprite) => create
                        if not settings.poke_info:
                            if mouse_cursor.poke_exist:
                                poke_info = Poke_info(125, 50, mouse_cursor.id_db_poke, mouse_cursor.db)
                                system_mech.poke_info_sprite = poke_info
                                system_mech.add(poke_info)
                                settings.poke_info = True
                        # if poke_info is exist (sprite) => update
                        else:
                            if mouse_cursor.poke_exist:
                                system_mech.poke_info_sprite_x = system_mech.poke_info_sprite.rect.x  # copying last x
                                system_mech.poke_info_sprite_y = system_mech.poke_info_sprite.rect.y  # copying last y
                                system_mech.remove(system_mech.poke_info_sprite)  # deleting poke_info
                                system_mech.poke_info_sprite = None  # clearing poke_info

                                # updating current poke_info (sprite)
                                poke_info = Poke_info(system_mech.poke_info_sprite_x, system_mech.poke_info_sprite_y,
                                                      mouse_cursor.id_db_poke, mouse_cursor.db)
                                system_mech.add(poke_info)
                                system_mech.poke_info_sprite = poke_info
                                settings.poke_info = True
                    # if we collide it with other sprites
                    else:
                        for sprite in system_mech:
                            if sprite.type_system == "icon_poke":
                                if sprite != mouse_cursor:  # except itself
                                    if sprite.poke_exist:  # if there is poke in slot
                                        if sprite.rect.collidepoint(pygame.mouse.get_pos()):
                                            is_settled = True
                                            collided_item = sprite

                        if is_settled:
                            settings.player_pokes.changer_poke_icon(collided_item, mouse_cursor, system_mech)
                            del land_poke  # delete current land poke
                            # And create a new land poke
                            land_poke = LandPoke(settings.player_pokes.poke_1.id_pokedex,
                                                 settings.player_pokes.poke_1.type_poke, player)
                            land_poke.standing_animation(player.last_move)  # start position of poke
                        else:
                            mouse_cursor.rect.x = mouse_cursor.x_standart
                            mouse_cursor.rect.y = mouse_cursor.y_standart
                elif mouse_cursor.type_system == "poke_info":
                    # checking, which button we pressed

                    # if we're closing sprite (close it)
                    if mouse_cursor.press_checker(e.pos[0], e.pos[1]) == "close_sprite":
                        system_mech.remove(mouse_cursor)
                        settings.poke_info = False
                    # if we're updating sprite (change its moves)
                    elif mouse_cursor.press_checker(e.pos[0], e.pos[1]) == "update_sprite":
                        system_mech.poke_info_sprite_x = system_mech.poke_info_sprite.rect.x  # copying last x
                        system_mech.poke_info_sprite_y = system_mech.poke_info_sprite.rect.y  # copying last y
                        system_mech.remove(system_mech.poke_info_sprite)  # deleting poke_info
                        system_mech.poke_info_sprite = None  # clearing poke_info

                        # updating current poke_info (sprite)
                        poke_info = Poke_info(system_mech.poke_info_sprite_x, system_mech.poke_info_sprite_y,
                                              mouse_cursor.id_db_poke, mouse_cursor.db)
                        system_mech.add(poke_info)
                        system_mech.poke_info_sprite = poke_info
                        settings.poke_info = True

            mouse_cursor = None
            x_diff = 0
            y_diff = 0

    player.update(world1.current_place,
                  left, right, up, down, f_button, world1.current_place.top_cord,
                  world1.current_place.left_cord, world1.current_place.right_cord, world1.current_place.bottom_cord,
                  world1.current_place.current_map.background_internal_items_with_rect, items, world1, settings)
    land_poke.update(left, right, up, down, player.poke_move, player.poke_last_move, player.speed, player.last_move)
    land_poke.draw(world1.current_place.layer_internal)
    player.draw(world1.current_place.layer_internal)

    items.update(player, world1.current_place.layer_internal, font, system_mech, settings)
    system_mech.update(screen)

    clock.tick(settings.FPS)
    pygame.display.update()
