
import pygame
import webbrowser
from config import LINKS, HEIGHT
from keyboard import Keyboard

class Annotations():
    def __init__(self, x:int, y:int, type:str):
        self.surface = pygame.display.get_surface()
        self.x = x
        self.y = y
        self.image = LINKS[type]['image']
        self.link = LINKS[type]['link']


    # Статический метод загрузки аннотаций
    @staticmethod
    def load_annotations():
        return [Annotations(iter * 20 + (iter - 1) * 48, HEIGHT - 68, key)
                for iter, key in enumerate(LINKS, start=1)]


    # Отрисовка аннотаций
    def draw(self):
        self.surface.blit(
            self.image,
            (self.x, self.y)
        )


    # Проверка на нажатие аннотации
    def is_press(self):
        mouse_pos = pygame.mouse.get_pos()
        key_pressed = pygame.mouse.get_pressed()

        if key_pressed[0] and Keyboard.key_LMB:
            if self.x <= mouse_pos[0] <= self.x + self.image.get_width():
                if self.y <= mouse_pos[1] <= self.y + self.image.get_height():
                    webbrowser.open(self.link)