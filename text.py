import pygame
from pygame.sprite import Sprite


class Text(Sprite):
    def __init__(self, font, text, color, ticks, column):
        super().__init__()
        self.image = font.render(text, 1, color)
        self.rect = self.image.get_rect()
        self.ticks = ticks + pygame.time.get_ticks()
        self.column = column
        self.rect = (column, 50)

    def update(self, ticks):
        if ticks > self.ticks:
            self.kill()

    def column(self):
        return self.column()