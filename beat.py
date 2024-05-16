from pathlib import Path
import random

import pygame
from directions import Direction
from text import Text


class Beat(pygame.sprite.Sprite):
    def __init__(self, first_beat, start, confidence):
        super(Beat, self).__init__()

        up_image = str(Path.cwd() / "pygame" / "images" / "greenup.png")
        down_image = str(Path.cwd() / "pygame" / "images" / "greendown.png")
        left_image = str(Path.cwd() / "pygame" / "images" / "greenleft.png")
        right_image = str(Path.cwd() / "pygame" / "images" / "greenright.png")

        randomStart = random.choice([Direction.LEFT.value, Direction.UP.value,
                                     Direction.DOWN.value, Direction.RIGHT.value])

        if randomStart == Direction.LEFT.value:
            self.direction = Direction.LEFT
            self.surf = pygame.image.load(left_image).convert_alpha()

        elif randomStart == Direction.UP.value:
            self.direction = Direction.UP
            self.surf = pygame.image.load(up_image).convert_alpha()

        elif randomStart == Direction.DOWN.value:
            self.direction = Direction.DOWN
            self.surf = pygame.image.load(down_image).convert_alpha()

        else:
            self.direction = Direction.RIGHT
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
        self.rect.move_ip(0, 12)
        if self.rect.top < 0:
            self.kill()

    def trigger_playback(self):
        if self.first_beat and self.rect.top > 600:
            self.first_beat = False
            return True
        return False
