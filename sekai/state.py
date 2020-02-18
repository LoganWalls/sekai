from collections import defaultdict
from math import copysign
from typing import Any, DefaultDict, Optional, Tuple

__all__ = ["State", "SekaiObject"]


class Grid:
    def __init__(self, n_columns: int, n_rows: int, default: Optional[Any] = None):
        self.n_columns: int = n_columns
        self.n_rows: int = n_rows
        self.shape: Tuple[int, int] = (n_columns, n_rows)
        self.content: DefaultDict[DefaultDict[int, None]] = defaultdict(defaultdict)
        self.default = default

    def _bounds_check(self, item):
        if not isinstance(item, tuple):
            raise KeyError('invalid indexing, please use `grid[x, y]`')
        x, y = item
        if (x < 0) or (y < 0) or (x > self.n_columns - 1) or (y > self.n_rows - 1):
            raise IndexError('grid index out of bounds')

    def __getitem__(self, item):
        self._bounds_check(item)
        return self.content[item[1]][item[0]]

    def __setitem__(self, key, value):
        self._bounds_check(key)
        self.content[key[1]][key[0]] = value

    def __delitem__(self, key):
        self._bounds_check(key)
        del self.content[key[1]][key[0]]

    def __iter__(self):
        for y in range(self.n_rows):
            for x in range(self.n_columns):
                o = self.get(x, y, default=None)
                if o:
                    yield o, (x, y)

    def get(self, x, y, default: Optional[Any] = None):
        try:
            return self[x, y]
        except KeyError:
            return default or self.default

    def bounded_coords(self, x: int, y: int) -> Tuple[int, int]:
        """Adjust out-of-bounds coordinates to the nearest valid coordinates.
        :param x: desired x coordinate
        :param y: desired y coordinate
        :return: a tuple containing the adjusted x and y coordinates
        """
        if x < 0:
            x = 0
        elif x > self.n_columns - 1:
            x = self.n_columns - 1

        if y < 0:
            y = 0
        elif y > self.n_rows - 1:
            y = self.n_rows - 1
        return x, y


class State:
    def __init__(self, n_columns: int, n_rows: int, default_tile: Optional = None):
        self.n_columns: int = n_columns
        self.n_rows: int = n_rows
        self.shape: Tuple[int, int] = (n_columns, n_rows)
        self.objects: Grid = Grid(n_columns, n_rows)
        self.tiles: Grid = Grid(n_columns, n_rows, default=default_tile)

        self.reward: float = 0.
        self.terminal_state: bool = False

    def move(self, from_: Tuple[int, int], to: Tuple[int, int]) -> bool:
        """Move an object along a straight path from `from_` to `to`.
        :param from_: a tuple or coordinates (x, y) with the object to be moved
        :param to: a tuple or coordinates (x, y) containing the destination object
        :return: whether or not the move was successful
        """
        if self.terminal_state:
            return False
        x, y = from_
        tx, ty = self.objects.bounded_coords(*to)
        obj = self.objects[x, y]
        while (x != tx) or (y != ty):
            if x != tx:
                x += int(copysign(1, tx - x))
            if y != ty:
                y += int(copysign(1, ty - y))

            destination_tile = self.tiles.get(x, y)
            if destination_tile and not destination_tile.collide(obj, self, x, y):
                return False

            other = self.objects.get(x, y)
            if other and not other.collide(obj, self, x, y):
                return False

        del self.objects[from_]
        self.objects[x, y] = obj
        return True


class SekaiObject(object):
    display = None
    display_bg = None

    def tick(self, state: State, x: int, y: int):
        """Defines behavior at each tick.
        :param state: the current world state
        :param x: the current x coordinate of the object
        :param y: the current y coordinate of the object
        """
        pass

    def collide(self, other, state: State, x: int, y: int) -> bool:
        """Defines behavior when another object collides with this object.
        :param other: the other object which is colliding with this one
        :param state: the current world state
        :param x: the x coordinate of the collision
        :param y: the y coordinate of the collision
        :return: whether or not `other` can remain on this tile
        """
        return True
