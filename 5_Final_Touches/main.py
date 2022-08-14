# The Galaxy Project
from kivy.config import Config
from kivy.core.audio import SoundLoader

Config.set('graphics', 'width', '900')
Config.set('graphics', 'height', '400')

from kivy.lang import Builder   # You need to import Builder before you can use it
from kivy.uix.relativelayout import RelativeLayout      # We changed the MainWidget from using "Widget" to "RelativeLayout"
from kivy.app import App
from kivy.core.window import Window
from kivy.graphics import Color, Quad, Triangle
from kivy.graphics import Line
from kivy.properties import NumericProperty, Clock, ObjectProperty, StringProperty
from kivy.uix.widget import Widget
import random

Builder.load_file("menu.kv")    # The Builder loads other kivy files to be executed.

class MainWidget(RelativeLayout):
    from transforms import transform, transform_2D, transform_perspective
    from user_controls import on_touch_up, on_touch_down, keyboard_closed, on_keyboard_up, on_keyboard_down

    menu_widget = ObjectProperty()      # You have to import "ObjectProperty" in order to use it

    perspective_point_x = NumericProperty(0)
    perspective_point_y = NumericProperty(0)

    # Vertical lines
    Num_of_Vertical_Lines = 8
    Vertical_Lines_Spacing = 0.4
    vertical_lines = []

    # Horizontal lines
    num_of_horizontal_lines = 6
    horizontal_lines_spacing = 1/num_of_horizontal_lines
    horizontal_lines = []

    # Vertical movement
    current_offset_y = 0
    SPEED = 1.0
    current_y_loop = 0

    # Horizontal movement
    SPEED_X = 65.0
    current_SPEED_X = 0
    current_offset_x = 0

    # The Tiles
    Num_of_Tiles = 8
    tiles = []
    tiles_coordinates = []
    beginning_tiles_count = 10

    # The Ship/Triangle
    ship = None
    SHIP_WIDTH = 0.1
    SHIP_HEIGHT = 0.035
    SHIP_BASE_Y = 0.04
    ship_coordinates = [(0, 0), (0, 0), (0, 0)]

    # Game over state
    state_game_over = False

    # Check If Game Started
    state_game_has_started = False

    # Menu titles   (We're giving it a default text)
    menu_title = StringProperty("G   A   L   A   X   Y")   # You have to import StringProperty in order to use it
    menu_button_title = StringProperty("START")

    # Score     (The default score is 0)
    Score_TXT = StringProperty("SCORE: 0")     # (Label only accepts strings)

    # Sound
    sound_begin = None
    sound_galaxy = None
    sound_gameover_impact = None
    sound_gameover_voice = None
    sound_music1 = None
    sound_restart = None

    def __init__(self, **kwargs):
        super(MainWidget, self).__init__(**kwargs)
        self.init_vertical_lines()
        self.init_horizontal_lines()
        self._keyboard = Window.request_keyboard(self.keyboard_closed, self)
        self._keyboard.bind(on_key_down=self.on_keyboard_down)
        self._keyboard.bind(on_key_up=self.on_keyboard_up)
        self.init_tiles()
        self.init_ship()
        self.reset_game()

        # initiate the audio
        self.init_audio()

        Clock.schedule_interval(self.update, 1.0 / 60.0)
        self.sound_galaxy.play()    # Plays an audio that just says "GALAXY" when we first launch/execute the game

    def init_audio(self):
        # This is how to have audio in your app
        self.sound_begin = SoundLoader.load("audio/begin.wav")     # We need to import "SoundLoader" in order to use it
        self.sound_galaxy = SoundLoader.load("audio/galaxy.wav")
        self.sound_gameover_impact = SoundLoader.load("audio/gameover_impact.wav")
        self.sound_gameover_voice = SoundLoader.load("audio/gameover_voice.wav")
        self.sound_music1 = SoundLoader.load("audio/music1.wav")
        self.sound_restart = SoundLoader.load("audio/restart.wav")

        # Controlling the volume of the audio
        self.sound_music1.volume = 1
        self.sound_begin.volume = 0.25
        self.sound_galaxy.volume = 0.25
        self.sound_gameover_voice.volume = 0.25
        self.sound_restart.volume = 0.25
        self.sound_gameover_impact.volume = 0.6

    def reset_game(self):
        # Reset the "current_x/y_speed", the number of loops of the tiles and the x offset to zero so it doesn't just start moving when the game restarts
        self.current_offset_y = 0
        self.current_y_loop = 0
        self.current_SPEED_X = 0
        self.current_offset_x = 0

        # reset "tiles_coordinates"     (We don't have to reinitialize the tiles since it's already been done)
        self.tiles_coordinates = []
        self.pre_fill_tiles_coordinates()   # regenerate the straight lines
        self.generate_tiles_coordinates()   # generate the random tiles

        # reset the score
        self.Score_TXT = "SCORE: 0"

        # Resets "Game_Over" to be False so that the tiles can start moving again
        self.state_game_over = False

    def on_parent(self, widget, parent):
        pass

    def on_perspective_point_x(self, widget, value):
        print("PX: " + str(value))

    def on_perspective_point_y(self, widget, value):
        print("PY: " + str(value))

    def init_vertical_lines(self):
        with self.canvas:
            Color(1, 1, 1)
            for i in range(0, self.Num_of_Vertical_Lines):
                self.vertical_lines.append(Line())

    def get_line_x_from_index(self, index):
        central_line_x = self.perspective_point_x
        spacing = self.Vertical_Lines_Spacing * self.width
        current_line_num = index - 0.5
        line_x = central_line_x + current_line_num * spacing + self.current_offset_x
        return line_x

    def update_vertical_lines(self):
        start_index = -int(self.Num_of_Vertical_Lines/2) + 1
        end_index = start_index + self.Num_of_Vertical_Lines
        for num in range(start_index, end_index):
            line_x = self.get_line_x_from_index(num)
            x1, y1 = self.transform(line_x, 0)
            x2, y2 = self.transform(line_x, self.height)
            self.vertical_lines[num].points = [x1, y1, x2, y2]

    def init_horizontal_lines(self):
        with self.canvas:
            Color(1, 1, 1)
            for i in range(0, self.num_of_horizontal_lines):
                self.horizontal_lines.append(Line())

    def update_horizontal_lines(self):
        start_index = -int(self.Num_of_Vertical_Lines / 2) + 1
        end_index = start_index + self.Num_of_Vertical_Lines - 1
        xmin = self.get_line_x_from_index(start_index)
        xmax = self.get_line_x_from_index(end_index)
        for i in range(0, self.num_of_horizontal_lines):
            line_y = self.get_line_y_from_index(i)

            x1, y1 = self.transform(xmin, line_y)
            x2, y2 = self.transform(xmax, line_y)

            self.horizontal_lines[i].points = [x1, y1, x2, y2]

    def get_line_y_from_index(self, index):
        spacing_y = self.horizontal_lines_spacing * self.height
        line_y = index * spacing_y - (self.current_offset_y)
        return line_y

    def get_tile_coordinates(self, index_x, index_y):
        index_y = index_y - self.current_y_loop
        x = self.get_line_x_from_index(index_x)
        y = self.get_line_y_from_index(index_y)
        return x, y

    def init_tiles(self):
        self.pre_fill_tiles_coordinates()
        self.generate_tiles_coordinates()
        with self.canvas:
            Color(1, 1, 1)
            for i in range(0, self.Num_of_Tiles):
                self.tiles.append(Quad())

    def pre_fill_tiles_coordinates(self):
        for i in range(self.beginning_tiles_count + 1):
            self.tiles_coordinates.append((0, i))

    def generate_tiles_coordinates(self):
        last_y = int()
        last_x = int()
        start_index = -int(self.Num_of_Vertical_Lines / 2) + 1
        end_index = start_index + self.Num_of_Vertical_Lines - 2
        for i in range(len(self.tiles_coordinates) - 1, -1, -1):
            if self.tiles_coordinates[i][1] < self.current_y_loop:
                del self.tiles_coordinates[i]
        if len(self.tiles_coordinates) > 0:
            last_coordinate = self.tiles_coordinates[-1]
            last_y = last_coordinate[1] + 1
            last_x = last_coordinate[0]
        for i in range(len(self.tiles_coordinates), self.Num_of_Tiles):
            rand = random.randint(0, 2)
            if last_x == start_index and rand == 2:
                rand = 1
            elif last_x == end_index and rand == 1:
                rand = 2
            self.tiles_coordinates.append((last_x, last_y))
            if rand == 1:
                last_x += 1
                self.tiles_coordinates.append((last_x, last_y))
                last_y += 1
                self.tiles_coordinates.append((last_x, last_y))
            if rand == 2:
                last_x -= 1
                self.tiles_coordinates.append((last_x, last_y))
                last_y += 1
                self.tiles_coordinates.append((last_x, last_y))
            last_y += 1

    def update_tiles(self):
        for i in range(0, self.Num_of_Tiles):
            tile = self.tiles[i]
            tile_coordinate = self.tiles_coordinates[i]
            xmin, ymin = self.get_tile_coordinates(tile_coordinate[0], tile_coordinate[1])
            xmax, ymax = self.get_tile_coordinates(tile_coordinate[0] + 1, tile_coordinate[1] + 1)
            x1, y1 = self.transform(xmin, ymin)
            x2, y2 = self.transform(xmin, ymax)
            x3, y3 = self.transform(xmax, ymax)
            x4, y4 = self.transform(xmax, ymin)
            tile.points = [x1, y1, x2, y2, x3, y3, x4, y4]

    def init_ship(self):
        with self.canvas:
            Color(0.1, 0.1, 0.1)
            self.ship = Triangle()

    def update_ship(self):
        center_x = self.width/2
        base_y = self.SHIP_BASE_Y * self.height
        ship_half_width = self.SHIP_WIDTH * self.width/2
        ship_height = self.SHIP_HEIGHT * self.height
        self.ship_coordinates[0] = (center_x - ship_half_width, base_y)
        self.ship_coordinates[1] = (center_x, ship_height + base_y)
        self.ship_coordinates[2] = (center_x + ship_half_width, base_y)
        x1, y1 = self.transform(*self.ship_coordinates[0])
        x2, y2 = self.transform(*self.ship_coordinates[1])
        x3, y3 = self.transform(*self.ship_coordinates[2])
        self.ship.points = [x1, y1, x2, y2, x3, y3]

    def check_ship_collision_with_tile(self, tile_x, tile_y):
        xmin, ymin = self.get_tile_coordinates(tile_x, tile_y)
        xmax, ymax = self.get_tile_coordinates(tile_x + 1, tile_y + 1)
        pos_x, pos_y = self.ship_coordinates[1][0], self.ship_coordinates[1][1] - (self.SHIP_HEIGHT * self.height)/2
        return xmin <= pos_x <= xmax and ymin <= pos_y <= ymax

    def check_ship_collision(self):
        for i in range(0, len(self.ship_coordinates)):
            tile_x, tile_y = self.tiles_coordinates[i]
            if tile_y > self.current_y_loop + 1:
                return False
            if self.check_ship_collision_with_tile(tile_x, tile_y):
                return True
        return False

    def on_menu_button_pressed(self):
        # Play "Begin" audio for the 1st run and "Restart" for the following runs
        if self.state_game_over:
            self.sound_restart.play()
        else:
            self.sound_begin.play()
        self.reset_game()     # resets the game
        self.state_game_has_started = True
        self.menu_widget.opacity = 0    # We are using the ID that was imported into MainWidget in order to change its attributes

    def play_game_over_voice_sound(self, dt):
        # We are creating this function in order to play this sound with a delay
            # We are going to achieve this through "Clock.schedule_once(function, seconds )" which only schedules the delay once
                # Since the Clock module always returns deltatime, we're going to need that as a parameter for this function
        if self.state_game_over:
            self.sound_gameover_voice.play()    # If we are still in a game over state, play the sound. If the user clicks the restart button before the sound plays, don't play the sound

    def update(self, deltaTime):
        time_factor = deltaTime * 60
        self.update_vertical_lines()
        self.update_horizontal_lines()
        self.update_tiles()
        self.update_ship()

        if not self.state_game_over and self.state_game_has_started:
            speed_y = self.SPEED * self.height
            self.current_offset_y += speed_y * time_factor / 100
            spacing_y = self.horizontal_lines_spacing * self.height
            while self.current_offset_y >= spacing_y:
                self.current_offset_y -= spacing_y
                self.current_y_loop += 1

                self.Score_TXT = f"SCORE: {str(self.current_y_loop)}"        # The score is going to whatever the current_y_loop is9

                self.generate_tiles_coordinates()
            speed_x = self.current_SPEED_X * self.width     # adjusts the x axis speed to be dependent on the screen width
            self.current_offset_x += speed_x * deltaTime / 100
        if not self.check_ship_collision() and not self.state_game_over:    # If the game is over, then we're only going to run this function twice
            self.state_game_over = True
            # When the game is over, the menu appears again and with new text
            self.menu_title = "G  A  M  E    O  V  E  R"
            self.menu_button_title = "RESTART"
            self.menu_widget.opacity = 1

            # When the game is over, stop the music and play the gameover voice and impact sounds
            self.sound_music1.stop()
            self.sound_gameover_impact.play()
            Clock.schedule_once(self.play_game_over_voice_sound, 3)

            print("Game Over")


class GalaxyApp(App):
    pass


GalaxyApp().run()