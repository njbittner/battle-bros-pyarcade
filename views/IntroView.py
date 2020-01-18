import arcade
from views.LoadingView import LoadingView
import pyglet

COLORS = [arcade.color.BLACK, arcade.color.RED_BROWN]

class IntroView(arcade.View):
    def __init__(self, window: pyglet.window.Window):
        super().__init__()
        self.window = window
        self.idx = 0

    def on_draw(self):
        self.idx +=1
        arcade.start_render()
        arcade.set_background_color(arcade.color.SLATE_GRAY)
        color =  COLORS[(self.idx // 80) % 2]
        arcade.draw_text("Battle Bros", self.window.width/2, self.window.height/2,
                     color, font_size=50, anchor_x="center")
        arcade.draw_text("Click to begin...", self.window.width/2, self.window.height/2-75,
                     arcade.color.WHITE, font_size=20, anchor_x="center")

    def on_mouse_press(self, _x, _y, _button, _modifiers):
        loading_view = LoadingView(self.window)
        self.window.show_view(loading_view)



