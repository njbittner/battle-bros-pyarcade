import glob
from Animation import Animation
import random
from constants import *

"""
character
    stance
        activity

"""
STANCES = {
    "high",
    "medium",
    "low"
}
ACTIVITIES = {
    "attack",
    "block",
    "hit",
    "idle",
    "movement"
}

ACTIVITY_PARAMS = {
    "attack": (ATTACK_TIME, False),
    "block": (BLOCK_INIT_TIME, False),
    "hit": (HIT_RECOVER_TIME, False),
    "idle": (IDLE_ANIMATION_TIME, True),
    "movement": (MOVEMENT_ANIMATION_TIME, True),
    'win': (WIN_TIME, False),
    'lose': (LOSE_TIME, False),
    'start': (START_TIME, False)
}

from constants import SPRITES_ROOT


def build_animations_registry(character):
    character_dir = SPRITES_ROOT + "/" + character
    animations_registry = {}
    # Combations
    for stance in STANCES:
        for activity in ACTIVITIES:
            key = (stance, activity)
            animations_registry[key] = ActivityAnimationBundle(character_dir + '/' + stance, activity)

    # Specials
    animations_registry['win'] = ActivityAnimationBundle(character_dir + '/end', 'win')
    animations_registry['lose'] = ActivityAnimationBundle(character_dir+'/end', 'lose')
    animations_registry['start'] = ActivityAnimationBundle(character_dir, 'start')
    print(animations_registry)
    return animations_registry


class ActivityAnimationBundle(object):
    def __init__(self, stance_path, action):
        print(stance_path)
        self.path = stance_path + "/" + action
        self.sub_dirs = glob.glob(self.path + '/*')
        self.animations = [Animation(x, ACTIVITY_PARAMS[action][0], ACTIVITY_PARAMS[action][1]) for x in self.sub_dirs]

    def random_animation(self):
        return random.choice(self.animations)
