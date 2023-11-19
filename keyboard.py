
import pygame

class Keyboard:
    key_LMB = True

    @classmethod
    def update(cls):
        mouse_keys = pygame.mouse.get_pressed()

        cls.key_LMB = True

        if mouse_keys[0]:
            cls.key_LMB = False