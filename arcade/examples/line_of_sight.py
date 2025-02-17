"""
Line of Sight

Artwork from https://kenney.nl

If Python and Arcade are installed, this example can be run from the command line with:
python -m arcade.examples.line_of_sight
"""

import arcade
import random

SPRITE_SCALING = 0.5

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = "Line of Sight"

MOVEMENT_SPEED = 5

VIEWPORT_MARGIN = 250


class MyGame(arcade.Window):
    """
    Main application class.
    """

    def __init__(self, width, height, title):
        """
        Initializer
        """

        # Call the parent class initializer
        super().__init__(width, height, title)

        # Variables that will hold sprite lists
        self.player_list = None
        self.wall_list = None
        self.enemy_list = None

        # Set up the player info
        self.player = None

        # Track the current state of what key is pressed
        self.left_pressed = False
        self.right_pressed = False
        self.up_pressed = False
        self.down_pressed = False

        self.physics_engine = None

        # Camera for scrolling
        self.cam = None

        # Set the background color
        self.background_color = arcade.color.AMAZON

    def setup(self):
        """ Set up the game and initialize the variables. """

        # Camera
        self.cam = arcade.camera.Camera2D()

        # Sprite lists
        self.player_list = arcade.SpriteList()
        self.wall_list = arcade.SpriteList(use_spatial_hash=True)
        self.enemy_list = arcade.SpriteList()

        # Set up the player
        self.player = arcade.Sprite(":resources:images/animated_characters/female_person/femalePerson_idle.png",
                                    scale=SPRITE_SCALING)
        self.player.center_x = 50
        self.player.center_y = 350
        self.player_list.append(self.player)

        # Set enemies
        enemy = arcade.Sprite(":resources:images/animated_characters/zombie/zombie_idle.png", scale=SPRITE_SCALING)
        enemy.center_x = 350
        enemy.center_y = 350
        self.enemy_list.append(enemy)

        spacing = 200
        for column in range(10):
            for row in range(10):
                sprite = arcade.Sprite(":resources:images/tiles/grassCenter.png", scale=SPRITE_SCALING)

                x = (column + 1) * spacing
                y = (row + 1) * sprite.height

                sprite.center_x = x
                sprite.center_y = y
                if random.randrange(100) > 20:
                    self.wall_list.append(sprite)

        self.physics_engine = arcade.PhysicsEngineSimple(self.player,
                                                         self.wall_list)

    def on_draw(self):
        """
        Render the screen.
        """
        try:
            # This command has to happen before we start drawing
            self.clear()

            # Draw all the sprites.
            self.player_list.draw()
            self.wall_list.draw()
            self.enemy_list.draw()

            for enemy in self.enemy_list:
                if arcade.has_line_of_sight(self.player.position,
                                            enemy.position,
                                            self.wall_list):
                    color = arcade.color.RED
                else:
                    color = arcade.color.WHITE
                arcade.draw_line(self.player.center_x,
                                 self.player.center_y,
                                 enemy.center_x,
                                 enemy.center_y,
                                 color,
                                 2)

        except Exception as e:
            print(e)

    def on_update(self, delta_time):
        """ Movement and game logic """

        # Calculate speed based on the keys pressed
        self.player.change_x = 0
        self.player.change_y = 0

        if self.up_pressed and not self.down_pressed:
            self.player.change_y = MOVEMENT_SPEED
        elif self.down_pressed and not self.up_pressed:
            self.player.change_y = -MOVEMENT_SPEED
        if self.left_pressed and not self.right_pressed:
            self.player.change_x = -MOVEMENT_SPEED
        elif self.right_pressed and not self.left_pressed:
            self.player.change_x = MOVEMENT_SPEED

        self.physics_engine.update()

        # --- Manage Scrolling ---

        # Keep track of if we changed the boundary. We don't want to
        # update the camera if we don't need to.
        changed = False

        pos = self.cam.position

        top_left = self.cam.top_left
        bottom_right = self.cam.bottom_right

        # Scroll left
        left_boundary = top_left[0] + VIEWPORT_MARGIN
        if self.player.left < left_boundary:
            changed = True
            pos = pos[0] + (self.player.left - left_boundary), pos[1]

        # Scroll up
        top_boundary = top_left[1] - VIEWPORT_MARGIN
        if self.player.top > top_boundary:
            changed = True
            pos = pos[0], pos[1] + (self.player.top - top_boundary)

        # Scroll right
        right_boundary = bottom_right[0] - VIEWPORT_MARGIN
        if self.player.right > right_boundary:
            changed = True
            pos = pos[0] + (self.player.right - right_boundary), pos[1]

        # Scroll down
        bottom_boundary = bottom_right[1] + VIEWPORT_MARGIN
        if self.player.bottom < bottom_boundary:
            changed = True
            pos = pos[0], pos[1] + (self.player.bottom - bottom_boundary)

        # If we changed the boundary values, update the view port to match
        if changed:
            self.cam.position = pos
            self.cam.use()

    def on_key_press(self, key, modifiers):
        """Called whenever a key is pressed. """

        if key == arcade.key.UP:
            self.up_pressed = True
        elif key == arcade.key.DOWN:
            self.down_pressed = True
        elif key == arcade.key.LEFT:
            self.left_pressed = True
        elif key == arcade.key.RIGHT:
            self.right_pressed = True

    def on_key_release(self, key, modifiers):
        """Called when the user releases a key. """

        if key == arcade.key.UP:
            self.up_pressed = False
        elif key == arcade.key.DOWN:
            self.down_pressed = False
        elif key == arcade.key.LEFT:
            self.left_pressed = False
        elif key == arcade.key.RIGHT:
            self.right_pressed = False


def main():
    """ Main function """
    window = MyGame(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()
