from tkinter import *
import spotipy.util as util
import spotipy


class Search:

    def __init__(self):
        self.sp = self.create_spotify_connection()
        self.search_screen()

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

    def search_for_song(self, T, Output):
        song = T.get("1.0", "end-1c")
        search = self.sp.search(song, 5)
        songs = []
        for song in search["tracks"]["items"]:
            Output.insert(END, song["name"] + " by " + song["artists"][0]["name"])
            songs.append(song["uri"])

    # def get_track_analysis(self):
    #     analysis = json.dumps(self.sp.audio_analysis(self.songs[self.song_choice]))
    #     x = json.loads(analysis, object_hook=lambda d: SimpleNamespace(**d))
    #     return x.beats
    #
    # def start_song_playback(self):
    #     self.sp.start_playback(uris=self.songs,
    #                            offset={"position": self.song_choice})
    #     # note if playback doesn't work play a song manually first

    def search_screen(self):
        window = Tk()
        greeting = Label(text="Smusik")
        greeting.pack()
        T = Text(window, height=5, width=52)
        T.pack()
        b1 = Button(window, text="Search", command=lambda: self.search_for_song(T, Output))
        b1.pack()
        Output = Text(window, height=5,
                         width=25,
                         bg="light cyan")
        Output.pack()
        song1Button = Button(window, text="Song 1", command=lambda:)
        song2Button = Button(window, text="Song 2", command=lambda:)
        song3Button = Button(window, text="Song 3", command=lambda:)
        song4Button = Button(window, text="Song 4", command=lambda:)
        song5Button = Button(window, text="Song 5", command=lambda:)
        song1Button.pack()
        song2Button.pack()
        song3Button.pack()
        song4Button.pack()
        song5Button.pack()
        window.geometry("800x1000")
        window.mainloop()
