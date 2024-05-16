import json
from types import SimpleNamespace

import pygame
from beat import Beat


class SmusicGame:
    def __init__(self, song, sp):
        self.song = song
        self.sp = sp
        self.track_analysis = self.get_track_analysis(song)

    def get_track_analysis(self, song):
        analysis = json.dumps(self.sp.audio_analysis(song))
        x = json.loads(analysis, object_hook=lambda d: SimpleNamespace(**d))
        return x.beats

    def start_beat_game(self):
        # Initialising screen size
        WIDTH = 800
        HEIGHT = 1000
        beat_countdown = self.track_analysis
        # Set up game
        pygame.init()
        screen = pygame.display.set_mode(size=[WIDTH, HEIGHT])
        pygame.mouse.set_visible(False)
        clock = pygame.time.Clock()

        # Set up the beat_list
        current_beat = 0
        ADD_BEAT = pygame.USEREVENT + 1
        beat_list = pygame.sprite.Group()
        first_beat = Beat(first_beat=True, start=0, confidence=1)
        beat_list.add(first_beat)
        pygame.time.set_timer(ADD_BEAT, int(beat_countdown[current_beat].duration * 1000))

        # Set up the player
        score = 0

        # Run until you get to an end condition
        running = True
        while running:

            for beat in beat_list:
                beat.move()
                if beat.trigger_playback():
                    self.sp.start_playback(uris=[self.song])

            # Did the user click the window close button?
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        for beat in beat_list:
                            if beat.direction == "left" and 600 < beat.rect.top < 700:
                                beat.kill()
                                score += 10
                    elif event.key == pygame.K_UP:
                        for beat in beat_list:
                            if beat.direction == "up" and 600 < beat.rect.top < 700:
                                beat.kill()
                                score += 10
                    elif event.key == pygame.K_DOWN:
                        for beat in beat_list:
                            if beat.direction == "down" and 600 < beat.rect.top < 700:
                                beat.kill()
                                score += 10
                    elif event.key == pygame.K_RIGHT:
                        for beat in beat_list:
                            if beat.direction == "right" and 600 < beat.rect.top < 700:
                                beat.kill()
                                score += 10
                elif event.type == ADD_BEAT:
                    # Create a new beat
                    new_beat = Beat(first_beat=False, start=beat_countdown[current_beat].start,
                                    confidence=beat_countdown[current_beat].confidence)
                    beat_list.add(new_beat)

                    # Stop the previous timer by setting the interval to 0
                    pygame.time.set_timer(ADD_BEAT, 0)

                    # Start a new timer
                    current_beat += 1
                    pygame.time.set_timer(ADD_BEAT, int(beat_countdown[current_beat].duration * 1000))

            # To render the screen, first fill the background
            screen.fill((36, 36, 36))

            # base line
            pygame.draw.line(screen, (47, 165, 114), (0, 700), (800, 700), 5)

            # vertical lines
            pygame.draw.line(screen, (47, 165, 114), (200, 0), (200, 1000), 2)
            pygame.draw.line(screen, (47, 165, 114), (400, 0), (400, 1000), 2)
            pygame.draw.line(screen, (47, 165, 114), (600, 0), (600, 1000), 2)

            # Draw the beats next
            for beat in beat_list:
                screen.blit(beat.surf, beat.rect)

            # Finally, draw the score at the bottom left
            score_font = pygame.font.SysFont("any_font", 36)
            score_block = score_font.render(f"Score: {score}", False, (47, 165, 114))
            screen.blit(score_block, (50, HEIGHT - 50))

            # Flip the display to make everything appear
            pygame.display.flip()

            # Ensure you maintain a 30 frames per second rate
            clock.tick(30)

        # Done! Print the final score
        print(f"Game over! Final score: {score}")

        self.sp.pause_playback()

        # Make the mouse visible again
        pygame.mouse.set_visible(True)

        # Quit the game
        pygame.quit()
