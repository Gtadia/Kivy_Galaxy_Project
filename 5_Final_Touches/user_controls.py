from kivy import platform
from kivy.uix.relativelayout import RelativeLayout

"""Touch Screen Controls"""
def on_touch_down(self, touch):
    # Because the game moves the ship when we touch the start menu button, we can address this issue by gathering touch data only after the game has started
    if not self.state_game_over and self.state_game_has_started:
        if touch.x < self.width / 2:
            self.current_SPEED_X = self.SPEED_X
        else:
            self.current_SPEED_X = -1 * self.SPEED_X

    # return super(MainWidget, self).on_touch_down(touch)   # This prevents touch functionality from impacting other widgets (such as the menu)
    return super(RelativeLayout, self).on_touch_down(touch) # We are instead going to give this touch functionality to RelativeLayout because we can't import MainWidget (because we're already importing user_controls in MainWidget)


def on_touch_up(self, touch):
    self.current_SPEED_X = 0


"""Keyboard Controls"""
def keyboard_closed(self):
    if self.desktop():
        self._keyboard.unbind(on_key_down=self._on_keyboard_down)
        self._keyboard.unbind(on_key_up=self._on_keyboard_up)
        self._keyboard = None


def is_desktop(self):
    return platform in ("linux", "win", "macos")


def on_keyboard_down(self, keyboard, keycode, text, modifiers):
    if keycode[1].lower() == "left" or keycode[1].lower() == "a":
        self.current_SPEED_X = self.SPEED_X
    elif keycode[1] == "right" or keycode[1] == "d":
        self.current_SPEED_X = -1 * self.SPEED_X
    return True


def on_keyboard_up(self, keyboard, keycode):
    self.current_SPEED_X = 0
    return True