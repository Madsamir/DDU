import random
import arcade
from pyglet.math import Vec2
import subprocess

SPRITE_SCALING = 0.5

DEFAULT_SCREEN_WIDTH = 800
DEFAULT_SCREEN_HEIGHT = 600
SCREEN_TITLE = "Sprite Move with Scrolling Screen Example"

    
VIEWPORT_MARGIN = 220

# How fast the camera pans to the player. 1.0 is instant.
CAMERA_SPEED = 0.1

# How fast the character moves
PLAYER_MOVEMENT_SPEED = 7


class MyGame(arcade.Window):
    """ Main application class. """

    def __init__(self, width, height, title):
        super().__init__(width, height, title, resizable=True)
        self.camera_sprites = arcade.Camera(DEFAULT_SCREEN_WIDTH, DEFAULT_SCREEN_HEIGHT)
        self.camera_gui = arcade.Camera(DEFAULT_SCREEN_WIDTH, DEFAULT_SCREEN_HEIGHT)

        # Sprite lists
        self.player_list = None
        self.wall_list = None
        self.square_list = None  # Added square list
        self.player = None

        # Set up the player
        self.player_sprite = None

        # Physics engine
        self.physics_engine = None

        # Track the current state of what key is pressed
        self.left_pressed = False
        self.right_pressed = False
        self.up_pressed = False
        self.down_pressed = False

    def setup(self):
        """ Set up the game and initialize the variables. """
        self.player_list = arcade.SpriteList()
        self.wall_list = arcade.SpriteList()
        self.square_list = arcade.SpriteList()  # Initialize square list

        # Set up the player
        self.player_sprite = arcade.Sprite(":resources:images/animated_characters/female_person/femalePerson_idle.png",
                                           scale=0.4)
        self.player_sprite.center_x = 256
        self.player_sprite.center_y = 512
        self.player_list.append(self.player_sprite)

        # Set up walls
        for x in range(200, 1650, 210):
            for y in range(0, 1600, 64):
                if random.randrange(5) > 0:
                    wall = arcade.Sprite(":resources:images/tiles/grassCenter.png", SPRITE_SCALING)
                    wall.center_x = x
                    wall.center_y = y
                    self.wall_list.append(wall)

        # Set up a square outside the walls but between them
        self.min_x = min(wall.center_x for wall in self.wall_list)
        self.max_x = max(wall.center_x for wall in self.wall_list)
        self.min_y = min(wall.center_y for wall in self.wall_list)
        self.max_y = max(wall.center_y for wall in self.wall_list)

        # Spawn the square outside the walls
        while True:
            self.char = arcade.Sprite(":resources:images/items/coinGold.png", scale=0.5)
            self.char.center_x = random.uniform(self.min_x, self.max_x)
            self.char.center_y = random.uniform(self.min_y, self.max_y)
            if not arcade.check_for_collision_with_list(self.char, self.wall_list):
                break

        self.square_list.append(self.char)

        self.physics_engine = arcade.PhysicsEngineSimple(self.player_sprite, self.wall_list)
        arcade.set_background_color(arcade.color.AMAZON)
    def on_draw(self):
        """ Render the screen. """
        self.clear()
        self.camera_sprites.use()

        # Draw sprites
        self.wall_list.draw()
        self.player_list.draw()
        self.square_list.draw()  # Draw square

        # GUI
        self.camera_gui.use()
        arcade.draw_rectangle_filled(self.width // 2, 20, self.width, 40, arcade.color.ALMOND)
        text = f"Scroll value: ({self.camera_sprites.position[0]:5.1f}, {self.camera_sprites.position[1]:5.1f})"
        arcade.draw_text(text, 10, 10, arcade.color.BLACK_BEAN, 20)

    def on_key_press(self, key, modifiers):
        """Called whenever a key is pressed. """

        if key == arcade.key.UP or key == arcade.key.W:
            self.up_pressed = True
        elif key == arcade.key.DOWN or key == arcade.key.S:
            self.down_pressed = True
        elif key == arcade.key.LEFT or key == arcade.key.A:
            self.left_pressed = True
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.right_pressed = True

    def on_key_release(self, key, modifiers):

        if key == arcade.key.UP or key == arcade.key.W:
            self.up_pressed = False
        elif key == arcade.key.DOWN or key == arcade.key.S:
            self.down_pressed = False
        elif key == arcade.key.LEFT or key == arcade.key.A:
            self.left_pressed = False
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.right_pressed = False

    def on_update(self, delta_time):
        """ Movement and game logic """

        # Calculate speed based on the keys pressed
        self.player_sprite.change_x = 0
        self.player_sprite.change_y = 0

        if self.up_pressed and not self.down_pressed:
            self.player_sprite.change_y = PLAYER_MOVEMENT_SPEED
        elif self.down_pressed and not self.up_pressed:
            self.player_sprite.change_y = -PLAYER_MOVEMENT_SPEED
        if self.left_pressed and not self.right_pressed:
            self.player_sprite.change_x = -PLAYER_MOVEMENT_SPEED
        elif self.right_pressed and not self.left_pressed:
            self.player_sprite.change_x = PLAYER_MOVEMENT_SPEED

        # Call update on all sprites (The sprites don't do much in this
        # example though.)
        self.physics_engine.update()

        for coin_sprite in self.square_list:
            if arcade.check_for_collision(self.player_sprite, coin_sprite):
                subprocess.run(["python", "CPR_test.py"])
                while True:
                    self.char = arcade.Sprite(":resources:images/items/coinGold.png", scale=0.5)
                    self.char.center_x = random.uniform(self.min_x, self.max_x)
                    self.char.center_y = random.uniform(self.min_y, self.max_y)
                    if not arcade.check_for_collision_with_list(self.char, self.wall_list):
                        break

                coin_sprite.remove_from_sprite_lists()

        self.scroll_to_player()



    def scroll_to_player(self):

        """

        Scroll the window to the player.



        if CAMERA_SPEED is 1, the camera will immediately move to the desired position.

        Anything between 0 and 1 will have the camera move to the location with a smoother

        pan.

        """



        position = Vec2(self.player_sprite.center_x - self.width / 2,

                        self.player_sprite.center_y - self.height / 2)

        self.camera_sprites.move_to(position, CAMERA_SPEED)



    def on_resize(self, width, height):

        """

        Resize window

        Handle the user grabbing the edge and resizing the window.

        """

        self.camera_sprites.resize(int(width), int(height))

        self.camera_gui.resize(int(width), int(height))


def main():
    """ Main function """
    window = MyGame(DEFAULT_SCREEN_WIDTH, DEFAULT_SCREEN_HEIGHT, SCREEN_TITLE)
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()