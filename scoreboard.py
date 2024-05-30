import customtkinter
from PIL import Image


class ScoreBoard:
    def __init__(self, score, greats, okays, misses):
        self.score = score
        self.greats = greats
        self.okays = okays
        self.misses = misses
        self.scoreboard_screen()

    def scoreboard_screen(self):
        customtkinter.set_appearance_mode("dark")
        customtkinter.set_default_color_theme("green")
        window = customtkinter.CTk()
        window.geometry("800x1000")
        window.title("smusic")

        my_image = customtkinter.CTkImage(light_image=Image.open("pygame/images/logo.png"),
                                          dark_image=Image.open("pygame/images/logo.png"),
                                          size=(238, 116))

        heading = customtkinter.CTkLabel(window, text="", image=my_image)
        greats = customtkinter.CTkLabel(window, text="GREAT: " + str(self.greats))
        okays = customtkinter.CTkLabel(window, text="OKAY: " + str(self.okays))
        misses = customtkinter.CTkLabel(window, text="MISSED: " + str(self.misses))
        total = customtkinter.CTkLabel(window, text="SCORE: " + str(self.score))

        heading.pack(pady=10)
        greats.pack(pady=10)
        okays.pack(pady=10)
        misses.pack(pady=10)
        total.pack(pady=10)

        window.mainloop()
