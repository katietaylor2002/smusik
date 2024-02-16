from pathlib import Path
import random

import pygame


class Beat(pygame.sprite.Sprite):
    def __init__(self, first_beat):
        super(Beat, self).__init__()

        up_image = str(Path.cwd() / "pygame" / "images" / "up.jpg")
        down_image = str(Path.cwd() / "pygame" / "images" / "down.png")
        left_image = str(Path.cwd() / "pygame" / "images" / "left.jpg")
        right_image = str(Path.cwd() / "pygame" / "images" / "right.jpg")

        randomStart = random.choice([100, 300, 500, 700])

        if randomStart == 100:
            self.direction = "left"
            self.surf = pygame.image.load(left_image).convert_alpha()
        elif randomStart == 300:
            self.direction = "up"
            self.surf = pygame.image.load(up_image).convert_alpha()
        elif randomStart == 500:
            self.direction = "down"
            self.surf = pygame.image.load(down_image).convert_alpha()
        else:
            self.direction = "right"
            self.surf = pygame.image.load(right_image).convert_alpha()

        self.rect = self.surf.get_rect(
            center=(
                randomStart,
                150,
            )
        )

        self.first_beat = first_beat

    def move(self):
        self.rect.move_ip(0, 1)
        if self.rect.top < 0:
            self.kill()

    def trigger_playback(self):
        if self.first_beat:
            self.first_beat = False
            return True
