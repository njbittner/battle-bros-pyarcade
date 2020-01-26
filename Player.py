import arcade
from arcade.draw_commands import draw_texture_rectangle
from constants import *
from arcade import sound
from AnimationBundle import build_animations_registry


PLAYER_2_KEYMAP = dict(
    UP=arcade.key.UP,
    DOWN=arcade.key.DOWN,
    LEFT=arcade.key.LEFT,
    RIGHT=arcade.key.RIGHT,
    ATTACK=arcade.key.O,
    BLOCK=arcade.key.P
)

PLAYER_1_KEYMAP = dict(
    UP=arcade.key.W,
    DOWN=arcade.key.S,
    LEFT=arcade.key.A,
    RIGHT=arcade.key.D,
    ATTACK=arcade.key.X,
    BLOCK=arcade.key.C
)
PLAYER_COLORS = [arcade.color.BLUE, arcade.color.PURPLE]


PLAYER_KEYMAPS=[PLAYER_1_KEYMAP, PLAYER_2_KEYMAP]
class Player(object):
    """
    Image of sprite
    location
    dimensions

    Health
    Attack_timer = -1
    """
    def __init__(self, center_x: int, center_y: int, width: int, height: int, player_idx: int, character='nate'):
        self.center_x = center_x
        self.center_y = center_y
        self.change_y = 0
        self.height = height
        self.width = width
        self.playerIdx = player_idx
        self.keymap = PLAYER_KEYMAPS[player_idx]
        self.color = PLAYER_COLORS[player_idx]
        self.health = 100
        self.level_state = LevelStates.medium
        self.character_face_direction = self.playerIdx  # TODO
        self.game_over = False

        # Movement
        self.left_down = False
        self.right_down = False

        # Counters
        self.block_counter = 0
        self.attack_counter = 0
        self.hit_counter = 0

        # start
        self.state = 'start'

        # load textures
        self.animations_registry = build_animations_registry(character)
        self.animation_bundle = self.animations_registry[self.state]
        self.animation = self.animation_bundle.random_animation()
        self.default_animation = self.animations_registry[('medium', 'idle')].random_animation()
        self.cur_texture_counter = 0
        self.texture = self.animation.get_frame(self.cur_texture_counter, self.character_face_direction)
        self.character = character

        # sounds
        self.hit_sound = sound.load_sound(os.path.join(SOUND_ROOT, "default/hit/hit1.wav"))
        self.block_sound = sound.load_sound(os.path.join(SOUND_ROOT, "default/block/block.wav"))
        self.miss_sound = sound.load_sound(os.path.join(SOUND_ROOT, "default/miss/swoosh-43.wav"))
        self.jump_sound = sound.load_sound(os.path.join(SOUND_ROOT, "default/jump/SFX_Jump_50.wav"))


    @property
    def alive(self):
        return self.health > 0

    def _reset_counters(self):
        self.block_counter = 0
        self.cur_texture_counter = 0
        self.attack_counter = 0
        self.hit_counter = 0

    def on_keypress(self, key, modifiers):
        # blocking pre-empts everything else. If you are blocking you can't start attacking
        # if you are attacking and you press block, you stop attacking.
        if key == self.keymap['BLOCK']:
            self._reset_counters()
            self.block_counter = BLOCK_TOTAL_TIME
        # pressing up causes a jump
        if key == self.keymap['UP'] and self.center_y <= Y_BASELINE + JUMP_FUDGE:
            self._reset_counters()
            self.change_y = JUMP_SPEED
            sound.play_sound(self.jump_sound)
        # down key causes crouching, if not already in the air
        elif key == self.keymap['DOWN']:
            self._reset_counters()
            self.level_state = LevelStates.low

        # you can be moving left and right no matter what, except when blocking
        elif key == self.keymap['LEFT'] and not self.block_counter:
            self.left_down = True
        elif key == self.keymap['RIGHT'] and not self.block_counter:
            self.right_down = True

        # can start an attack if one is not already in progress and you aren't blocking
        elif key == self.keymap['ATTACK'] and not self.attack_counter and not self.block_counter:
            self.attack_counter = ATTACK_TIME

    def on_key_release(self, key, modifiers):
        if key == self.keymap['DOWN']:
            self.level_state = LevelStates.medium
        elif key == self.keymap['LEFT']:
            self.left_down = False
        elif key == self.keymap['RIGHT']:
            self.right_down = False
        elif key == self.keymap['BLOCK']:
            self.block_counter = 0

    @property
    def change_x(self):
        if self.right_down:
            if self.left_down:
                return 0
            else:
                return MOVEMENT_SPEED
        elif self.left_down:
            return -1 * MOVEMENT_SPEED
        return 0

    def update_initial(self, dir):
        if dir:
            if self.playerIdx == 0:
                self.character_face_direction = 1
            else:
                self.character_face_direction = 0
        else:
            if self.playerIdx == 0:
                self.character_face_direction = 0
            else:
                self.character_face_direction = 1
        # Move the player
        if self.alive and not self.game_over:
            self.center_x += self.change_x
            # See if the player hit the edge of the screen. If so, change direction
            if self.center_x < self.width:
                self.center_x = self.width

            if self.center_x > SCREEN_WIDTH - self.width:
                self.center_x = SCREEN_WIDTH - self.width

        self.center_y = max(Y_BASELINE, self.center_y + self.change_y)
        if self.center_y > Y_BASELINE:
            self.change_y -= GRAV_CONSTANT

        # Update Counters
        if self.attack_counter:
            self.attack_counter -= 1
        elif self.hit_counter:
            self.hit_counter -= 1
        elif self.block_counter:
            self.block_counter -= 1

    def hit_update(self, other):
        # if you're crouching and they're not, then you don't have to be blocking
        if self.level_state == LevelStates.low:
            if not other.level_state == LevelStates.low:
                sound.play_sound(self.miss_sound)
                return
        # you're not crouching, or you and they both are, but you're blocking
        if 0 < self.block_counter <= BLOCK_ACTIVE_TIME:
            sound.play_sound(self.block_sound)
            return
        # you're hit-able and not blocking.
        if not self.hit_counter:
            sound.play_sound(self.hit_sound)
            self.hit_counter = HIT_RECOVER_TIME
            back_direction = -1 if self.character_face_direction else 1
            self.center_x -= back_direction*KNOCKBACK_DISTANCE
            self.health -= HIT_DAMAGE
            self.block_counter = 0

    def render_healthbar(self):
        if self.playerIdx == 0:
            HEALTHBAR_X = HEALTHBAR_WIDTH//2 + 10
            arcade.draw_text(self.character, HEALTHBAR_X, SCREEN_HEIGHT - 40,
                             self.color, font_size=30, anchor_x="center")
            arcade.draw_rectangle_filled(center_x=HEALTHBAR_X, center_y=SCREEN_HEIGHT-HEALTHBAR_HEIGHT//2 - HEALTHBAR_Y_OFFSET, width=HEALTHBAR_WIDTH, height=HEALTHBAR_HEIGHT, color=arcade.color.BLACK)
            arcade.draw_rectangle_filled(center_x=HEALTHBAR_X, center_y=SCREEN_HEIGHT-HEALTHBAR_HEIGHT//2 - HEALTHBAR_Y_OFFSET, width=((HEALTHBAR_WIDTH-HEALTHBAR_PADDING)*self.health/100)//1, height=HEALTHBAR_HEIGHT-HEALTHBAR_PADDING, color=arcade.color.GREEN)
        else:
            HEALTHBAR_X = SCREEN_WIDTH - (HEALTHBAR_WIDTH//2+10)
            arcade.draw_text(self.character, HEALTHBAR_X, SCREEN_HEIGHT - 40,
                             self.color, font_size=30, anchor_x="center")
            arcade.draw_rectangle_filled(center_x=HEALTHBAR_X, center_y=SCREEN_HEIGHT-HEALTHBAR_HEIGHT//2 - HEALTHBAR_Y_OFFSET, width=HEALTHBAR_WIDTH, height=HEALTHBAR_HEIGHT, color=arcade.color.BLACK)
            arcade.draw_rectangle_filled(center_x=HEALTHBAR_X, center_y=SCREEN_HEIGHT-HEALTHBAR_HEIGHT//2 - HEALTHBAR_Y_OFFSET, width=((HEALTHBAR_WIDTH-HEALTHBAR_PADDING)*self.health/100)//1, height=HEALTHBAR_HEIGHT-HEALTHBAR_PADDING, color=arcade.color.GREEN)

    def update_texture(self, cur_state, next_state):
        if cur_state == next_state:
            self.cur_texture_counter += 1
            self.texture = self.animation.get_frame(self.cur_texture_counter, self.character_face_direction)
        else:
            # Reset animation counter
            # Change animation to one indexed by new state
            self.cur_texture_counter = 0
            try:
                self.animation = self.animations_registry[next_state].random_animation()
            except IndexError:
                self.animation = self.default_animation
            self.texture = self.animation.get_frame(self.cur_texture_counter, self.character_face_direction)

    def update_animation(self):
        if self.state == 'start':
            self.update_texture(self.state, self.state)
        elif self.game_over:
            if self.alive:
                new_state = "win"
                self.update_texture(self.state, new_state)
            else:
                new_state = "lose"
                self.update_texture(self.state, new_state)
            self.state = new_state
        else:
            # level state
            if self.center_y > Y_BASELINE:
                level_state = "high"
            else:
                level_state = self.level_state.name

            # action state
            if self.hit_counter:
                action_state = 'hit'
            elif self.block_counter:
                action_state = 'block'
            elif self.attack_counter:
                action_state = "attack"
            elif self.change_x !=0:
                action_state = 'movement'
            else:
                action_state = 'idle'

            new_state = (level_state, action_state)
            self.update_texture(self.state, new_state)
            self.state = new_state

    def draw(self, debug=False):
        if debug:
            if self.hit_counter:
                color = arcade.color.RED
            elif self.attack_counter:
                color = arcade.color.GREEN
            elif self.block_counter:
                if self.block_counter <= BLOCK_ACTIVE_TIME:
                    color = arcade.color.PINK
                else:
                    color = arcade.color.ORANGE
            else:
                color = arcade.color.BLUE

            if self.level_state == LevelStates.low and self.center_y == Y_BASELINE:
                arcade.draw_rectangle_filled(self.center_x, self.center_y, self.width, self.height//2, color)
            else:
                arcade.draw_rectangle_filled(self.center_x, self.center_y, self.width, self.height, color)

        # Update Textures
        self.update_animation()

        draw_texture_rectangle(self.center_x, self.center_y,
                               self.width*4, self.height, self.texture)
        self.render_healthbar()
