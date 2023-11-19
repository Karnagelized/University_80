
import os
import math
import random
import pygame
from config import HEIGHT, WIDTH


# Класс для воздушных шариков
class Balloon():
    def __init__(self):
        self.y = random.randint(HEIGHT, 2 * HEIGHT)
        self.add_x = random.randint(0, WIDTH)
        self.x = self.add_x + 20 * math.sin(0.1 * self.y)
        self.step = random.uniform(0.2, 0.7)
        self.image = random.choice([
            pygame.image.load(f'data/image/balloon/{image}') for image in os.listdir('data/image/balloon')
        ])


    # Изменение позиции объекта
    def update(self):
        self.y -= self.step
        self.x = self.add_x + 20 * math.sin(0.1 * self.y)


    # Отрисовка на экране объекта
    def draw(self):
        _surface = pygame.display.get_surface()
        _surface.blit(
            self.image,
            (self.x, self.y)
        )

        if self.y < -256:
            self.y = HEIGHT + 260