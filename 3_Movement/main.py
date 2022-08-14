# The Galaxy Project
"""Used to set the size of the window"""
from kivy import platform
from kivy.config import Config
Config.set('graphics', 'width', '900')      # The configurations must be set before any other imports/code
Config.set('graphics', 'height', '400')


from kivy.app import App
from kivy.core.window import Window
from kivy.graphics import Color
from kivy.graphics import Line
from kivy.properties import NumericProperty, Clock
from kivy.uix.widget import Widget


class MainWidget(Widget):
    perspective_point_x = NumericProperty(0)
    perspective_point_y = NumericProperty(0)

    # Vertical lines
    Num_of_Vertical_Lines = 10
    Vertical_Lines_Spacing = 0.25
    vertical_lines = []

    # Horizontal lines
    num_of_horizontal_lines = 6
    horizontal_lines_spacing = 1/num_of_horizontal_lines
    horizontal_lines = []

    # Vertical movement     (By moving the horizontal lines, we are given the illusion of moving vertically forwards)
    current_offset_y = 0
    SPEED = 3

    # Horizontal movement   (By moving the vertical lines, we are given the illusion of moving horizontally/to the left and to the right)
    SPEED_X = 150
    current_SPEED_X = 0
    current_offset_x = 0


    def __init__(self, **kwargs):
        super(MainWidget, self).__init__(**kwargs)

        self.init_vertical_lines()
        self.init_horizontal_lines()

        self._keyboard = Window.request_keyboard(self.keyboard_closed, self)   # Import "Window" from "kivy.core.window"
        self._keyboard.bind(on_key_down=self.on_keyboard_down)
        self._keyboard.bind(on_key_up=self.on_keyboard_up)

        Clock.schedule_interval(self.update, 1.0 / 60.0)    # Imported from the "Kivy.properties" and it executes a function in a regular time interval     # Make sure the clock schedule occurs AFTER everything else has been initialized

    def on_parent(self, widget, parent):
        pass

    def on_size(self, *args):
        """
        The update_vertical & _horizontal lines functions are not needed in "on_size" anymore because we're already going to have to update them in the "update" function.
        """
        # self.update_vertical_lines()
        # self.update_horizontal_lines()
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

    def update_vertical_lines(self):
        center_x = int(self.width/2)

        current_line_num = -int(self.Num_of_Vertical_Lines/2) + 0.5
        spacing = self.Vertical_Lines_Spacing * self.width

        for num in range(0, self.Num_of_Vertical_Lines):
            # line_x = int(center_x + current_line_num * spacing)
            line_x = int(center_x + current_line_num * spacing) - self.current_offset_x     # We are going to subtract by an offset on the vertical lines to give the illusion of moving left and right

            x1, y1 = self.transform(line_x, 0)
            x2, y2 = self.transform(line_x, self.height)

            self.vertical_lines[num].points = [x1, y1, x2, y2]
            current_line_num += 1


    def transform(self, x, y):
        return self.transform_perspective(x, y)

    def transform_2D(self, x, y):
        return int(x), int(y)

    def transform_perspective(self, x, y):
        linear_y = self.perspective_point_y * (y / self.height)
        if linear_y > self.perspective_point_y:
            linear_y = self.perspective_point_y

        diff_x = x-self.perspective_point_x
        diff_y = self.perspective_point_y - linear_y
        factor_y = pow(diff_y/self.perspective_point_y, 2)

        transform_x = self.perspective_point_x + diff_x * factor_y
        transform_y = (1-factor_y) * self.perspective_point_y

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

        xmin = center_x + (offset * spacing_x) - self.current_offset_x  # We are going to subtract by an offset on the vertical lines to give the illusion of moving left and right
        xmax = center_x - (offset * spacing_x) - self.current_offset_x  # We are going to subtract by an offset on the vertical lines to give the illusion of moving left and right

        spacing_y = self.horizontal_lines_spacing * self.height

        for i in range(0, self.num_of_horizontal_lines):
            # line_y = i * spacing_y
            line_y = i * spacing_y - (self.current_offset_y)  # We are going to subtract by an offset on the horizontal lines to give the illusion of moving up

            x1, y1 = self.transform(xmin, line_y)
            x2, y2 = self.transform(xmax, line_y)

            self.horizontal_lines[i].points = [x1, y1, x2, y2]




    def update(self, deltaTime):
        """When we use Clock.schedule, it passes in deltaTime as one of the parameters for the function. Remember that."""
        """
        deltaTime:
            So the reason why we need this is because with the "Clock.schedule" method can lead to problems:
                - Some older computers maybe cannot keep up with 60 fps/execute a function every 1/60 seconds. This means that the result would be the device will execute
                the game slower, which in turn makes the game far easier for people using these slower devices.

            To fix this, we're going to use DELTATIME
                So if the delta time/the time that wet by is 2, we're going to travel 2 times the distance (by increasing the speed by 2X)
                 than it normally would in order to make up for the delay.
        """
        time_factor = deltaTime * 60  # if it's 1, then the function ran exactly when it should have but if it's not, the time_factor is going to make up for it by increasing the speed.

        self.update_vertical_lines()
        self.update_horizontal_lines()

        self.current_offset_y += self.SPEED * time_factor     # moves the horizontal lines downwards to give the illusion of moving forwards      # speed scaled by the "time_factor"

        """ 
        We do come across an issue where after a while, we run out of horiziontal lines (all of them go off-screen). 
        We can fix this by looping the horiziontal lines (the lines go back to their starting position after a single 
        line goes offscreen/moves >= the horizontal spacing) 
        """

        spacing_y = self.horizontal_lines_spacing * self.height     # spacing_y from the "update_horizontal_lines()" function

        if self.current_offset_y >= spacing_y:
            self.current_offset_y -= spacing_y  # resetting the lines



        """THE HORIZONTAL MOVEMENT (the same thing as vertical movement but just in the horiziontal direction)"""
        # self.current_offset_x += self.SPEED_X * deltaTime

        # We want to move only when we press on the left and right
        self.current_offset_x += self.current_SPEED_X * deltaTime   #



    """Touch Screen Controls"""
    def on_touch_down(self, touch):
        # This function executes when the left side of the screen is touched
        if touch.x < self.width/2:
            print("left")
            self.current_SPEED_X = -1 * self.SPEED_X
        else:
            print("right")
            self.current_SPEED_X = self.SPEED_X

    def on_touch_up(self, touch):
        # This function executes when what was being pressed is released.
        print("Up")
        self.current_SPEED_X = 0



    """Keyboard Controls"""
    def keyboard_closed(self):
        if self.desktop():      # if it is a desktop, then we can use the keyboard
            self._keyboard.unbind(on_key_down=self._on_keyboard_down)
            self._keyboard.unbind(on_key_up=self._on_keyboard_up)
            self._keyboard = None


    def on_keyboard_down(self, keyboard, keycode, text, modifiers):
        if keycode[1].lower() == "a":
            self.current_SPEED_X = -1 * self.SPEED_X
        elif keycode[1] == "d":     # It doesn't care if "d" is capitalized or not
            self.current_SPEED_X = self.SPEED_X

        # If you press both a and d for even a second, the horizontal movement will just stops for a second.

        return True

    def on_keyboard_up(self, keyboard, keycode):
        self.current_SPEED_X = 0
        return True



    def is_desktop(self):
        """We don't want keyboard inputs on mobile because the onscreen keyboard will show up everytime we play the game and that's going to be annoying"""
        return platform in ("linux", "win", "macos")     # If you import "platform" from "kivy.platform", we can find which operating system you're using.







class GalaxyApp(App):
    pass


GalaxyApp().run()