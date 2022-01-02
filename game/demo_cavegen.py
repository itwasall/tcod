from typing import Any
from random import choice
from random import randint

import numpy as np
import scipy.signal # type: ignore
from numpy.typing import NDArray


def convolve(tiles: NDArray[Any]) -> NDArray[np.bool_]:
    """Return the next step of the cave generation algorithm

    'tiles' is the input array (0: wall, 1: floor)

    If a 3x3 area around a tile (including itself) has 'wall_rule' number of walls then the tile becomes a wall.
    """
    wall_rule = randint(2,7)
    # Use convolve2d, the 2nd input is a 3x3 ones array
    neighbors: NDArray[Any] = scipy.signal.convolve2d(tiles == 0, [[1,1,1],[1,1,1],[1,1,1]], "same")
    next_tiles: NDArray[np.bool_] = neighbors < wall_rule # Apply the wall rule
    return next_tiles


def show(tiles: NDArray[Any]) -> None:
    """Print out the tiles of an array"""
    floor_types = "".join([".,..,,,     .,,   .,     ,   .,    .,   .,     ,   .,   .,   .,     ,   .,      .,m,   .,     ,   .,    .,   .,     ,   .,   .,   .,     ,   .,      ",
                           "., ,   .,     ,   .,    .,   .,     ,   .,   .,   .,     ,   .,      .,m,   .,     ,   .,    .,   .,     ,   .,   .,   .,     ,   .,      .,m   .,   ",
                           "., ,   .,     ,   .,    .,   .,     ,   .,   .,   .,     ,   .,      .,m,   .,     ,   .,    .,   .,     ,   .,   .,   .,     ,   .,      .,m   .,   ",
                           "., ,   .,     ,   .,    .,   .,     ,   .,   .,   .,     ,   .,      .,m,   .,     ,   .,    .,   .,     ,   .,   .,   .,     ,   .,      .,m   .,   ",
                           "., ,   .,     ,   .,    .,   .,     ,   .,   .,   .,     ,   .,      .,m,   .,     ,   .,    .,   .,     ,   .,   .,   .,     ,   .,      .,m   .,   ",
                           ",   .,    .,   .,     ,   .,   .,   .,     ,   .,      .,m  C"])
    for line in tiles:
        print("".join(f"#{choice(floor_types)}"[int(cell)] for cell in line))


if __name__ == "__main__":
    WIDTH, HEIGHT = 60, 20
    INITIAL_CHANCE = randint(40,50)/100 # Initial wall chance
    CONVOLVE_STEPS = 7
    # 0: wall, 1: floor
    tiles: NDArray[np.bool_] = np.random.random((HEIGHT, WIDTH)) > INITIAL_CHANCE
    for _ in range(CONVOLVE_STEPS):
        tiles = convolve(tiles)
        tiles[[0, -1], :] = 0 # Ensure surrounding wall
        tiles[:, [0, -1]] = 0
    show(tiles)
