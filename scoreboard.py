import customtkinter
from PIL import Image


class ScoreBoard:
    def __init__(self, score, greats, okays, misses):
        self.score = score
        self.greats = greats
        self.okays = okays
        self.misses = misses
        self.scoreboard_screen()

    def calculate_grade(self):
        total_hits = self.greats + self.okays + self.misses
        if total_hits == 0:
            return "F"
        if total_hits == self.greats:
            return "S"
        elif total_hits == self.greats + self.okays:
            return "A"
        elif self.misses / total_hits < 0.1:
            return "B"
        elif self.misses / total_hits < 0.2:
            return "C"
        elif self.misses / total_hits < 0.3:
            return "D"
        elif self.misses / total_hits < 0.4:
            return "E"
        else:
            return "F"

    def scoreboard_screen(self):
        customtkinter.set_appearance_mode("dark")
        customtkinter.set_default_color_theme("green")
        window = customtkinter.CTk()
        window.geometry("800x1000")
        window.title("smusic")

        my_image = customtkinter.CTkImage(light_image=Image.open("pygame/images/logo.png"),
                                          dark_image=Image.open("pygame/images/logo.png"),
                                          size=(238, 116))
        grade = self.calculate_grade()

        mark = customtkinter.CTkImage(light_image=Image.open(f"pygame/images/{grade}.png"),
                                          dark_image=Image.open(f"pygame/images/{grade}.png"),
                                          size=(272, 274))

        heading = customtkinter.CTkLabel(window, text="", image=my_image)
        grade_image = customtkinter.CTkLabel(window, text="", image=mark)
        greats = customtkinter.CTkLabel(window, height=50, width=400, font=("Impact", 40), text="GREAT: " + str(self.greats))
        okays = customtkinter.CTkLabel(window, height=50, width=400, font=("Impact", 40), text="OKAY: " + str(self.okays))
        misses = customtkinter.CTkLabel(window, height=50, width=400, font=("Impact", 40), text="MISSED: " + str(self.misses))
        total = customtkinter.CTkLabel(window, height=50, width=400, font=("Impact", 40), text="TOTAL SCORE: " + str(self.score))

        heading.pack(pady=40)
        grade_image.pack(pady=40)
        greats.pack(pady=10)
        okays.pack(pady=10)
        misses.pack(pady=10)
        total.pack(pady=40)

        window.mainloop()
