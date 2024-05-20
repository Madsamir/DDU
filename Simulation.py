import random
from uuid import uuid4
import subprocess
import arcade
from pyglet.math import Vec2

SPRITE_SCALING = 0.5

DEFAULT_SCREEN_WIDTH = 800
DEFAULT_SCREEN_HEIGHT = 600
SCREEN_TITLE = "Minimap Example"

# How many pixels to keep as a minimum margin between the character
# and the edge of the screen.
VIEWPORT_MARGIN = 220

# How fast the camera pans to the player. 1.0 is instant.
CAMERA_SPEED = 0.1

# How fast the character moves
PLAYER_MOVEMENT_SPEED = 7


# Background color must include an alpha component

MINIMAP_BACKGROUND_COLOR = arcade.get_four_byte_color(arcade.color.ALMOND)

MINIMAP_WIDTH = 256

MINIMAP_HEIGHT = 256

MAP_WIDTH = 2048

MAP_HEIGHT = 2048



class MyGame(arcade.Window):

    def __init__(self, width, height, title):
        super().__init__(width, height, title, resizable=True)

        # Sprite lists
        self.player_list = None
        self.wall_list = None
        self.square_list = None
        self.green_tegn_list = None
        self.hjertestater = False
        self.points = 0
        # Mini-map related

        # List of all our minimaps (there's just one)

        self.minimap_sprite_list = None

        # Texture and associated sprite to render our minimap to

        self.minimap_texture = None

        self.minimap_sprite = None


        # Set up the player
        self.player_sprite = None
        self.green_tegn_sprite = None

        self.physics_engine = None

        # Camera for sprites, and one for our GUI
        self.camera_sprites = arcade.Camera(DEFAULT_SCREEN_WIDTH, DEFAULT_SCREEN_HEIGHT)
        self.camera_gui = arcade.Camera(DEFAULT_SCREEN_WIDTH, DEFAULT_SCREEN_HEIGHT)

    def setup(self):
        """ Set up the game and initialize the variables. """

        # Sprite lists
        self.player_list = arcade.SpriteList()
        self.wall_list = arcade.SpriteList()
        self.square_list = arcade.SpriteList()
        self.green_tegn_list = arcade.SpriteList()

        # Set up the player
        self.player_sprite = arcade.Sprite("Main.png",
                                           scale=0.4)
        self.green_tegn_sprite = arcade.Sprite("Green_maps.png", scale = 0.2)
        self.green_tegn_sprite.center_x = 90
        self.green_tegn_sprite.center_y = 100
        self.green_tegn_list.append(self.green_tegn_sprite)

        self.player_sprite.center_x = 256
        self.player_sprite.center_y = 512
        self.player_list.append(self.player_sprite)

        # -- Set up several columns of walls
        for x in range(0, MAP_WIDTH, 210):
            for y in range(0, MAP_HEIGHT, 64):
                # Randomly skip a box so the player can find a way through
                if random.randrange(5) > 0:
                    building = random.randint(1,4)
                    if building == 1:
                        wall = arcade.Sprite("tile_0010.png", SPRITE_SCALING + 3)
                    elif building == 2:
                        wall = arcade.Sprite("tile_0009.png", SPRITE_SCALING + 3)
                    elif building == 3:
                        wall = arcade.Sprite("tile_0008.png", SPRITE_SCALING + 3)
                    elif building == 4:
                        wall = arcade.Sprite("tile_0011.png", SPRITE_SCALING + 3)
                    wall.center_x = x
                    wall.center_y = y
                    self.wall_list.append(wall)
        min_x = min(wall.center_x for wall in self.wall_list)
        max_x = max(wall.center_x for wall in self.wall_list)
        min_y = min(wall.center_y for wall in self.wall_list)
        max_y = max(wall.center_y for wall in self.wall_list)

        # Spawn the square outside the walls
        while True:
            self.char = arcade.Sprite("Dead_new.png", scale=0.2)
            self.char.center_x = random.uniform(min_x, max_x)
            self.char.center_y = random.uniform(min_y, max_y)
            if not arcade.check_for_collision_with_list(self.char, self.wall_list):
                break

        self.square_list.append(self.char)

        self.physics_engine = arcade.PhysicsEngineSimple(self.player_sprite, self.wall_list)
        arcade.set_background_color(arcade.color.AMAZON)

        # Set the background color
        arcade.set_background_color(arcade.color.AMAZON)


        # Construct the minimap

        size = (MINIMAP_WIDTH - 50, MINIMAP_HEIGHT - 50)

        self.minimap_texture = arcade.Texture.create_empty(str(uuid4()), size)

        self.minimap_sprite = arcade.Sprite(center_x=(MINIMAP_WIDTH - 48) / 2,

                                            center_y=self.height - (MINIMAP_HEIGHT - 50) / 2,

                                            texture=self.minimap_texture)



        self.minimap_sprite_list = arcade.SpriteList()

        self.minimap_sprite_list.append(self.minimap_sprite)



    def update_minimap(self):

        proj = 0, MAP_WIDTH, 0, MAP_HEIGHT

        with self.minimap_sprite_list.atlas.render_into(self.minimap_texture, projection=proj) as fbo:

            fbo.clear(MINIMAP_BACKGROUND_COLOR)

            self.wall_list.draw()
            self.char.scale = 1
            self.square_list.draw()
            self.char.scale = 0.3

            self.player_sprite.scale = 0.4  # Set the desired scale
            self.player_sprite.draw()
            self.player_sprite.scale = 0.15
            self.green_tegn_sprite.scale = 0.5
            self.green_tegn_list.draw()
            self.green_tegn_sprite.scale = 0.2


    def on_draw(self):
        """
        Render the screen.
        """

        # This command has to happen before we start drawing
        self.clear()

        # Select the camera we'll use to draw all our sprites
        self.camera_sprites.use()

        # Draw all the sprites.
        self.wall_list.draw()
        self.player_list.draw()
        self.square_list.draw()
        self.green_tegn_list.draw()

        # Select the (unscrolled) camera for our GUI
        self.camera_gui.use()


        # Update the minimap

        self.update_minimap()



        # Draw the minimap

        self.minimap_sprite_list.draw()


        # Draw the GUI
        arcade.draw_rectangle_filled(self.width // 2, 20, self.width, 40, arcade.color.ALMOND)
        text = f"Du har: {self.points} points"
        arcade.draw_text(text, 10, 10, arcade.color.BLACK_BEAN, 20)

    def on_key_press(self, key, modifiers):
        """Called whenever a key is pressed. """

        if key == arcade.key.UP or key == arcade.key.W:
            self.player_sprite.change_y = PLAYER_MOVEMENT_SPEED
        elif key == arcade.key.DOWN or key == arcade.key.S:
            self.player_sprite.change_y = -PLAYER_MOVEMENT_SPEED
        elif key == arcade.key.LEFT or key == arcade.key.A:
            self.player_sprite.change_x = -PLAYER_MOVEMENT_SPEED
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.player_sprite.change_x = PLAYER_MOVEMENT_SPEED

    def on_key_release(self, key, modifiers):
        """Called when the user releases a key. """

        if key == arcade.key.UP or key == arcade.key.DOWN or key == arcade.key.W or key == arcade.key.S:
            self.player_sprite.change_y = 0
        elif key == arcade.key.LEFT or key == arcade.key.RIGHT or key == arcade.key.A or key == arcade.key.D:
            self.player_sprite.change_x = 0

    def on_update(self, delta_time):
        """ Movement and game logic """

        # Call update on all sprites (The sprites don't do much in this
        # example though.)
        for character in self.square_list:
            if arcade.check_for_collision(self.player_sprite, character):
                print("Touched")
                character.remove_from_sprite_lists()
                # Run another script
                if self.hjertestater == False:
                    subprocess.run(["python", "CPR_test.py"])
                else:
                    self.hjertestater = False
                    self.points += 1
                # Replace "another_script.py" with the name of your script
                # and make sure it's in the same directory as your main script.
        for green_tegn in self.green_tegn_list:
            if arcade.check_for_collision(self.player_sprite, green_tegn):
                green_tegn.remove_from_sprite_lists()
                self.hjertestater = True
        self.physics_engine.update()

        # Scroll the screen to the player
        self.scroll_to_player()

    def scroll_to_player(self):

        # Scroll to the proper location
        position = Vec2(self.player_sprite.center_x - self.width / 2,
                        self.player_sprite.center_y - self.height / 2)
        self.camera_sprites.move_to(position, CAMERA_SPEED)

    def on_resize(self, width, height):

        self.camera_sprites.resize(int(width), int(height))
        self.camera_gui.resize(int(width), int(height))


def main():
    """ Main function """
    window = MyGame(DEFAULT_SCREEN_WIDTH, DEFAULT_SCREEN_HEIGHT, SCREEN_TITLE)
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()