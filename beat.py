from pathlib import Path
import random

import pygame


class Beat(pygame.sprite.Sprite):
    def __init__(self):
        super(Beat, self).__init__()

        beat_image = str(Path.cwd() / "pygame" / "images" / "coin_gold.png")

        self.surf = pygame.image.load(beat_image).convert_alpha()

        randomStart = random.choice([100, 300, 500, 700])
        self.rect = self.surf.get_rect(
            center=(
                randomStart,
                150,
            )
        )

    def move(self):
        self.rect.move_ip(0, 1)
        if self.rect.top < 0:
            self.kill()
