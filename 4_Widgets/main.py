# The Galaxy Project
"""Used to set the size of the window"""
from kivy.config import Config
Config.set('graphics', 'width', '900')
Config.set('graphics', 'height', '400')

from kivy.app import App
from kivy.core.window import Window
from kivy.graphics import Color, Quad, Triangle
from kivy.graphics import Line
from kivy.properties import NumericProperty, Clock
from kivy.uix.widget import Widget
import random



class MainWidget(Widget):
    from transforms import transform, transform_2D, transform_perspective   # We put all the transform functions in a separate .py file called "transforms" and through this line of code, we are access these functions from this other file.
    from user_controls import on_touch_up, on_touch_down, keyboard_closed, on_keyboard_up, on_keyboard_down     # We also did the same with the touch and keyboard controls.

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
    current_y_loop = 0     # For the animation of the tiles (without this variable, the tile will just stay in one place and not move)

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
    ship = None              # Will contain the "Triangle()" shape that is drawn on a canvas
    SHIP_WIDTH = 0.1
    SHIP_HEIGHT = 0.035
    SHIP_BASE_Y = 0.04       # The distance from the bottom of the screen to the bottom of the ship
    ship_coordinates = [(0, 0), (0, 0), (0, 0)]

    # Game over state
    state_game_over = False

    def __init__(self, **kwargs):
        super(MainWidget, self).__init__(**kwargs)

        self.init_vertical_lines()
        self.init_horizontal_lines()

        self._keyboard = Window.request_keyboard(self.keyboard_closed, self)
        self._keyboard.bind(on_key_down=self.on_keyboard_down)
        self._keyboard.bind(on_key_up=self.on_keyboard_up)

        self.init_tiles()   # initializes the tiles

        self.init_ship()    # We HAVE to call "init_ship" after "init_tiles" or else the ship is going to be underneath the tiles

        Clock.schedule_interval(self.update, 1.0 / 60.0)

    def on_parent(self, widget, parent):
        pass


    def on_perspective_point_x(self, widget, value):
        print("PX: " + str(value))

    def on_perspective_point_y(self, widget, value):
        print("PY: " + str(value))

    def init_vertical_lines(self):
        """Initialize the lines"""
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
        """
        This isn't necessary anymore because this is computed in "get_line_x_from_index"

        # center_x = int(self.width/2)
        #
        # current_line_num = -int(self.Num_of_Vertical_Lines/2) + 0.5
        # spacing = self.Vertical_Lines_Spacing * self.width

        """
        start_index = -int(self.Num_of_Vertical_Lines/2) + 1        # The middle line is 0 so the starting index is gong to be negative (but since we have an even number of lines, we are going to get a line like this: "-1 0 1 2", hence the +1
        end_index = start_index + self.Num_of_Vertical_Lines        # EX: - 1 0 1 2   ==> -1 + 4 = 3

        for num in range(start_index, end_index):
            line_x = self.get_line_x_from_index(num)

            x1, y1 = self.transform(line_x, 0)
            x2, y2 = self.transform(line_x, self.height)

            self.vertical_lines[num].points = [x1, y1, x2, y2]


    """transform, transform_2D, and transform_perspective has been moved to transforms.py"""


    def init_horizontal_lines(self):
        with self.canvas:
            Color(1, 1, 1)
            for i in range(0, self.num_of_horizontal_lines):
                self.horizontal_lines.append(Line())


    def update_horizontal_lines(self):
        """
        This isn't necessary anymore because this is computed in "get_line_x_from_index"
        (This is because we just copied and pasted this code from "update_vertical_lines)

        # center_x = int(self.width/2)
        #
        # current_line_num = -int(self.Num_of_Vertical_Lines/2) + 0.5
        # spacing = self.Vertical_Lines_Spacing * self.width

        # xmin = center_x + (offset * spacing_x) - self.current_offset_x
        # xmax = center_x - (offset * spacing_x) - self.current_offset_x
        """
        start_index = -int(self.Num_of_Vertical_Lines / 2) + 1       # All we need is to copy and paste the start and end index from "update_vertical_lines"
        end_index = start_index + self.Num_of_Vertical_Lines - 1    # We are subtracting one because this actually gives us + 1 the maximum index, which is good for loops but not so much if we want the exact value

        xmin = self.get_line_x_from_index(start_index)
        xmax = self.get_line_x_from_index(end_index)

        """
        This isn't necessary anymore because this is computed in "get_line_y_from_index"
        
        # spacing_y = self.horizontal_lines_spacing * self.height
        """


        for i in range(0, self.num_of_horizontal_lines):
            line_y = self.get_line_y_from_index(i)

            x1, y1 = self.transform(xmin, line_y)
            x2, y2 = self.transform(xmax, line_y)

            self.horizontal_lines[i].points = [x1, y1, x2, y2]


    def update(self, deltaTime):
        time_factor = deltaTime * 60

        self.update_vertical_lines()
        self.update_horizontal_lines()

        self.update_tiles()
        self.update_ship()

        if not self.state_game_over:    # If the game is not over, then continue to go forwards (or sidewards), if the game is over, then stop
            """Vertical Speed/y-axis speed"""
            speed_y = self.SPEED * self.height  # adjusts the y axis speed to be dependent on the screen height
            self.current_offset_y += speed_y * time_factor / 100

            spacing_y = self.horizontal_lines_spacing * self.height
            while self.current_offset_y >= spacing_y:
                self.current_offset_y -= spacing_y

                self.current_y_loop += 1
                self.generate_tiles_coordinates()

            """Horizontal Speed/x-axis speed"""
            speed_x = self.current_SPEED_X * self.width     # adjusts the x axis speed to be dependent on the screen width
            self.current_offset_x += speed_x * deltaTime / 100

        """Ship Collision"""
        if not self.check_ship_collision() and not self.state_game_over:    # If the game is over, then we're only going to run this function twice
            self.state_game_over = True
            print("Game Over")


    """
    on_touch_up, on_touch_down, keyboard_closed, on_keyboard_up, on_keyboard_down, & is_desktop 
    has been moved to user_controls.py
    """

    def get_line_y_from_index(self, index):
        spacing_y = self.horizontal_lines_spacing * self.height
        line_y = index * spacing_y - (self.current_offset_y)

        return line_y



    def get_tile_cordinates(self, index_x, index_y):  # index_x ==> x index        index_y ==> y index
        index_y = index_y - self.current_y_loop         # This is to keep the tile to actually move instead of staying in one spot

        x = self.get_line_x_from_index(index_x)
        y = self.get_line_y_from_index(index_y)
        return x, y


    def init_tiles(self):
        self.pre_fill_tiles_coordinates()   # Creates the prefilled straight tiles before randomly generated tiles
        self.generate_tiles_coordinates()

        with self.canvas:
            Color(1, 1, 1)
            for i in range(0, self.Num_of_Tiles):
                self.tiles.append(Quad())


    def pre_fill_tiles_coordinates(self):
        for i in range(self.beginning_tiles_count + 1):
            self.tiles_coordinates.append((0, i))


    def generate_tiles_coordinates(self):
        last_y = int()                               # The value of the y value before it was incremented
        last_x = int()                               # The last x value before it was changed

        start_index = -int(self.Num_of_Vertical_Lines / 2) + 1       # Left most side
        end_index = start_index + self.Num_of_Vertical_Lines - 2     # Right most side

        # clean the coordinates that are out of the screen
        # when index_y is less than current_y_loop
        for i in range(len(self.tiles_coordinates) - 1, -1, -1):
            if self.tiles_coordinates[i][1] < self.current_y_loop:
                del self.tiles_coordinates[i]


        if len(self.tiles_coordinates) > 0:                 # If the tiles_coordinates has some tiles in it...
            last_coordinate = self.tiles_coordinates[-1]    # take the last tile and save it in a variable
            last_y = last_coordinate[1] + 1                 # and last_y will store the y value from the tuple in last_coordinate
            last_x = last_coordinate[0]                     # and last_x will store the x value from the tuple in last_coordinate

        for i in range(len(self.tiles_coordinates), self.Num_of_Tiles):
            """Random Generation of Tiles"""
            rand = random.randint(0, 2)        # inclusive of -1 and 1

            if last_x == start_index and rand == 2:
                rand = 1    # overrides to generate land on the right instead of the left
            elif last_x == end_index and rand == 1:
                rand = 2    # overrides to generate land on the left instead of the right

            # 0 => straight
            # 1 => right
            # 2 => left
            self.tiles_coordinates.append((last_x, last_y))     # moves UP one spot from the previous x value (because we called "last_y += 1" in the end of this for loop)
            if rand == 1:
                """This if statement only creates the "#*" part"""
                   #*
                #  #*
                """Only the "#*" part"""
                last_x += 1     # move right
                self.tiles_coordinates.append((last_x, last_y))
                last_y += 1     # move up
                self.tiles_coordinates.append((last_x, last_y))

            if rand == 2:
                """This if statement only creates the "#*" part"""
                #*
                #*  #
                """Only the "#*" part"""
                last_x -= 1     # moves left
                self.tiles_coordinates.append((last_x, last_y))
                last_y += 1     # moves up
                self.tiles_coordinates.append((last_x, last_y))
            """Random Generation of Tiles"""

            last_y += 1     # moves up


    def update_tiles(self):
        for i in range(0, self.Num_of_Tiles):
            tile = self.tiles[i]
            tile_coordinate = self.tiles_coordinates[i]
            xmin, ymin = self.get_tile_cordinates(tile_coordinate[0], tile_coordinate[1])
            xmax, ymax = self.get_tile_cordinates(tile_coordinate[0] + 1, tile_coordinate[1] + 1)

            x1, y1 = self.transform(xmin, ymin) # transform the points for both the 2d and transform_perspective view
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


    def check_ship_collision_with_tile(self, tile_x, tile_y):   # Are the corners of the ship on a tile
        xmin, ymin = self.get_tile_cordinates(tile_x, tile_y)
        xmax, ymax = self.get_tile_cordinates(tile_x + 1, tile_y + 1)

        pos_x, pos_y = self.ship_coordinates[1][0], self.ship_coordinates[1][1] - (self.SHIP_HEIGHT * self.height)/2   # If the center point goes off screen, then the game ends
        return xmin <= pos_x <= xmax and ymin <= pos_y <= ymax

    def check_ship_collision(self):
        for i in range(0, len(self.ship_coordinates)):
            tile_x, tile_y = self.tiles_coordinates[i]
            if tile_y > self.current_y_loop + 1:
                return False
            if self.check_ship_collision_with_tile(tile_x, tile_y):
                return True
        return False



class GalaxyApp(App):
    pass


GalaxyApp().run()