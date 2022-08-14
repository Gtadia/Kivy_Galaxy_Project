# The Galaxy Project
from kivy.app import App
from kivy.graphics import Color
from kivy.graphics import Line
from kivy.properties import NumericProperty
from kivy.uix.widget import Widget

class MainWidget(Widget):
    perspective_point_x = NumericProperty(0) # creating a variable that can be accessed inside of the .kv file
    perspective_point_y = NumericProperty(0) # creating a variable that can be accessed inside of the .kv file

    Num_of_Vertical_Lines = 7
    Vertical_Lines_Spacing = 0.1
    vertical_lines = []

    def __init__(self, **kwargs):
        super(MainWidget, self).__init__(**kwargs)
        # print("INIT W: " + str(self.width), "H: " + str(self.height)) # only runs on the initial execution of the code (Also, it returns the size of the window as (100, 100) but that's incorrect)
        # self.init_vertical_lines()    # This doesn't position the line in the middle because we call this function within the __init__ function, which makes it our parent function. Because we are getting the width and height from the parent function and the parent function's default size is 100 by 100, it's not lined up.
        self.init_vertical_lines()      # The "update_vertical_lines" function will just change the points (and not touch the "init_vertical_lines")   and the "init_vertical_lines" function will create/initialize the code

    def on_parent(self, widget, parent):  # These functions are all attributes to the widget in the kivy file
        # print("ON PARENT W: " + str(self.width), "H: " + str(self.height)) # the same thing as the "INIT" print statement in __init__()
        pass

    def on_size(self, *args):  # This function is an attribute in the kivy file
        print("ON SIZE W: " + str(self.width), "H: " + str(self.height)) # This not only continuously provide the the size data, it's also accurate

        """The two following lines of code are commented out because we're going to try to do the same thing these 
        lines of code achieved inside of the .kv file"""
        # self.perspective_point_x = self.width/2
        # self.perspective_point_y = self.height * 0.75 # because the data continuously changes and is accurate, we can make these variables get updated here

        # self.init_vertical_lines()    # If we instead called this function inside of on_size (or that it runs everytime that the size of the window changse), the previous lines won't dissappear

        # Instead, what we can do is to call a separate function that is specifically meant to update our init_vertical_lines function
        self.update_vertical_lines()    # This function will just change the points (and not touch the "init_vertical_lines")   and the "init_vertical_lines" function will create/initialize the code

    def on_perspective_point_x(self, widget, value):  # We created a new function ==> new attribute
        # This function will automatically be called when the value it's property, "perspective_point_x", changes
            # value is the new value of "perspective_point_x"
        print("PX: " + str(value))

    def on_perspective_point_y(self, widget, value):
        print("PY: " + str(value)) # on_perspective_point_x and y automatically updates

    """
    Anything with "on_" is run when the property of that attribute (such as the attribute of the "parent" of the
    "size" of the window or custom attributes (such as "perspective_point_x" and "perspective_point_y")
        
        If the values of these attributes change, their "on_" functions will execute
    """


    """
    VERTICAL LINES 
    """
    def init_vertical_lines(self):
        """Initialize the lines"""
        with self.canvas:
            Color(1, 1, 1)
            # self.vertical_line = Line(points=[100, 0, 100, 100])   # This doesn't position the line in the middle because we call this function within the __init__ function, which makes it our parent function. Because we are getting the width and height from the parent function and the parent function's default size is 100 by 100, it's not lined up.
            for i in range(0, self.Num_of_Vertical_Lines):
                self.vertical_lines.append(Line()) # Initializes all the different lines (and declared within the "update_vertical_line" function).

    def update_vertical_lines(self):
        center_x = int(self.width/2)
        # self.vertical_line.points = [center_x, 0, center_x, 100]
        # You can't change the values in the list one by one because if you just update the list, it won't trigger the "on_line" code somewhere in the kivy library and it won't actually update the display. If you want to update the display, you have to completely give a new list/change the entire variable with a new list.
        # self.line.points[0] = int(self.width/2)

        current_line_num = -int(self.Num_of_Vertical_Lines/2) # number of lines on each half.
        spacing = self.Vertical_Lines_Spacing * self.width  # the spacing between each line

        for num in range(0, self.Num_of_Vertical_Lines):
            line_x = int(center_x + current_line_num * spacing)
            self.vertical_lines[num].points = [line_x, 0, line_x, self. height]
            current_line_num += 1   # moves onto the next line



# The class that creates the "App"
class GalaxyApp(App):
    pass

GalaxyApp().run()