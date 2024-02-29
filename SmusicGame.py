import time
from timer import Timer

import spotipy.util as util
import spotipy
import json
from types import SimpleNamespace

import pygame
from beat import Beat


class SmusicGame:
    def __init__(self):
        self.sp = self.create_spotify_connection()
        self.songs = self.search_for_song()
        self.song_choice = self.get_song_choice()

    @staticmethod
    def create_spotify_connection():
        username = "katietaylor150"
        scope = "user-modify-playback-state user-read-playback-state streaming"
        redirect_uri = "http://localhost:8888/callback"
        CLIENT_ID = 'f188b8fd96304f02934c23370541b5fd'
        CLIENT_SECRET = 'afeb64fd90204bb29b63f3c7607a1924'

        token = util.prompt_for_user_token(username, scope, CLIENT_ID, CLIENT_SECRET, redirect_uri)
        return spotipy.Spotify(auth=token)

    @staticmethod
    def get_song_choice():
        print("select song")
        return int(input())

    def search_for_song(self):
        print("enter a song to play")
        song = input()
        search = self.sp.search(song, 5)
        songs = []
        for song in search["tracks"]["items"]:
            print(song["name"] + " by " + song["artists"][0]["name"])
            songs.append(song["uri"])
        return songs

    def get_track_analysis(self):
        analysis = json.dumps(self.sp.audio_analysis(self.songs[self.song_choice]))
        x = json.loads(analysis, object_hook=lambda d: SimpleNamespace(**d))
        return x.beats

    def start_song_playback(self):
        self.sp.start_playback(uris=self.songs,
                               offset={"position": self.song_choice})
        # note if playback doesn't work play a song manually first

    def start_beat_game(self):
        # Initialising screen size
        WIDTH = 800
        HEIGHT = 1000
        beat_countdown = self.get_track_analysis()
        self.sp.pause_playback()

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
        t = Timer()

        # Run until you get to an end condition
        running = True
        while running:

            for beat in beat_list:
                beat.move()
                if beat.trigger_playback():
                    print("yes")
                    self.start_song_playback()
                    t.start()


            # Did the user click the window close button?
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        for beat in beat_list:
                            if beat.direction == "left" and 600 < beat.rect.top < 700:
                                print(beat.start + "at time" + t.stop)
                                beat.kill()
                                score += 10
                    elif event.key == pygame.K_UP:
                        for beat in beat_list:
                            if beat.direction == "up" and 600 < beat.rect.top < 700:
                                print(beat.start + "at time" + time.time())
                                beat.kill()
                                score += 10
                    elif event.key == pygame.K_DOWN:
                        for beat in beat_list:
                            if beat.direction == "down" and 600 < beat.rect.top < 700:
                                print(beat.start + "at time" + time.time())
                                beat.kill()
                                score += 10
                    elif event.key == pygame.K_RIGHT:
                        for beat in beat_list:
                            if beat.direction == "right" and 600 < beat.rect.top < 700:
                                print(beat.start + "at time" + time.time())
                                beat.kill()
                                score += 10
                elif event.type == ADD_BEAT:
                    if beat_countdown[current_beat].confidence < 0:
                        current_beat += 1
                    else:
                        # Create a new beat
                        new_beat = Beat(first_beat=False, start=beat_countdown[current_beat].start,
                                        confidence=beat_countdown[current_beat].confidence)
                        beat_list.add(new_beat)

                        # Stop the previous timer by setting the interval to 0
                        pygame.time.set_timer(ADD_BEAT, 0)

                        # Start a new timer
                        current_beat += 1
                        pygame.time.set_timer(ADD_BEAT, int(beat_countdown[current_beat].duration * 1000))

            # To render the screen, first fill the background with pink
            screen.fill((255, 170, 164))

            # base line
            pygame.draw.line(screen, (255, 0, 0), (0, 700), (800, 700), 2)

            # vertical lines
            pygame.draw.line(screen, (255, 0, 0), (200, 0), (200, 1000), 2)
            pygame.draw.line(screen, (255, 0, 0), (400, 0), (400, 1000), 2)
            pygame.draw.line(screen, (255, 0, 0), (600, 0), (600, 1000), 2)

            # Draw the beats next
            for beat in beat_list:
                screen.blit(beat.surf, beat.rect)

            # Finally, draw the score at the bottom left
            score_font = pygame.font.SysFont("any_font", 36)
            score_block = score_font.render(f"Score: {score}", False, (0, 0, 0))
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
