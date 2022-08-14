from kivy.uix.relativelayout import RelativeLayout


class MenuWidget(RelativeLayout):
    def on_touch_down(self, touch):
        if self.opacity == 0:   # When the opacity of the menu is 0, the buttons shouldn't work (which is what return False does)
            return False

        return super(RelativeLayout, self).on_touch_down(touch) # If the opacity isn't zero, then the button should relay the information/do an action