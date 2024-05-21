import random
import arcade
import time

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = "Livredder Simulator"

class MyWindow(arcade.Window):
    def __init__(self, width, height, title):
        super().__init__(width, height, title)

        self.clicks = 0
        self.start_time = None
        self.total_time = 15
        self.tid_gaaet = self.total_time
        self.printed_result = False
        self.press_sound = None
        self.hjertesimulator = False
        self.puls_tjek = True
        self.tjekket = False
        self.har_puls = random.randint(1, 3)
        self.printet_puls = None
        self.background = None  # Tilføjet til baggrundsbilledet

    def setup(self):
        arcade.set_background_color(arcade.color.ALMOND)
        self.torso = arcade.load_texture("CHEST.png")
        self.puls_krop = arcade.load_texture("Man_passed_out.png")
        self.press_sound = arcade.load_sound("mixkit-arcade-game-jump-coin-216.wav")
        self.background = arcade.load_texture("image.png")  # Indlæs baggrundsbilledet

    def on_draw(self):
        arcade.start_render()
        arcade.draw_lrwh_rectangle_textured(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT, self.background)  # Tegn baggrundsbilledet
        if self.hjertesimulator:
            self.hjertesimulation()
        elif self.puls_tjek:
            self.puls_tjekker()

    def on_update(self, delta_time):
        if self.start_time is not None and self.hjertesimulator:
            elapsed_time = time.time() - self.start_time
            self.tid_gaaet = max(0, self.total_time - elapsed_time)

        if self.tid_gaaet <= 0 and not self.printed_result:
            self.printed_result = True

    def on_mouse_press(self, x: int, y: int, button: int, modifiers: int):
        print("Mouse pressed at:", x, y)  # Tilføjet til at kontrollere, om denne metode bliver kaldt

        if self.puls_tjek and (
            (385 < x < 400 and 360 < y < 385) or
            (410 < x < 430 and 360 < y < 385) or
            (470 < x < 490 and 220 < y < 240) or
            (325 < x < 345 and 200 < y < 225)
        ):
            if self.har_puls == 1 and not self.tjekket:
                self.printet_puls = True
                self.tjekket = True
            else:
                self.printet_puls = False
                self.tjekket = True

        if self.tjekket and 650 < x < 800 and 550 < y < 600:
            print("Switching to hjertesimulation...")  # Kontrollere, om denne betingelse er opfyldt
            self.hjertesimulator = True
            self.puls_tjek = False
            self.start_time = None  # Nulstille starttiden
            self.clicks = 0  # Nulstille antallet af klik

        if self.start_time is None and self.hjertesimulator:
            self.start_time = time.time()

        if self.tid_gaaet > 0 and 325 < x < 465 and 225 < y < 300 and self.hjertesimulator:
            self.clicks += 1
            arcade.play_sound(self.press_sound)

    def hjertesimulation(self):
        arcade.draw_text(f"Tid gået: {self.tid_gaaet:.2f}", 10, 10, arcade.color.BLACK, 12)
        arcade.draw_text("Tryk på brystet i rytme til CPR", 180, 400, arcade.color.BLACK, 24)
        arcade.draw_text("Husk at få omkring 100-120 tryk i minuttet", 200, 50, arcade.color.BLACK, 16)
        arcade.draw_texture_rectangle(400, 250, 100, 100, self.torso)

        if self.printed_result:
            result_text = f"Du har trykket {self.clicks} gange, svarende til {self.clicks * 4} tryk i minuttet"
            arcade.draw_text(result_text, 150, 200, arcade.color.BLACK, 18)

    def puls_tjekker(self):
        arcade.draw_text("Tjek pulsen", 320, 475, arcade.color.BLACK, 24)
        arcade.draw_texture_rectangle(400, 250, 400, 400, self.puls_krop)

        if self.printet_puls:
            arcade.draw_text("Bro har en puls", 300, 525, arcade.color.BLACK, 18)
            arcade.draw_rectangle_filled(750, 575, 200, 50, arcade.color.WHITE)
            arcade.draw_rectangle_filled(50, 575, 200, 50, arcade.color.WHITE)
            arcade.draw_text("GIV CPR", 675, 570, arcade.color.BLACK, 18)
            arcade.draw_text("Sæt i stabilt sideleje", 7, 570, arcade.color.BLACK, 12)
        elif self.printet_puls == False:
            arcade.draw_text("Bro har ingen puls", 300, 525, arcade.color.BLACK, 18)
            arcade.draw_rectangle_filled(750, 575, 200, 50, arcade.color.WHITE)
            arcade.draw_rectangle_filled(50, 575, 200, 50, arcade.color.WHITE)
            arcade.draw_text("GIV CPR", 675, 570, arcade.color.BLACK, 18)
            arcade.draw_text("Sæt i stabilt sideleje", 7, 570, arcade.color.BLACK, 12)

def main():
    window = MyWindow(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    window.setup()
    arcade.run()

if __name__ == "__main__":
    main()
