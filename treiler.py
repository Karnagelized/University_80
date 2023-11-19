
import os
import asyncio
import time

import pygame
from config import FONT_LINK
from keyboard import Keyboard


class Trailer():
    def __init__(self):
        self.surface = pygame.display.get_surface()
        # Фоновая музыка
        self.is_play = False
        self.background_music = pygame.mixer.Sound('data/sound/background.mp3')
        self.background_music.set_volume(0.7)
        # Чёрный фон для плавного затухания/появления
        self.b_background = pygame.image.load(f'data/image/black_background.png')
        # Число прозрачности фона от 0 до 255
        self.b_background_alpha = 0
        # Шрифты для трейлера
        self.font_trailer = pygame.font.Font(FONT_LINK, 60)
        self.font_recom = pygame.font.Font(FONT_LINK, 25)
        # Стадия начальной заставки
        self.state = 0

        # Изображения ЮУрГУ 1943 года
        self.image_1943 = [
            pygame.image.load(f'data/image/1943/{image}') for image in os.listdir('data/image/1943')
        ]

        # Изображения ЮУрГУ 1990 года
        self.image_1990 = [
            pygame.image.load(f'data/image/1990/{image}') for image in os.listdir('data/image/1990')
        ]

        # Изображения ЮУрГУ в настоящее время
        self.image_2023 = [
            pygame.image.load(f'data/image/2023/{image}') for image in os.listdir('data/image/2023')
        ]


    # Метод для очистки экрана
    async def clear_surface(self):
        self.surface.fill((0, 0, 0))


    # Вывод на экран рекомендаций
    async def view_recommendation(self):
        # Досрочный выход, если стадия больше 4-й
        if self.state > 4:
            return

        # Создания надписи
        _text = self.font_recom.render(
            'Рекомендуется  включить  звук',
            1,
            (100, 100, 100),
        )

        # Отрисовка надписи на экране
        self.surface.blit(
            _text,
            (self.surface.get_width() // 2 - _text.get_width() // 2,
             self.surface.get_height() - _text.get_height() - 20)
        )


    # Плавное появление/затухание экрана
    async def screen_appearance(self, step:int):
        self.b_background_alpha += step
        self.b_background.set_alpha(self.b_background_alpha)

        # Отрисовка картинки
        self.surface.blit(
            self.b_background,
            (0, 0)
        )


    # Метод проверки нажатия на текст
    async def is_press(self, text_yes:pygame.Surface):
        mouse_pos = pygame.mouse.get_pos()
        key_pressed = pygame.mouse.get_pressed()

        # Позиция текста без смещения
        _x = self.surface.get_width() // 2 - text_yes.get_width() // 2
        _y = self.surface.get_height() // 2 - text_yes.get_height() // 2 + 80

        if key_pressed[0] and Keyboard.key_LMB:
            # Левая и Правая кнопка
            if _x - 100 <= mouse_pos[0] <= _x - 100 + text_yes.get_width() or\
                _x + 100 <= mouse_pos[0] <= _x + 100 + text_yes.get_width():
                if _y <= mouse_pos[1] <= _y + text_yes.get_height():
                    return True


    # Метод показала трейлера
    async def show_trailer_window(self):
        # Прошедшее время после запуска программы в секундах
        ticks = pygame.time.get_ticks() / 1000

        # Отображение рекомендации по включению звука
        await self.view_recommendation()

        # Отображение UI по стадиям
        if self.state == 0 and ticks > 1:
            # Смена стадии
            self.state = 1

            # Проигрывание музыки
            if not self.is_play:
                self.is_play = True
                self.background_music.play()


            # Создания надписи
            _text = self.font_trailer.render(
                'Этому  городу  нужен  новый  Герой',
                1,
                (255, 255, 255),
            )

            # Отрисовка надписи на экране
            self.surface.blit(
                _text,
                (self.surface.get_width() // 2 - _text.get_width() // 2,
                self.surface.get_height() // 2)
            )
        elif self.state == 1 and ticks > 4.5:
            # Смена стадии
            self.state = 2

            # Очистка экрана
            await self.clear_surface()

            # Создания надписи
            _text = self.font_trailer.render(
                'Лучший  Университет  мира',
                1,
                (255, 255, 255),
            )

            # Отрисовка надписи на экране
            self.surface.blit(
                _text,
                (self.surface.get_width() // 2 - _text.get_width() // 2,
                self.surface.get_height() // 2)
            )
        elif self.state == 2 and ticks > 7.8:
            # Очистка экрана
            await self.clear_surface()

            # Создания надписи
            _text_first = self.font_trailer.render(
                'ЮУрГУ',
                1,
                (255, 255, 255),
            )

            _text_second = self.font_trailer.render(
                'Исполняется  80  лет',
                1,
                (255, 255, 255),
            )

            # Отрисовка первой надписи на экране
            self.surface.blit(
                _text_first,
                (self.surface.get_width() // 2 - _text_first.get_width() // 2,
                 self.surface.get_height() // 2 - 60),
            )

            # Отрисовка второй надписи на экране
            if ticks > 7.9:
                # Смена стадии
                self.state = 3

                self.surface.blit(
                    _text_second,
                    (self.surface.get_width() // 2 - _text_second.get_width() // 2,
                     self.surface.get_height() // 2 + 60),
                )
        elif self.state == 3 and ticks > 14.8:
            # Смена стадии
            self.state = 4

            # Очистка экрана
            await self.clear_surface()

            # Создания надписи
            _text = self.font_trailer.render(
                'Это  не  всё',
                1,
                (255, 255, 255),
            )

            # Отрисовка надписи на экране
            self.surface.blit(
                _text,
                (self.surface.get_width() // 2 - _text.get_width() // 2,
                 self.surface.get_height() // 2)
            )
        elif self.state == 4 and ticks > 21.5:
            # Смена стадии
            self.state = 5

            # Очистка экрана
            await self.clear_surface()

            # Создания надписи
            _text = self.font_trailer.render(
                'Мы  гордимся  ЮУрГУ',
                1,
                (255, 255, 255),
            )

            # Отрисовка надписи на экране
            self.surface.blit(
                _text,
                (self.surface.get_width() // 2 - _text.get_width() // 2,
                 self.surface.get_height() // 2)
            )
        elif self.state == 5 and ticks > 28.5:
            # Очистка экрана
            await self.clear_surface()

            # Создания надписи
            _text = self.font_trailer.render(
                'Полёт  в  историю',
                1,
                (255, 255, 255),
            )

            _text_year = self.font_trailer.render(
                '1943',
                1,
                (255, 255, 255),
            )

            # Отрисовка надписи на экране
            self.surface.blit(
                _text,
                (self.surface.get_width() // 2 - _text.get_width() // 2,
                 _text.get_height() + 20)
            )

            # Отрисовка года на экране
            if ticks > 29:
                # Смена стадии
                self.state = 6

                self.surface.blit(
                    _text_year,
                    (self.surface.get_width() // 2 - _text_year.get_width() // 2,
                     _text_year.get_height() * 2 + 60)
                )
        elif self.state == 6 and ticks > 29.5:
            # Отрисовка картинки
            self.surface.blit(
                self.image_1943[0],
                (self.image_1943[0].get_width() - 40,
                 self.surface.get_height() // 2 - 100)
            )

            if ticks > 32:
                # Отрисовка картинки
                self.surface.blit(
                    self.image_1943[1],
                    (self.image_1943[1].get_width() * 2 + 80,
                     self.surface.get_height() // 2 - 100)
                )

            if ticks > 34:
                # Отрисовка картинки
                self.surface.blit(
                    self.image_1943[2],
                    (self.image_1943[2].get_width() * 3 + 120,
                     self.surface.get_height() // 2 - 100)
                )

            if ticks > 36:
                # Отрисовка картинки
                self.surface.blit(
                    self.image_1943[3],
                    (self.image_1943[3].get_width() * 1.5 + 40,
                     self.surface.get_height() // 2 + 200)
                )

            if ticks > 38:
                # Отрисовка картинки
                self.surface.blit(
                    self.image_1943[4],
                    (self.image_1943[4].get_width() * 2.5 + 80,
                     self.surface.get_height() // 2 + 200)
                )

            # Смена стадии
            if ticks > 41:
                self.state = 7
        elif self.state == 7 and ticks > 42:
            # Очистка экрана
            await self.clear_surface()

            # Создания надписи
            _text = self.font_trailer.render(
                'Полёт  в  историю',
                1,
                (255, 255, 255),
            )

            _text_year = self.font_trailer.render(
                '1990',
                1,
                (255, 255, 255),
            )

            # Отрисовка надписи на экране
            self.surface.blit(
                _text,
                (self.surface.get_width() // 2 - _text.get_width() // 2,
                 _text.get_height() + 20)
            )

            # Отрисовка года на экране
            if ticks > 42.5:
                # Смена стадии
                self.state = 8

                self.surface.blit(
                    _text_year,
                    (self.surface.get_width() // 2 - _text_year.get_width() // 2,
                     _text_year.get_height() * 2 + 60)
                )
        elif self.state == 8 and ticks > 43:
            # Отрисовка картинки
            self.surface.blit(
                self.image_1990[0],
                (self.image_1990[0].get_width() - 160,
                 self.surface.get_height() // 2 - 100)
            )

            if ticks > 45:
                # Отрисовка картинки
                self.surface.blit(
                    self.image_1990[1],
                    (self.image_1990[1].get_width() * 2 + 20,
                     self.surface.get_height() // 2 - 100)
                )

            if ticks > 47:
                # Отрисовка картинки
                self.surface.blit(
                    self.image_1990[2],
                    (self.image_1990[2].get_width() * 3 + 160,
                     self.surface.get_height() // 2 - 100)
                )

            if ticks > 49:
                # Отрисовка картинки
                self.surface.blit(
                    self.image_1990[3],
                    (self.image_1990[3].get_width() * 1.5,
                     self.surface.get_height() // 2 + 200)
                )

            if ticks > 51:
                # Отрисовка картинки
                self.surface.blit(
                    self.image_1990[4],
                    (self.image_1990[4].get_width() * 2.5 + 80,
                     self.surface.get_height() // 2 + 200)
                )

            # Смена стадии
            if ticks > 54:
                self.state = 9
        elif self.state == 9 and ticks > 56:
            # Очистка экрана
            await self.clear_surface()

            # Создания надписи
            _text = self.font_trailer.render(
                'Полёт  в  историю',
                1,
                (255, 255, 255),
            )

            _text_year = self.font_trailer.render(
                'Вперёд  в  настоящее',
                1,
                (255, 255, 255),
            )

            # Отрисовка надписи на экране
            self.surface.blit(
                _text,
                (self.surface.get_width() // 2 - _text.get_width() // 2,
                 _text.get_height() + 20)
            )

            # Отрисовка года на экране
            if ticks > 56.5:
                # Смена стадии
                self.state = 10

                self.surface.blit(
                    _text_year,
                    (self.surface.get_width() // 2 - _text_year.get_width() // 2,
                     _text_year.get_height() * 2 + 60)
                )
        elif self.state == 10 and ticks > 58:
            # Смена стадии
            self.state = 11

            # Закрашивание старой области
            self.surface.blit(
                pygame.surface.Surface((1920, 900)),
                (0, 270)
            )

            # Отрисовка картинки
            self.surface.blit(
                self.image_2023[0],
                (self.surface.get_width() // 2 - self.image_2023[0].get_width() // 2,
                100 + self.surface.get_height() // 2 - self.image_2023[0].get_height() // 2)
            )
        elif self.state == 11 and ticks > 60:
            # Смена стадии
            self.state = 12

            # Закрашивание старой области
            self.surface.blit(
                pygame.surface.Surface((1920, 900)),
                (0, 270)
            )

            # Отрисовка картинки
            self.surface.blit(
                self.image_2023[1],
                (self.surface.get_width() // 2 - self.image_2023[1].get_width() // 2,
                 100 + self.surface.get_height() // 2 - self.image_2023[1].get_height() // 2)
            )
        elif self.state == 12 and ticks > 62:
            # Смена стадии
            self.state = 13

            # Закрашивание старой области
            self.surface.blit(
                pygame.surface.Surface((1920, 900)),
                (0, 270)
            )

            # Отрисовка картинки
            self.surface.blit(
                self.image_2023[2],
                (self.surface.get_width() // 2 - self.image_2023[2].get_width() // 2,
                 100 + self.surface.get_height() // 2 - self.image_2023[2].get_height() // 2)
            )
        elif self.state == 13 and ticks > 64:
            # Смена стадии
            self.state = 14

            # Закрашивание старой области
            self.surface.blit(
                pygame.surface.Surface((1920, 900)),
                (0, 270)
            )

            # Отрисовка картинки
            self.surface.blit(
                self.image_2023[3],
                (self.surface.get_width() // 2 - self.image_2023[3].get_width() // 2,
                 100 + self.surface.get_height() // 2 - self.image_2023[3].get_height() // 2)
            )
        elif self.state == 14 and ticks > 66:
            # Смена стадии
            self.state = 15

            # Закрашивание старой области
            self.surface.blit(
                pygame.surface.Surface((1920, 900)),
                (0, 270)
            )

            # Отрисовка картинки
            self.surface.blit(
                self.image_2023[4],
                (self.surface.get_width() // 2 - self.image_2023[4].get_width() // 2,
                 100 + self.surface.get_height() // 2 - self.image_2023[4].get_height() // 2)
            )
        elif self.state == 15 and ticks > 68:
            # Смена стадии
            self.state = 16

            # Закрашивание старой области
            self.surface.blit(
                pygame.surface.Surface((1920, 900)),
                (0, 270)
            )

            # Отрисовка картинки
            self.surface.blit(
                self.image_2023[5],
                (self.surface.get_width() // 2 - self.image_2023[5].get_width() // 2,
                 100 + self.surface.get_height() // 2 - self.image_2023[5].get_height() // 2)
            )
        elif self.state == 16 and ticks > 70:
            # Смена стадии
            self.state = 17

            # Закрашивание старой области
            self.surface.blit(
                pygame.surface.Surface((1920, 900)),
                (0, 270)
            )

            # Отрисовка картинки
            self.surface.blit(
                self.image_2023[6],
                (self.surface.get_width() // 2 - self.image_2023[6].get_width() // 2,
                 100 + self.surface.get_height() // 2 - self.image_2023[6].get_height() // 2)
            )
        elif self.state == 17 and ticks > 72:
            # Смена стадии
            self.state = 18

            # Закрашивание старой области
            self.surface.blit(
                pygame.surface.Surface((1920, 900)),
                (0, 270)
            )

            # Отрисовка картинки
            self.surface.blit(
                self.image_2023[7],
                (self.surface.get_width() // 2 - self.image_2023[7].get_width() // 2,
                 100 + self.surface.get_height() // 2 - self.image_2023[7].get_height() // 2)
            )
        elif self.state == 18 and ticks > 74:
            # Смена стадии
            self.state = 19

            # Закрашивание старой области
            self.surface.blit(
                pygame.surface.Surface((1920, 900)),
                (0, 270)
            )

            # Отрисовка картинки
            self.surface.blit(
                self.image_2023[8],
                (self.surface.get_width() // 2 - self.image_2023[8].get_width() // 2,
                 100 + self.surface.get_height() // 2 - self.image_2023[8].get_height() // 2)
            )
        elif self.state == 19 and ticks > 76:
            # Смена стадии
            self.state = 20

            # Закрашивание старой области
            self.surface.blit(
                pygame.surface.Surface((1920, 900)),
                (0, 270)
            )

            # Отрисовка картинки
            self.surface.blit(
                self.image_2023[9],
                (self.surface.get_width() // 2 - self.image_2023[9].get_width() // 2,
                 100 + self.surface.get_height() // 2 - self.image_2023[9].get_height() // 2)
            )
        elif self.state == 20 and ticks > 78:
            # Смена стадии
            self.state = 21

            # Закрашивание старой области
            self.surface.blit(
                pygame.surface.Surface((1920, 900)),
                (0, 270)
            )

            # Отрисовка картинки
            self.surface.blit(
                self.image_2023[10],
                (self.surface.get_width() // 2 - self.image_2023[10].get_width() // 2,
                 100 + self.surface.get_height() // 2 - self.image_2023[10].get_height() // 2)
            )
        elif self.state == 21 and ticks > 81:
            # Смена стадии
            self.state = 22

            # Затухание музыки
            self.background_music.fadeout(2000)
        elif self.state == 22:
            await self.screen_appearance(2)

            # Смена стадии
            if self.b_background_alpha > 255:
                self.state = 23
                self.b_background_alpha = 0
        elif self.state == 23:
            # Создания надписи
            _text = self.font_trailer.render(
                'Продолжить?',
                1,
                (255, 255, 255),
            )

            _text_yes = self.font_trailer.render(
                'Да',
                1,
                (255, 255, 255),
            )

            # Отрисовка надписи на экране
            self.surface.blit(
                _text,
                (self.surface.get_width() // 2 - _text.get_width() // 2,
                 self.surface.get_height() // 2 - _text.get_height() // 2 - 80)
            )

            # Отрисовка надписи на экране
            self.surface.blits(
                [
                    (_text_yes,
                    (self.surface.get_width() // 2 - _text_yes.get_width() // 2 - 100,
                    self.surface.get_height() // 2 - _text_yes.get_height() // 2 + 80)),
                    (_text_yes,
                    (self.surface.get_width() // 2 - _text_yes.get_width() // 2 + 100,
                     self.surface.get_height() // 2 - _text_yes.get_height() // 2 + 80)),
                ]
            )

            # Проверка на нажатие кнопки
            return await self.is_press(_text_yes)