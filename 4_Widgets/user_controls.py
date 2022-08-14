from kivy import platform

"""Touch Screen Controls"""
def on_touch_down(self, touch):
    if touch.x < self.width / 2:
        self.current_SPEED_X = self.SPEED_X
    else:
        self.current_SPEED_X = -1 * self.SPEED_X


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
    if keycode[1].lower() == "a":
        self.current_SPEED_X = self.SPEED_X
    elif keycode[1] == "d":
        self.current_SPEED_X = -1 * self.SPEED_X
    return True


def on_keyboard_up(self, keyboard, keycode):
    self.current_SPEED_X = 0
    return True