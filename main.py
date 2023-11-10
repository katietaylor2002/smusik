import spotipy.util as util
import spotipy

def getCurrentlyListening():
    username = "katietaylor150"
    scope = "user-read-playback-state"
    redirect_uri = "http://localhost:8888/callback"
    CLIENT_ID = 'f188b8fd96304f02934c23370541b5fd'
    CLIENT_SECRET = 'afeb64fd90204bb29b63f3c7607a1924'

    token = util.prompt_for_user_token(username, scope, CLIENT_ID, CLIENT_SECRET, redirect_uri)
    sp = spotipy.Spotify(auth=token)

    print(sp.audio_analysis('28Ymf40EoJ6776juQZNPoY'))

if __name__ == '__main__':
    getCurrentlyListening()
