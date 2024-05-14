import io
import urllib.request
from tkinter import *
import customtkinter
from PIL import Image

import spotipy.util as util
import spotipy

from SmusicGame import SmusicGame


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

    def create_song_button(self, window, song_number, search_results):
        current_song = search_results["tracks"]["items"][song_number]

        with urllib.request.urlopen(current_song["album"]["images"][0]["url"]) as u:
            raw_data = u.read()

        image = customtkinter.CTkImage(light_image=Image.open(io.BytesIO(raw_data)),
                                       dark_image=Image.open(io.BytesIO(raw_data)),
                                       size=(180, 180))

        button = customtkinter.CTkButton(window, text=current_song["name"].strip() + " by " + current_song["artists"][0]["name"].strip(),
                                         font=("Impact", 40),
                                         image=image,
                                         height=50,
                                         width=700,
                                         anchor='w',
                                         command=lambda: self.start_game(current_song["uri"], window))

        button._text_label.configure(wraplength=500)
        button.pack(pady=30)

    def search_for_song(self, search_textbox, window):
        song = search_textbox.get("1.0", "end-1c")
        search = self.sp.search(song, 3)
        for i in range(0, 3):
            self.create_song_button(window, i, search)

    def start_game(self, song, window):
        window.destroy()
        new_game = SmusicGame(song, self.sp)
        new_game.start_beat_game()

    def search_screen(self):
        customtkinter.set_appearance_mode("dark")
        customtkinter.set_default_color_theme("green")
        window = customtkinter.CTk()
        window.geometry("800x1000")
        window.title("smusic")

        my_image = customtkinter.CTkImage(light_image=Image.open("pygame/images/logo.png"),
                                          dark_image=Image.open("pygame/images/logo.png"),
                                          size=(238, 116))

        heading = customtkinter.CTkLabel(window, text="", image=my_image)
        search_textbox = customtkinter.CTkTextbox(window, height=50, width=400, font=("Impact", 40))
        search_button = customtkinter.CTkButton(window, text="search", font=("Impact", 40),
                                                command=lambda: [self.search_for_song(search_textbox, window),
                                                                 search_button.destroy(),
                                                                 search_textbox.configure(state="disabled"),
                                                                 ])

        heading.pack(pady=10)
        search_textbox.pack(pady=10)
        search_button.pack(pady=10)

        window.mainloop()
