import pygame
from pygame.sprite import Sprite


class Text(Sprite):
    def __init__(self, location, message):
        super().__init__()
        font = pygame.font.Font(None, 50)
        self.image = font.render(message.name, 1, message.value)
        self.rect = self.image.get_rect()
        self.ticks = 1500 + pygame.time.get_ticks()
        self.column = location
        self.rect = (location, 50)

    def update(self, ticks):
        if ticks > self.ticks:
            self.kill()

    def column(self):
        return self.column()
