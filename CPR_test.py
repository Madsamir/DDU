import arcade
import time
import subprocess

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

    def setup(self):
        arcade.set_background_color(arcade.color.ALMOND)
        self.torso = arcade.load_texture("CHEST.png")

    def on_draw(self):
        arcade.start_render()

        arcade.draw_text(f"Tid gået: {self.tid_gaaet:.2f}", 10, 10, arcade.color.BLACK, 12)
        arcade.draw_text("Tryk på brystet i rytme til CPR", 180, 400, arcade.color.BLACK, 24)
        arcade.draw_text("Husk at få omkring 100-120 tryk i minuttet", 200, 50, arcade.color.BLACK, 16)
        arcade.draw_texture_rectangle(400, 250, 200, 200, self.torso)

        if self.printed_result:
            result_text = f"Du har trykket {self.clicks} gange, svarende til {self.clicks * 4} tryk i minuttet"
            arcade.draw_text(result_text, 150, 200, arcade.color.BLACK, 18)

    def on_update(self, delta_time):
        if self.start_time is not None:
            elapsed_time = time.time() - self.start_time
            self.tid_gaaet = max(0, self.total_time - elapsed_time)

        if self.tid_gaaet <= 0 and not self.printed_result:
            self.printed_result = True

    def on_mouse_press(self, x: int, y: int, button: int, modifiers: int):
        if self.start_time is None:
            self.start_time = time.time()

        if self.tid_gaaet > 0 and x > 325 and x < 465 and y > 225 and y < 300:
            self.clicks += 1
            print(self.clicks)

def main():
    window = MyWindow(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    window.setup()
    arcade.run()

if __name__ == "__main__":
    main()
