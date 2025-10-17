from enum import Enum


class SlidingDirection(Enum):
    DOWN = (0, -1)
    LEFT = (1, 0)
    UP = (0, 1)
    RIGHT = (-1, 0)

    @property
    def delta(self):
        return self.value