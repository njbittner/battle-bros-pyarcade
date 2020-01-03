import arcade
from Player import Player
import math
import random
from constants import *
import glob

"""
Need to have Start and End ANimation
"""

## MAIN GAME CLASS
class FightView(arcade.View):

    def __init__(self, window):
        """
        :param width: Width of Window
        :param height:  Height of window
        :param title:  Title of game
        """
        # Call the parent class's init function
        super().__init__()

        # Make the mouse disappear when it is over the window.
        # So we just see our object, not the pointer.
        self.window = window
        self.window.set_mouse_visible(False)

        # arcade.set_background_color(arcade.color.ASH_GREY)

        # Create our players
        self.player1 = Player(int(1/8 * SCREEN_WIDTH), Y_BASELINE, BOX_WIDTH, BOX_HEIGHT, 0, character='jason')
        self.player2 = Player(int(7/8 * SCREEN_WIDTH), Y_BASELINE, BOX_WIDTH, BOX_HEIGHT, 1, character='ian')

        # endgame
        self.winner = None

        # background images
        bg_images = glob.glob(os.path.join(BACKGROUND_IMG_ROOT, "*.jpeg"))
        bg_image = random.choice(bg_images)
        self.background_texture = arcade.load_texture(bg_image)

        # Saving recordings
        self.abs_counter = 0

        # background music
        self.enable_bg = True
        songs = glob.glob(os.path.join(MUSIC_ROOT, "*.wav"))
        bg_song = random.choice(songs)
        self.background_music = arcade.load_sound(bg_song)
        if self.enable_bg:
            arcade.play_sound(self.background_music)

        # Do a countdown
        self.countdown_counter = (COUNTDOWN_FROM + 1) * TICKS_PER_COUNTDOWN
        self.countdown_values = range(1, COUNTDOWN_FROM+1)

    def on_key_press(self, key, modifiers):
        if not self.winner and not self.countdown_counter:
            self.player1.on_keypress(key, modifiers)
            self.player2.on_keypress(key, modifiers)

    def on_key_release(self, key, modifiers):
        if not self.winner and not self.countdown_counter:
            self.player1.on_key_release(key, modifiers)
            self.player2.on_key_release(key, modifiers)

    def _update_winner(self):
        if self.player1.health <1:
            self.winner = self.player2
        if self.player2.health <1:
            self.winner = self.player1

        if self.winner and self.enable_bg:
            self.player1.game_over = True
            self.player2.game_over = True
            # self.background_music.player.pause()
            # arcade.stop_sound(self.background_music)

    def on_update(self, delta_time):
        """ Initial Update """

        if self.countdown_counter:
            self.countdown_counter -= 1
            if self.countdown_counter == TICKS_PER_COUNTDOWN:
                self.player1.state = ('medium', 'idle')
                self.player2.state = ('medium', 'idle')
        else:
            self._update_winner()
            if self.player1.center_x < self.player2.center_x:
                dir = 0
            else:
                dir = 1
            self.player1.update_initial(dir)
            self.player2.update_initial(dir)
            # handle hits
            if abs(self.player1.center_x - self.player2.center_x) < STRIKE_DISTANCE:
                if ATTACK_OFFSET < self.player1.attack_counter <= ATTACK_OFFSET + ATTACK_FUDGE:
                    self.player2.hit_update(self.player1)
                if ATTACK_OFFSET < self.player2.attack_counter <= ATTACK_OFFSET + ATTACK_FUDGE:
                    self.player1.hit_update(self.player2)

    def on_draw(self):
        arcade.start_render()

        # Draw background
        arcade.draw_texture_rectangle(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2,
                                      SCREEN_WIDTH, SCREEN_HEIGHT, self.background_texture)
        self.player1.draw()
        self.player2.draw()

        if self.countdown_counter > TICKS_PER_COUNTDOWN:
            arcade.draw_text(f"{self.countdown_values[(self.countdown_counter-TICKS_PER_COUNTDOWN) // TICKS_PER_COUNTDOWN]}", SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2,
                             arcade.color.RED, font_size=120, anchor_x="center", font_name="Utopia", bold=True)
        elif self.countdown_counter:
            arcade.draw_text(FIGHT_MSG,
                             SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2,
                             arcade.color.RED, font_size=120, anchor_x="center", font_name="Utopia", bold=True)
        elif self.winner:
            arcade.draw_text(f"Player {self.winner.playerIdx + 1} WINS!!", SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2,
                             arcade.color.RED, font_size=60, anchor_x="center", font_name="Utopia")


