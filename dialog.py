import pygame
from pygame import *
from npc import NPC, Dialogue, sans_sound


class Dialog_box(pygame.sprite.Sprite):
    def __init__(self, x, y, text, text2, text3, text4, *questions):
        super(Dialog_box, self).__init__()
        self.type = "item"

        self.action = True  # setting action mechanic
        self.action_on = False  # setting action mechanic
        self.dialogue = None
        self.dialogue_create = True  # setting action mechanic
        self.talking = False  # setting, would be npc talk or no
        self.text_default = text.split("|")
        self.text_default2 = text2.split("|")
        self.text_default3 = text3.split("|")
        self.text_default4 = text4.split("|")
        self.text_content = text.split("|")
        self.text_content2 = text2.split("|")
        self.text_content3 = text3.split("|")
        self.text_content4 = text4.split("|")
        self.text = ""  # our text
        self.text2 = ""  # our text
        self.text3 = ""  # our text
        self.text4 = ""  # our text
        self.color1 = (0, 0, 0)  # color text (default)
        self.color2 = (0, 0, 0)  # color text (default)
        self.color3 = (0, 0, 0)  # color text (default)
        self.color4 = (0, 0, 0)  # color text (default)
        self.letter_index = 0  # setting, would be npc talk or no
        self.letter_index2 = 0  # setting, would be npc talk or no
        self.letter_index3 = 0  # setting, would be npc talk or no
        self.letter_index4 = 0  # setting, would be npc talk or no
        self.text_index = 0  # setting index of text_content
        self.delay_text = 5  # delay between text (dialog) change
        self.change = False  # setting action mechanic

        self.up_answer = False  # setting action mechanic
        self.down_answer = False  # setting action mechanic
        self.change_with_active = False  # setting action mechanic
        self.fps_answer_delay = 3  # setting action mechanic

        self.questions = []
        self.index_of_answers = 0
        self.color_not_active = (210, 204, 22)
        self.color_active = (210, 148, 22)
        self.answer = 2  # default answer index
        for question in questions:
            self.questions.append(question)

        self.image = Surface([32, 32], pygame.SRCALPHA)  # our player Surface

        self.rect = Rect(x, y, 32, 32)
        self.cord_of_npc = [self.rect.x, self.rect.y]
        self.right_cord_of_item = [self.rect.x + 32, self.rect.y + 16]
        self.left_cord_of_item = [self.rect.x, self.rect.y + 16]
        self.up_cord_of_item = [self.rect.x + 16, self.rect.y]
        self.down_cord_of_item = [self.rect.x + 16, self.rect.y + 32]
        self.center_cord_of_item = [self.rect.x + 16, self.rect.y + 16]

    def set_default_text_content(self):
        self.text_content = self.text_default
        self.text_content2 = self.text_default2
        self.text_content3 = self.text_default3
        self.text_content4 = self.text_default4

    def update(self, player, screen, *args):
        font_of_npc = args[0]
        system_mech = args[1]
        settings = args[2]

        if self.action:
            if self.action_on:
                if self.dialogue_create:
                    settings.world_status_changer("DIALOG")
                    self.dialogue = Dialogue()
                    system_mech.add(self.dialogue)
                    self.dialogue_create = False
                try:
                    for q in self.questions:
                        if q["index"] == self.text_index:
                            settings.world_status_changer("DIALOG_ANSWER")
                            if self.index_of_answers != q["answer_count"]:
                                for i in q["answer"]:
                                    if self.index_of_answers == 0:
                                        self.color2 = self.color_active
                                        self.text2 += i
                                    elif self.index_of_answers == 1:
                                        self.color3 = self.color_not_active
                                        self.text3 += i
                                    elif self.index_of_answers == 2:
                                        self.color4 = self.color_not_active
                                        self.text4 += i

                                    self.index_of_answers += 1

                    if self.letter_index != len(self.text_content[self.text_index]):
                        sans_sound.play()
                        self.text += self.text_content[self.text_index][self.letter_index]
                        self.letter_index += 1
                    else:
                        if self.letter_index2 != len(self.text_content2[self.text_index]):
                            sans_sound.play()
                            self.text2 += self.text_content2[self.text_index][self.letter_index2]
                            self.letter_index2 += 1
                        else:
                            if self.letter_index3 != len(self.text_content3[self.text_index]):
                                sans_sound.play()
                                self.text3 += self.text_content3[self.text_index][self.letter_index3]
                                self.letter_index3 += 1
                            else:
                                if self.letter_index4 != len(self.text_content4[self.text_index]):
                                    sans_sound.play()
                                    self.text4 += self.text_content4[self.text_index][self.letter_index4]
                                    self.letter_index4 += 1
                    text_surface = font_of_npc.render(self.text, True, self.color1)
                    text_surface2 = font_of_npc.render(self.text2, True, self.color2)
                    text_surface3 = font_of_npc.render(self.text3, True, self.color3)
                    text_surface4 = font_of_npc.render(self.text4, True, self.color4)
                    self.dialogue.text_set(text_surface, text_surface2, text_surface3, text_surface4)
                    if self.delay_text != 0:
                        self.delay_text -= 1
                        self.change = False
                except IndexError:
                    self.set_default_text_content()
                    self.dialogue.kill()
                    system_mech.remove(self.dialogue)
                    self.dialogue_create = True
                    self.action_on = False
                    self.text_index = 0

                    settings.world_status_changer("MAIN")
            if self.change:
                if settings.world_status == "DIALOG":
                    if self.text != self.text_content[self.text_index] and \
                            self.text2 != self.text_content2[self.text_index] and \
                            self.text3 != self.text_content3[self.text_index] and \
                            self.text4 != self.text_content4[self.text_index]:
                        self.letter_index = len(self.text_content[self.text_index])
                        self.letter_index2 = len(self.text_content2[self.text_index])
                        self.letter_index3 = len(self.text_content3[self.text_index])
                        self.letter_index4 = len(self.text_content4[self.text_index])
                        self.text = self.text_content[self.text_index]
                        self.text2 = self.text_content2[self.text_index]
                        self.text3 = self.text_content3[self.text_index]
                        self.text4 = self.text_content4[self.text_index]
                        self.change = False
            if self.change:
                if settings.world_status == "DIALOG":
                    self.delay_text = 5
                    self.text_index += 1
                    self.text = ""
                    self.text2 = ""
                    self.text3 = ""
                    self.text4 = ""
                    self.letter_index = 0
                    self.letter_index2 = 0
                    self.letter_index3 = 0
                    self.letter_index4 = 0
                    self.change = False

            if self.up_answer:
                if self.fps_answer_delay != 0:
                    self.fps_answer_delay -= 1
                else:
                    for q in self.questions:
                        if self.answer == 2:
                            if q["answer_count"] == 3:
                                self.answer = 4
                            elif q["answer_count"] == 2:
                                self.answer = 3
                            else:
                                self.answer = 2
                        elif self.answer == 3:
                            if q["answer_count"] == 3:
                                self.answer = 2
                            elif q["answer_count"] == 2:
                                self.answer = 2
                        elif self.answer == 4:
                            if q["answer_count"] == 3:
                                self.answer = 3

                        if self.answer == 2:
                            self.color2 = self.color_active
                            self.color3 = self.color_not_active
                            self.color4 = self.color_not_active
                        elif self.answer == 3:
                            self.color2 = self.color_not_active
                            self.color3 = self.color_active
                            self.color4 = self.color_not_active
                        elif self.answer == 4:
                            self.color2 = self.color_not_active
                            self.color3 = self.color_not_active
                            self.color4 = self.color_active
                    self.fps_answer_delay = 3
                    self.up_answer = False

            if self.down_answer:
                if self.fps_answer_delay != 0:
                    self.fps_answer_delay -= 1
                else:
                    for q in self.questions:
                        if self.answer == 2:
                            if q["answer_count"] == 3:
                                self.answer = 3
                            elif q["answer_count"] == 2:
                                self.answer = 3
                            else:
                                self.answer = 2
                        elif self.answer == 3:
                            if q["answer_count"] == 3:
                                self.answer = 4
                            elif q["answer_count"] == 2:
                                self.answer = 2
                        elif self.answer == 4:
                            if q["answer_count"] == 3:
                                self.answer = 2

                        if self.answer == 2:
                            self.color2 = self.color_active
                            self.color3 = self.color_not_active
                            self.color4 = self.color_not_active
                        elif self.answer == 3:
                            self.color2 = self.color_not_active
                            self.color3 = self.color_active
                            self.color4 = self.color_not_active
                        elif self.answer == 4:
                            self.color2 = self.color_not_active
                            self.color3 = self.color_not_active
                            self.color4 = self.color_active
                    self.fps_answer_delay = 3
                    self.down_answer = False

            if self.change_with_active:
                if self.fps_answer_delay != 0:
                    self.fps_answer_delay -= 1
                else:
                    for q in self.questions:
                        if self.answer == 2:
                            index_of_text_after = 1
                            for i in q["text_after"]:
                                text = i.split("/")
                                if len(text) == 1:
                                    self.text_content[self.text_index + index_of_text_after] = text[0]
                                elif len(text) == 2:
                                    self.text_content[self.text_index + index_of_text_after] = text[0]
                                    self.text_content2[self.text_index + index_of_text_after] = text[1]
                                elif len(text) == 3:
                                    self.text_content[self.text_index + index_of_text_after] = text[0]
                                    self.text_content2[self.text_index + index_of_text_after] = text[1]
                                    self.text_content3[self.text_index + index_of_text_after] = text[2]
                                elif len(text) == 4:
                                    self.text_content[self.text_index + index_of_text_after] = text[0]
                                    self.text_content2[self.text_index + index_of_text_after] = text[1]
                                    self.text_content3[self.text_index + index_of_text_after] = text[2]
                                    self.text_content4[self.text_index + index_of_text_after] = text[3]
                                index_of_text_after += 1
                        elif self.answer == 3:
                            index_of_text_after = 1
                            for i in q["text_after_2"]:
                                text = i.split("/")
                                if len(text) == 1:
                                    self.text_content[self.text_index + index_of_text_after] = text[0]
                                elif len(text) == 2:
                                    self.text_content[self.text_index + index_of_text_after] = text[0]
                                    self.text_content2[self.text_index + index_of_text_after] = text[1]
                                elif len(text) == 3:
                                    self.text_content[self.text_index + index_of_text_after] = text[0]
                                    self.text_content2[self.text_index + index_of_text_after] = text[1]
                                    self.text_content3[self.text_index + index_of_text_after] = text[2]
                                elif len(text) == 4:
                                    self.text_content[self.text_index + index_of_text_after] = text[0]
                                    self.text_content2[self.text_index + index_of_text_after] = text[1]
                                    self.text_content3[self.text_index + index_of_text_after] = text[2]
                                    self.text_content4[self.text_index + index_of_text_after] = text[3]
                                index_of_text_after += 1
                        elif self.answer == 4:
                            index_of_text_after = 1
                            for i in q["text_after_3"]:
                                text = i.split("/")
                                if len(text) == 1:
                                    self.text_content[self.text_index + index_of_text_after] = text[0]
                                elif len(text) == 2:
                                    self.text_content[self.text_index + index_of_text_after] = text[0]
                                    self.text_content2[self.text_index + index_of_text_after] = text[1]
                                elif len(text) == 3:
                                    self.text_content[self.text_index + index_of_text_after] = text[0]
                                    self.text_content2[self.text_index + index_of_text_after] = text[1]
                                    self.text_content3[self.text_index + index_of_text_after] = text[2]
                                elif len(text) == 4:
                                    self.text_content[self.text_index + index_of_text_after] = text[0]
                                    self.text_content2[self.text_index + index_of_text_after] = text[1]
                                    self.text_content3[self.text_index + index_of_text_after] = text[2]
                                    self.text_content4[self.text_index + index_of_text_after] = text[3]
                                index_of_text_after += 1

                    self.color2 = self.color1
                    self.color3 = self.color1
                    self.color4 = self.color1
                    self.fps_answer_delay = 5
                    self.change_with_active = False
                    self.index_of_answers = 0
                    settings.world_status_changer("DIALOG")

                    if settings.world_status == "DIALOG":
                        self.delay_text = 5
                        self.text_index += 1
                        self.text = ""
                        self.text2 = ""
                        self.text3 = ""
                        self.text4 = ""
                        self.letter_index = 0
                        self.letter_index2 = 0
                        self.letter_index3 = 0
                        self.letter_index4 = 0
                        self.change = False

            # checking, if dialogue is empty, kill him
            try:
                if self.text_content[self.text_index] == " " and self.text_content2[self.text_index] == " " and \
                        self.text_content3[self.text_index] == " " and self.text_content4[self.text_index] == " ":
                    self.delay_text = 5
                    self.text_index = 0
                    self.text = ""
                    self.text2 = ""
                    self.text3 = ""
                    self.text4 = ""
                    self.letter_index = 0
                    self.letter_index2 = 0
                    self.letter_index3 = 0
                    self.letter_index4 = 0
                    self.set_default_text_content()

                    self.dialogue.kill()
                    system_mech.remove(self.dialogue)
                    self.dialogue_create = True
                    self.action_on = False
                    self.text_index = 0
                    settings.world_status_changer("MAIN")
            except IndexError:
                pass
