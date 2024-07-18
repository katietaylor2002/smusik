import json
from types import SimpleNamespace

from pygame.sprite import Group

import pygame
from beat import Beat
from directions import Direction
from messages import Messages
from scoreboard import ScoreBoard
from text import Text


class Game:
    def __init__(self, song, sp, mode):
        pygame.init()

        self.song = song
        self.sp = sp
        self.score = 0
        self.misses = 0
        self.okays = 0
        self.greats = 0
        self.texts = Group()
        self.beat_list = Group()
        self.mode = mode

        self.track_analysis = self.get_track_analysis(song)
        self.start_beat_game()

    def get_track_analysis(self, song):
        analysis = json.dumps(self.sp.audio_analysis(song))
        x = json.loads(analysis, object_hook=lambda d: SimpleNamespace(**d))
        return x.beats

    def add_text_to_screen(self, text_location, message):
        for text in self.texts:
            if text.column == text_location:
                text.kill()
        self.texts.add(Text(text_location, message))

    def process_input(self, direction):
        text_location = direction.value - 45

        for beat in self.beat_list:
            if beat.direction == direction and 625 < beat.rect.top < 675:
                beat.kill()
                self.score += 10
                self.greats += 1
                self.add_text_to_screen(text_location, Messages.GREAT)
                break

            elif beat.direction == direction and 550 < beat.rect.top < 750:
                beat.kill()
                self.score += 5
                self.okays += 1
                self.add_text_to_screen(text_location, Messages.OKAY)
                break

            else:
                self.score -= 5
                self.misses += 1
                self.add_text_to_screen(text_location, Messages.MISS)

    def get_confidence(self):
        if self.mode == 0:
            return 0.4
        elif self.mode == 1:
            return 0.3
        else:
            return 0

    def get_speed(self):
        if self.mode == 0:
            return 12
        elif self.mode == 1:
            return 15
        else:
            return 18

    def start_beat_game(self):
        WIDTH = 800
        HEIGHT = 1000

        bg = pygame.image.load("when-dizzie.jpg")
        screen = pygame.display.set_mode(size=[WIDTH, HEIGHT])
        pygame.mouse.set_visible(False)
        clock = pygame.time.Clock()

        current_beat = 0
        ADD_BEAT = pygame.USEREVENT + 1
        first_beat = Beat(first_beat=True, start=0, speed=self.get_speed())
        self.beat_list.add(first_beat)
        pygame.time.set_timer(ADD_BEAT, int(self.track_analysis[current_beat].duration * 1000))

        running = True
        while running:

            for beat in self.beat_list:
                if beat.trigger_playback():
                    self.sp.start_playback(uris=[self.song])

                if beat.move_and_get_location() > 800:
                    beat.kill()
                    self.score -= 5
                    self.misses += 1
                    self.add_text_to_screen(beat.direction.value-45, Messages.MISS)
                    break

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False
                    elif event.key == pygame.K_LEFT:
                        self.process_input(Direction.LEFT)
                    elif event.key == pygame.K_UP:
                        self.process_input(Direction.UP)
                    elif event.key == pygame.K_DOWN:
                        self.process_input(Direction.DOWN)
                    elif event.key == pygame.K_RIGHT:
                        self.process_input(Direction.RIGHT)

                elif event.type == ADD_BEAT:
                    if self.track_analysis[current_beat].confidence >= self.get_confidence():
                        new_beat = Beat(first_beat=False, start=self.track_analysis[current_beat].start,
                                        speed=self.get_speed())
                        self.beat_list.add(new_beat)
                    pygame.time.set_timer(ADD_BEAT, 0)
                    current_beat += 1
                    pygame.time.set_timer(ADD_BEAT, int(self.track_analysis[current_beat].duration * 1000))

            # To render the screen, first fill the background
            if self.mode == 2:
                screen.blit(bg, (0, 0))
            else:
                screen.fill((36, 36, 36))

            pygame.draw.line(screen, (16, 106, 67), (0, 700), (800, 700), 15)
            pygame.draw.line(screen, (47, 165, 114), (0, 600), (800, 600), 2)
            pygame.draw.line(screen, (47, 165, 114), (0, 800), (800, 800), 2)
            pygame.draw.line(screen, (47, 165, 114), (200, 0), (200, 1000), 2)
            pygame.draw.line(screen, (47, 165, 114), (400, 0), (400, 1000), 2)
            pygame.draw.line(screen, (47, 165, 114), (600, 0), (600, 1000), 2)

            for beat in self.beat_list:
                screen.blit(beat.surf, beat.rect)

            score_font = pygame.font.SysFont("any_font", 36)
            score_block = score_font.render(f"Score: {self.score}", False, (47, 165, 114))
            screen.blit(score_block, (50, 950))

            ticks = pygame.time.get_ticks()
            self.texts.update(ticks)
            self.texts.draw(screen)

            pygame.display.flip()

            clock.tick(30)

        print(f"Game over! Final score: {self.score}")

        self.sp.pause_playback()

        pygame.mouse.set_visible(True)

        pygame.quit()
        ScoreBoard(self.score, self.greats, self.okays, self.misses)
