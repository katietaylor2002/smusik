from pathlib import Path
from typing import Tuple

import pygame


class Player(pygame.sprite.Sprite):
    def __init__(self):
        """Initialize the player sprite"""
        super(Player, self).__init__()

        # Get the image to draw for the player
        player_image = str(
            Path.cwd() / "pygame" / "images" / "alien_green_stand.png"
        )
        # Load the image, preserve alpha channel for transparency
        self.surf = pygame.image.load(player_image).convert_alpha()
        # Save the rect so you can move it
        self.rect = self.surf.get_rect()

    def update(self, pos: Tuple):
        (x, _) = pos
        self.rect.center = (x, 450)
