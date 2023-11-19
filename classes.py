
import asyncio
import sys
import pygame
import os
from config import HEIGHT, SIZE, FONT_LINK
from treiler import Trailer
from items import Balloon
from annotations import Annotations
from keyboard import Keyboard


# Класс UI приложения
class UI():
    def __init__(self):
        self.surface = pygame.display.get_surface()
        # Загрузка гимна
        self.is_play = False
        self.hymn = pygame.mixer.Sound('data/sound/hymn.mp3')
        self.hymn.set_volume(0.7)
        # Объект трейлера
        self.TRAILER = Trailer()
        # Объекты воздушных шаров
        self.balloons = [Balloon() for _ in range(30)]
        # Стадия показала начальной заставки
        self.select_window = 0
        # Чёрный фон для плавного затухания/появления
        self.b_background = pygame.image.load(f'data/image/black_background.png')
        # Число прозрачности фона от 0 до 255
        self.b_background_alpha = 0
        # Изображения для главного экрана
        self.background = pygame.image.load('data/image/background.jpg')
        self.u_logo = pygame.image.load('data/image/U_logo.png')
        # Фоны для главной страницы
        self.font_main = pygame.font.Font(FONT_LINK, 60)
        self.font_signature = pygame.font.Font(FONT_LINK, 20)
        self.font_hymn = pygame.font.Font(FONT_LINK, 25)
        # Создание объектов аннотаций
        self.annotations = Annotations.load_annotations()


    # Плавное появление/затухание экрана
    async def screen_appearance(self, step:int):
        self.b_background_alpha += step
        self.b_background.set_alpha(self.b_background_alpha)

        # Отрисовка картинки
        self.surface.blit(
            self.b_background,
            (0, 0)
        )


    # Показ главного UI приложения
    async def show_main_window(self):
        if not self.is_play:
            self.is_play = True
            self.hymn.play()

        # Отрисовка заднего фона
        self.surface.blit(
            self.background,
            (0, 0)
        )

        # Отрисовка логотипа ЮУрГУ
        self.surface.blit(
            self.u_logo,
            (150, 20)
        )

        # Отрисовка сообщения с поздравлением
        _congrats = self.font_main.render(
            'ЮУрГУ 80!',
            1,
            (255, 255, 255),
        )
        self.surface.blit(
            _congrats,
            (self.surface.get_width() // 2 - _congrats.get_width() // 2,
             self.surface.get_height() // 2 - _congrats.get_height() // 2 - 80)
        )

        # Отрисовка сообщения с цитатой
        _quote = self.font_main.render(
            'Инвестируйте  в  будущее!',
            1,
            (255, 255, 255),
        )
        self.surface.blit(
            _quote,
            (self.surface.get_width() // 2 - _quote.get_width() // 2,
             self.surface.get_height() // 2 - _quote.get_height() // 2 + 80)
        )

        # Отрисовка сообщения подписи цитаты
        _signature = self.font_signature.render(
            'Александр Шестаков',
            1,
            (255, 255, 255),
        )
        self.surface.blit(
            _signature,
            (self.surface.get_width() // 2 + _signature.get_width() // 2,
             self.surface.get_height() // 2 - _signature.get_height() // 2 + 120)
        )

        # Отрисовка аннотаций
        for annotation in self.annotations:
            annotation.draw()
            annotation.is_press()

        # Плавное появление
        if self.b_background_alpha > 1:
            await self.screen_appearance(-2)
            return

        # Отрисовка воздушных шаров
        for balloon in self.balloons:
            balloon.draw()
            balloon.update()


    # Основной блок отображения UI
    async def run(self):
        if self.select_window == 0:
            # Отображение трейлера
            if await self.TRAILER.show_trailer_window():
                self.select_window = 1
        elif self.select_window == 1:
            # Затухание окна
            await self.screen_appearance(2)

            # Выход из затухания экрана
            if self.b_background_alpha > 255:
                self.select_window = 2

            return
        elif self.select_window == 2:
            # Отображение главного окна приложения
            await self.show_main_window()


# Основной класс для обработки ивентов
class Program():
    def __init__(self):
        # Инициализация зависимостей PyGame
        pygame.init()
        pygame.display.set_caption('ЮУрГУ 80 лет!')
        self.icon = pygame.image.load('data/icon/icon.ico')
        pygame.display.set_icon(self.icon)
        pygame.mixer.init()
        pygame.font.init()

        # Установка действующего экрана
        self.screen = pygame.display.set_mode(SIZE, pygame.FULLSCREEN)
        # Инициализация часов
        self.clock = pygame.time.Clock()

        # Инициализация UI программы
        self.UI = UI()


    # Метод запуска программы
    async def run(self):
        while True:
            keys = pygame.key.get_pressed()

            for event in pygame.event.get():
                # Выход из программы
                if event.type == pygame.QUIT or keys[pygame.K_ESCAPE]:
                    await self.exit()

            # Обновляем UI экран
            await self.UI.run()

            # Обновляем статус кнопок
            Keyboard.update()

            # Применяем изменения экрана
            pygame.display.update()
            self.clock.tick(60)


    # Метод выхода из программы
    async def exit(self):
        pygame.quit()
        sys.exit()
