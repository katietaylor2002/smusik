from pathlib import Path
import random

from pygame.sprite import Sprite

import pygame
from directions import Direction


class Beat(Sprite):
    def __init__(self, first_beat, start, speed):
        super(Beat, self).__init__()

        up_image = str(Path.cwd() / "pygame" / "images" / "greenup.png")
        down_image = str(Path.cwd() / "pygame" / "images" / "greendown.png")
        left_image = str(Path.cwd() / "pygame" / "images" / "greenleft.png")
        right_image = str(Path.cwd() / "pygame" / "images" / "greenright.png")

        randomStart = random.choice([Direction.LEFT.value, Direction.UP.value,
                                     Direction.DOWN.value, Direction.RIGHT.value])

        match randomStart:
            case Direction.LEFT.value:
                self.direction = Direction.LEFT
                self.surf = pygame.image.load(left_image).convert_alpha()

            case Direction.UP.value:
                self.direction = Direction.UP
                self.surf = pygame.image.load(up_image).convert_alpha()

            case Direction.DOWN.value:
                self.direction = Direction.DOWN
                self.surf = pygame.image.load(down_image).convert_alpha()

            case Direction.RIGHT.value:
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
        self.speed = speed

    def move_and_get_location(self):
        self.rect.move_ip(0, self.speed)
        return self.rect.top

    def trigger_playback(self):
        if self.first_beat and self.rect.top > 600:
            self.first_beat = False
            return True
        return False
