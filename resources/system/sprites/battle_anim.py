import pyganim
import pygame


class BattleAttackAnimSetter:
    def __init__(self, img_background, damage_poke_getter, move_anim=None):
        self.image_background = img_background
        self.transparent_cube_me = pygame.Surface([200, 200], pygame.SRCALPHA)
        self.transparent_cube_me.blit(img_background, (0, 0), [15, 183, 200, 200])
        self.transparent_cube_foe = pygame.Surface([200, 200], pygame.SRCALPHA)
        self.transparent_cube_foe.blit(img_background, (0, 0), [320, 25, 200, 200])
        for i in range(1, 19):
            exec(f"self.frame_{i} = pygame.Surface([570, 400], pygame.SRCALPHA)")
            exec(f"self.frame_{i}.fill((0, 0, 0, 0))")

        if move_anim is None:
            if damage_poke_getter == "A":
                for i in range(1, 19):
                    if (0 < i < 4) or (6 < i < 10) or (12 < i < 16):
                        exec(f"self.frame_{i}.blit(self.transparent_cube_me, [15, 183])")

        if move_anim is None:
            if damage_poke_getter == "B":
                for i in range(1, 19):
                    if (0 < i < 4) or (6 < i < 10) or (12 < i < 16):
                        exec(f"self.frame_{i}.blit(self.transparent_cube_foe, [320, 25])")

        self.battle_attack_anim = pyganim.PygAnimation([
            (self.frame_1, 0.05),
            (self.frame_2, 0.05),
            (self.frame_3, 0.05),
            (self.frame_4, 0.05),
            (self.frame_5, 0.05),
            (self.frame_6, 0.05),
            (self.frame_7, 0.05),
            (self.frame_8, 0.05),
            (self.frame_9, 0.05),
            (self.frame_10, 0.05),
            (self.frame_11, 0.05),
            (self.frame_12, 0.05),
            (self.frame_13, 0.05),
            (self.frame_14, 0.05),
            (self.frame_15, 0.05),
            (self.frame_16, 0.05),
            (self.frame_17, 0.05),
            (self.frame_18, 0.05)])
        self.battle_attack_anim.loop = not self.battle_attack_anim.loop

    def play(self):
        self.battle_attack_anim.play()

    def draw(self, screen):
        if not self.battle_attack_anim.state == "stopped":
            self.battle_attack_anim.blit(screen, [9, 50])


