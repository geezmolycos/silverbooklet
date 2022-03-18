from itertools import zip_longest

import attr

def grouper(iterable, n, fillvalue=None):
    "Collect data into non-overlapping fixed-length chunks or blocks"
    # grouper('ABCDEFG', 3, 'x') --> ABC DEF Gxx
    args = [iter(iterable)] * n
    return zip_longest(*args, fillvalue=fillvalue)

@attr.s(order=False, frozen=True)
class Vector2D:

    x = attr.ib()
    y = attr.ib()
    
    @property
    def length_sq(self):
        return (self.x**2 + self.y**2)

    @property
    def length(self):
        return (self.x**2 + self.y**2) ** 0.5

    @property
    def manhattan(self):
        return abs(self.x) + abs(self.y)

    @property
    def tuple(self):
        return (self.x, self.y)

    def __neg__(self):
        return type(self)(-self.x, -self.y)

    def __add__(self, other):
        return type(self)(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return self + (-other)

    def __mul__(self, other):
        return type(self)(self.x * other, self.y * other)

    __rmul__ = __mul__

    def dot_product(self, other):
        return self.x * other.x + self.y * other.y

    def is_perpendicular_to(self, other):
        return self.dot_product(other) == 0

    def cross_product(self, other):
        return self.x * other.y - self.y * other.x

    def is_parallel_to(self, other):
        return self.cross_product(other) == 0

    def __iter__(self):
        yield from self.tuple

    def apply_matrix(self, mati, matj):
        return self.x * mati + self.y * matj

    def affine_transform(self, mati, matj, translation):
        return self.apply_matrix(mati, matj) + translation

    def affine_transform_with_origin(self, origin, *args, **kwargs):
        return (self - origin).affine_transform(*args, **kwargs) + origin

class Cardinal:
    NORTH = UP = FORWARD = Vector2D(0, -1)
    EAST = RIGHT = Vector2D(1, 0)
    SOUTH = DOWN = BACKWARD = Vector2D(0, 1)
    WEST = LEFT = Vector2D(-1, 0)

def list_transpose(l):
    return list(map(list, zip(*l)))

@attr.s
class List2D:
    dim = attr.ib()

    def __attrs_post_init__(self):
        self.l = [None] * self.dim.x * self.dim.y

    def flatten(self, index):
        if index.x >= self.dim.x or index.y >= self.dim.y:
            raise IndexError(f"index {index} is out of bound")
        return index.y * self.dim.x + index.x

    def __getitem__(self, key):
        if isinstance(key, Vector2D):
            return self.l[self.flatten(key)]
        elif isinstance(key, slice):
            q = []
            x_range = range(key.start.x, key.stop.x, key.step.x)
            y_range = range(key.start.y, key.stop.y, key.step.y)
            for i in x_range:
                q.extend(self.l[
                    self.flatten(Vector2D(i, key.start.y))
                    :self.flatten(Vector2D(i, key.stop.y))
                    :key.step.y
                ])
            n = List2D(Vector2D(len(x_range), len(y_range)))
            n.l = q
            return n
        else:
            raise KeyError()

    def __setitem__(self, key, value):
        if isinstance(key, Vector2D):
            self.l[self.flatten(key)] = value
        elif isinstance(key, slice):
            x_range = range(key.start.x, key.stop.x, key.step.x)
            y_range = range(key.start.y, key.stop.y, key.step.y)
            for i, j in zip(x_range, count(0)):
                self.l[
                    self.flatten(Vector2D(i, key.start.y))
                    :self.flatten(Vector2D(i, key.stop.y))
                    :key.step.y
                ] = value[Vector2D(j, 0):Vector2D(j, len(y_range))]
                # ".l" is not necessary since __iter__ is implemented
        else:
            raise KeyError()

    def __iter__(self):
        yield from self.l
    
    def copy(self):
        new = type(self)(self.dim)
        new.l = self.l.copy()
        return new


def list_split(l, sep):
    l = iter(l)
    splitted = []
    while True:
        sub = []
        try:
            while (item := next(l)) != sep:
                sub.append(item)
        except StopIteration:
            break
        finally:
            splitted.append(sub)
    return splitted

def list_join(l, sep):
    joined = l[0]
    for sub in l[1:]:
        joined.append(sep)
        joined.extend(sub)
    return joined
    
