from collections import OrderedDict

__all__ = ['directions', 'direction_vectors']

directions = OrderedDict([
    ("left", (-1, 0)),
    ("up", (0, 1)),
    ("right", (1, 0)),
    ("down", (0, -1))
])

direction_vectors = list(directions.values())
