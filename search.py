import io
import urllib.request
from tkinter import *
import customtkinter
from PIL import Image, ImageTk
import requests

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

    @staticmethod
    def get_song_choice():
        print("select song")
        return int(input())

    def search_for_song(self, search_textbox, window):
        song = search_textbox.get("1.0", "end-1c")
        search = self.sp.search(song, 5)

        with urllib.request.urlopen(search["tracks"]["items"][0]["album"]["images"][0]["url"]) as u:
            raw_data = u.read()

        my_image = customtkinter.CTkImage(light_image=Image.open(io.BytesIO(raw_data)),
                                          dark_image=Image.open(io.BytesIO(raw_data)),
                                          size=(180, 180))  # WidthxHeight

        image_1 = customtkinter.CTkLabel(window, text="", image=my_image)

        song_button_1 = customtkinter.CTkButton(window, text=search["tracks"]["items"][0]["name"] + " by " +
                                                             search["tracks"]["items"][0]["artists"][0]["name"],
                                                font=("Impact", 20),
                                                command=lambda: self.start_game(search["tracks"]["items"][0]["uri"],
                                                                                window))

        with urllib.request.urlopen(search["tracks"]["items"][1]["album"]["images"][0]["url"]) as u:
            raw_data = u.read()

        my_image = customtkinter.CTkImage(light_image=Image.open(io.BytesIO(raw_data)),
                                          dark_image=Image.open(io.BytesIO(raw_data)),
                                          size=(180, 180))  # WidthxHeight

        image_2 = customtkinter.CTkLabel(window, text="", image=my_image)

        song_button_2 = customtkinter.CTkButton(window, text=search["tracks"]["items"][1]["name"] + " by " +
                                                             search["tracks"]["items"][1]["artists"][0]["name"],
                                                font=("Impact", 20),
                                                command=lambda: self.start_game(search["tracks"]["items"][1]["uri"],
                                                                                window))

        with urllib.request.urlopen(search["tracks"]["items"][2]["album"]["images"][0]["url"]) as u:
            raw_data = u.read()

        my_image = customtkinter.CTkImage(light_image=Image.open(io.BytesIO(raw_data)),
                                          dark_image=Image.open(io.BytesIO(raw_data)),
                                          size=(180, 180))  # WidthxHeight

        image_3 = customtkinter.CTkLabel(window, text="", image=my_image)

        song_button_3 = customtkinter.CTkButton(window, text=search["tracks"]["items"][2]["name"] + " by " +
                                                             search["tracks"]["items"][2]["artists"][0]["name"],
                                                font=("Impact", 20),
                                                command=lambda: self.start_game(search["tracks"]["items"][2]["uri"],
                                                                                window))

        with urllib.request.urlopen(search["tracks"]["items"][3]["album"]["images"][0]["url"]) as u:
            raw_data = u.read()

        my_image = customtkinter.CTkImage(light_image=Image.open(io.BytesIO(raw_data)),
                                          dark_image=Image.open(io.BytesIO(raw_data)),
                                          size=(180, 180))  # WidthxHeight

        image_4 = customtkinter.CTkLabel(window, text="", image=my_image)

        song_button_4 = customtkinter.CTkButton(window, text=search["tracks"]["items"][3]["name"] + " by " +
                                                             search["tracks"]["items"][3]["artists"][0]["name"],
                                                font=("Impact", 20),
                                                command=lambda: self.start_game(search["tracks"]["items"][3]["uri"],
                                                                                window))

        with urllib.request.urlopen(search["tracks"]["items"][4]["album"]["images"][0]["url"]) as u:
            raw_data = u.read()

        my_image = customtkinter.CTkImage(light_image=Image.open(io.BytesIO(raw_data)),
                                          dark_image=Image.open(io.BytesIO(raw_data)),
                                          size=(180, 180))  # WidthxHeight

        image_5 = customtkinter.CTkLabel(window, text="", image=my_image)

        song_button_5 = customtkinter.CTkButton(window, text=search["tracks"]["items"][4]["name"] + " by " +
                                                             search["tracks"]["items"][4]["artists"][0]["name"],
                                                font=("Impact", 20),
                                                command=lambda: self.start_game(search["tracks"]["items"][4]["uri"],
                                                                                window))

        image_1.pack(pady=10)
        song_button_1.pack(pady=5)

        image_2.pack(pady=10)
        song_button_2.pack(pady=5)

        image_3.pack(pady=10)
        song_button_3.pack(pady=5)

        image_4.pack(pady=10)
        song_button_4.pack(pady=5)

        image_5.pack(pady=10)
        song_button_5.pack(pady=5)

    def start_game(self, song, window):
        window.destroy()
        new_game = SmusicGame(song, self.sp)
        new_game.start_beat_game()

    def search_screen(self):
        customtkinter.set_appearance_mode("dark")
        customtkinter.set_default_color_theme("green")
        window = customtkinter.CTk()

        heading = customtkinter.CTkLabel(window, text="SMUSIC", font=("Impact", 40))
        search_textbox = customtkinter.CTkTextbox(window, height=100, width=400, font=("Impact", 40))
        search_button = customtkinter.CTkButton(window, text="search", font=("Impact", 30),
                                                command=lambda: self.search_for_song(search_textbox, window))

        heading.pack(pady=10)
        search_textbox.pack(pady=10)
        search_button.pack(pady=10)

        window.geometry("800x1000")
        window.mainloop()
