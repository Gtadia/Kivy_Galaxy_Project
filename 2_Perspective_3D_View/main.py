# The Galaxy Project
from kivy.app import App
from kivy.graphics import Color
from kivy.graphics import Line
from kivy.properties import NumericProperty
from kivy.uix.widget import Widget


class MainWidget(Widget):
    perspective_point_x = NumericProperty(0)
    perspective_point_y = NumericProperty(0)

    Num_of_Vertical_Lines = 14   # If we have a line in the middle, we need an odd num of lines but if we want to center the space in between the lines to be centered, we need an even number of lines
    Vertical_Lines_Spacing = 0.1
    vertical_lines = []

    num_of_horizontal_lines = 6
    horizontal_lines_spacing = 1/num_of_horizontal_lines
    horizontal_lines = []

    def __init__(self, **kwargs):
        super(MainWidget, self).__init__(**kwargs)

        self.init_vertical_lines()
        self.init_horizontal_lines()

    def on_parent(self, widget, parent):
        pass

    def on_size(self, *args):
        print("ON SIZE W: " + str(self.width), "H: " + str(self.height))

        self.update_vertical_lines()
        self.update_horizontal_lines()

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

    def update_vertical_lines(self):
        center_x = int(self.width/2)    # If I wanted the center to be the center in between two lines instead of the center being a line, we can either half of "spacing"

        current_line_num = -int(self.Num_of_Vertical_Lines/2) + 0.5      # or we can add "0.5" so that we multiply by 1.5 spacing (in the for loop below) ("1" from the -int() and the 0.5 from the "0.5")
        spacing = self.Vertical_Lines_Spacing * self.width

        for num in range(0, self.Num_of_Vertical_Lines):
            line_x = int(center_x + current_line_num * spacing) # normally we don't want to multiply be a floating point for coordinates but it won't matter since we're going to convert it into an int anyways

            x1, y1 = self.transform(line_x, 0)
            x2, y2 = self.transform(line_x, self.height)

            self.vertical_lines[num].points = [x1, y1, x2, y2]
            current_line_num += 1


    def transform(self, x, y):
        # This transform function is going to take in the coordinates and then pass those values to be either 2D or transformed (you could just directly pass the value into "transform_prespective" or "transform_2D" but this is here just to make it easier to understand
        return self.transform_perspective(x, y)

    def transform_2D(self, x, y):
        return int(x), int(y)

    def transform_perspective(self, x, y):
        # This is the function that we're going to have to implement
        """
        linear_y:
            * self.perspective_point_y
                - Scaled the y axis down to perspective_point_y
            * y/self.height
                - The percentage of how close to the top we want to go (but scaled down by the scalar *reference up above*)

            - VERTICAL LINES:
                - When y = 0, linear_y = 0
                - When y = self.height, linear_y = perspective_point_y
            - HORIZONTAL LINES:
                - Can be 0% - 100% of the perspective_point_y height
        """
        linear_y = self.perspective_point_y * (y / self.height)   # when y = self.height, this is going to equal to 1, meaning that only "self.perspective_point_y" will exist for the vertical lines. However, for the horizontal lines, the y value is always going to change.
        if linear_y > self.perspective_point_y:
            linear_y = self.perspective_point_y

        diff_x = x-self.perspective_point_x
        diff_y = self.perspective_point_y - linear_y
        factor_y = pow(diff_y/self.perspective_point_y, 2)  # equal to 1 when diff_y == self.perspective_point_y  AND is equal to 0 when diff_y == 0        (SO IT'S ALWAYS GOING TO BE 1 or 0 for the vertical lines) (for the horizontal lines

        transform_x = self.perspective_point_x + diff_x * factor_y  # We multiply diff_x by proportion_y because it's always going to 0 or 1
        transform_y = (1-factor_y) * self.perspective_point_y  # A simplified version of "self.perspective_point_y - factor_y * self.perspective_point_y"



        return int(transform_x), int(transform_y)





    """Horizontal Lines"""
    def init_horizontal_lines(self):
        """initializing the lines"""
        with self.canvas:
            Color(1, 1, 1)
            for i in range(0, self.num_of_horizontal_lines):
                self.horizontal_lines.append(Line())


    def update_horizontal_lines(self):
        center_x = int(self.width/2)
        offset = -int(self.Num_of_Vertical_Lines/2) + 0.5
        spacing_x = self.Vertical_Lines_Spacing * self.width

        xmin = center_x + (offset * spacing_x)
        xmax = center_x - (offset * spacing_x)

        spacing_y = self.horizontal_lines_spacing * self.height

        for i in range(0, self.num_of_horizontal_lines):
            line_y = i * spacing_y

            x1, y1 = self.transform(xmin, line_y)
            x2, y2 = self.transform(xmax, line_y)

            self.horizontal_lines[i].points = [x1, y1, x2, y2]


        """
        The reason why the horizontal lines look so much further apart is because with the perspective mode, the constant spacing in between the lines just makes
        the distance in between the lines look larger.
        
        In other words, Horizontal Line Perspective needs to be adjusted.
        """











class GalaxyApp(App):
    pass


GalaxyApp().run()