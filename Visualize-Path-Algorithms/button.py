from cs1lib import *


class Button:
    def __init__(self, x, y, w, h, text, function):
        self.x = x
        self.y = y
        self.width = w
        self.height = h
        self.text = text
        self.function = function

    def draw(self):
        set_stroke_color(1, 1, 1)
        set_fill_color(.5, .5, .5)
        draw_rectangle(self.x, self.y, self.width, self.height)
        set_stroke_color(0, 0, 0)
        set_font_size(20)
        draw_text(self.text, self.x, self.y + self.height)
        draw_text('test', 100, 100)

    def do(self):
        self.function()

    def __str__(self):
        return self.text
