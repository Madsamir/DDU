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
        self.total_time = 15  # Total time in seconds
        self.tid_gaaet = self.total_time
        self.printed_result = False  # Variable to track if the result has been printed

    def setup(self):
        arcade.set_background_color(arcade.color.ALMOND)

    def on_draw(self):
        # Render the screen
        arcade.start_render()

        # Draw your graphics here
        arcade.draw_text(f"Tid gået: {self.tid_gaaet:.2f}", 10, 10, arcade.color.BLACK, 12)
        arcade.draw_text("Tryk på skærmen i rytme til CPR", 180, 300, arcade.color.BLACK, 24)


    def on_update(self, delta_time):
        if self.start_time is not None:
            elapsed_time = time.time() - self.start_time
            self.tid_gaaet = max(0, self.total_time - elapsed_time)

        if self.tid_gaaet <= 0 and not self.printed_result:
            print(f" Du har trykket {self.clicks} gange, svarende til {self.clicks * 4} tryk i minuttet")
            self.printed_result = True  # Set the flag to True to indicate the result has been printed

    def on_mouse_press(self, x: int, y: int, button: int, modifiers: int):
        if self.start_time is None:
            self.start_time = time.time()

        if self.tid_gaaet > 0:
            self.clicks += 1

def main():
    window = MyWindow(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    window.setup()
    arcade.run()

if __name__ == "__main__":
    main()
