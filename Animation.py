import arcade
import glob
from constants import CHARACTER_SCALING

"""
[x] Animations can either repeat or hold.
"""

def load_texture_pair(filename):
    """
    Load a texture pair, with the second being a mirror image.
    """
    return [
        arcade.load_texture(filename, scale=CHARACTER_SCALING),
        arcade.load_texture(filename, scale=CHARACTER_SCALING, mirrored=True)
    ]


class Animation(object):
    def __init__(self, dirpath, tick_count, repeats):
        self.frame_paths = sorted(glob.glob(dirpath + "/*.png"))
        if not self.frame_paths:
            raise RuntimeError("No frames in '%s'" % dirpath)
        self.textures = [load_texture_pair(x) for x in self.frame_paths]
        self.frame_count = len(self.frame_paths)
        self.tick_count = tick_count
        self.step, self.remainder = divmod(self.tick_count, self.frame_count)
        self.check = self.frame_count * self.step
        self.repeats = repeats

    def get_frame(self, index_count: int, direction: int = 0):
        if index_count > self.check-1 and not self.repeats:
            return self.textures[-1][direction]
        else:
            idx = (index_count // self.step) % self.frame_count
            return self.textures[idx][direction]
