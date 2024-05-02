from pathlib import Path
import random

import pygame


class Beat(pygame.sprite.Sprite):
    def __init__(self, first_beat, start, confidence):
        super(Beat, self).__init__()

        up_image = str(Path.cwd() / "pygame" / "images" / "up.png")
        down_image = str(Path.cwd() / "pygame" / "images" / "down.png")
        left_image = str(Path.cwd() / "pygame" / "images" / "left.png")
        right_image = str(Path.cwd() / "pygame" / "images" / "right.png")

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
                100,
            )
        )

        self.first_beat = first_beat
        self.start = start
        self.confidence = confidence

    def move(self):
        self.rect.move_ip(0, 10)
        if self.rect.top < 0:
            self.kill()

    def trigger_playback(self):
        if self.first_beat and self.rect.top > 600:
            self.first_beat = False
            return True
        return False
