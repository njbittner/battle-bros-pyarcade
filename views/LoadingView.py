import arcade
from constants import SCREEN_WIDTH, Y_BASELINE, BOX_HEIGHT, BOX_WIDTH
from views.FightView import FightView
import pyglet
from Player import Player


class LoadingView(arcade.View):
    def __init__(self, window: pyglet.window.Window):
        super().__init__()
        self.window = window
        self.idx = 0
        arcade.set_background_color(arcade.color.BLACK)
        self.tick_idx = 0
        self.drawn = False

    def on_draw(self):
        arcade.start_render()
        arcade.draw_text("Loading Characters...", self.window.width/2, self.window.height/2,
                         arcade.color.WHITE, font_size=50, anchor_x="center")
        arcade.draw_text("(May take a moment)", self.window.width/2, self.window.height/2 - 30,
                         arcade.color.WHITE, font_size=30, anchor_x="center")
        self.tick_idx += 1
        self.drawn = True

    def on_update(self, delta_time: float):
        if self.drawn:
            player1 = Player(int(1/8 * SCREEN_WIDTH), Y_BASELINE, BOX_WIDTH, BOX_HEIGHT, 0, character='nate')
            player2 = Player(int(7/8 * SCREEN_WIDTH), Y_BASELINE, BOX_WIDTH, BOX_HEIGHT, 1, character='nate')
            fight_view = FightView(self.window, player1=player1, player2=player2)
            self.window.show_view(fight_view)

