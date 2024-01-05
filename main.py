import spotipy.util as util
import spotipy
import json
from types import SimpleNamespace
import pygame
from player import Player
from beat import Beat


def start_beat_game():

    # Initialising screen size
    WIDTH = 800
    HEIGHT = 1000
    beat_countdown = get_currently_listening()

    # Set up game
    pygame.init()
    screen = pygame.display.set_mode(size=[WIDTH, HEIGHT])
    pygame.mouse.set_visible(False)
    clock = pygame.time.Clock()

    # Set up the beat_list
    current_beat = 0
    ADD_BEAT = pygame.USEREVENT + 1
    pygame.time.set_timer(ADD_BEAT, int(beat_countdown[current_beat].duration * 1000))
    beat_list = pygame.sprite.Group()

    # Set up the player
    score = 0
    player = Player()
    player.update(pygame.mouse.get_pos())

    # Run until you get to an end condition
    running = True
    while running:

        for beat in beat_list:
            beat.move()

        # Did the user click the window close button?
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == ADD_BEAT:
                if beat_countdown[current_beat].confidence < confidence_threshold():
                    current_beat += 1
                else:
                    # Create a new beat
                    new_beat = Beat()
                    beat_list.add(new_beat)

                    # Stop the previous timer by setting the interval to 0
                    pygame.time.set_timer(ADD_BEAT, 0)

                    # Start a new timer
                    current_beat += 1
                    pygame.time.set_timer(ADD_BEAT, int(beat_countdown[current_beat].duration * 1000))

        # Update the player position
        player.update(pygame.mouse.get_pos())

        # Check if the player has collided with a beat, removing the beat if so
        beats_collected = pygame.sprite.spritecollide(
            sprite=player, group=beat_list, dokill=True
        )

        for beat in beats_collected:
            score += 10

        # To render the screen, first fill the background with pink
        screen.fill((255, 170, 164))
        pygame.draw.line(screen, (255, 0, 0), (0, 700), (800, 700), 2)

        # Draw the beats next
        for beat in beat_list:
            screen.blit(beat.surf, beat.rect)

        # Then draw the player
        screen.blit(player.surf, player.rect)

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

    # Make the mouse visible again
    pygame.mouse.set_visible(True)

    # Quit the game
    pygame.quit()


def get_average_track_confidence():
    pass

def confidence_threshold():
    return 0.5


def get_currently_listening():
    username = "katietaylor150"
    scope = "user-read-playback-state"
    redirect_uri = "http://localhost:8888/callback"
    CLIENT_ID = 'f188b8fd96304f02934c23370541b5fd'
    CLIENT_SECRET = 'afeb64fd90204bb29b63f3c7607a1924'

    token = util.prompt_for_user_token(username, scope, CLIENT_ID, CLIENT_SECRET, redirect_uri)
    sp = spotipy.Spotify(auth=token)

    analysis = json.dumps(sp.audio_analysis('4ThaT2zAl53ah6uxOdWUMs'))

    x = json.loads(analysis, object_hook=lambda d: SimpleNamespace(**d))

    return x.beats




if __name__ == '__main__':
    get_currently_listening()
    start_beat_game()
