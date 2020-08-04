from collections import namedtuple
import math


class Coordinate(namedtuple('Position', 'x y')):
    @classmethod
    def _translate(cls, e, v):
        dx, dy = v
        return cls(e.x + dx, e.y + dy)

    def translate(self, vector):
        return self._translate(self, vector)

    @classmethod
    def _rotate(cls, e, a):
        r = math.radians(a)
        rcos = math.cos(r)
        rsin = math.sin(r)
        ne = cls(
            round(e.x*rcos - e.y*rsin, 14),
            round(e.x*rsin + e.y*rcos, 14)
        )
        return ne

    def rotate(self, angle):
        return self._rotate(self, angle)


class Symbol(namedtuple('Symbol', 'color symbol')):
    available_colors = set(['RED', 'BLUE', 'GREEN', 'YELLOW', None])
    available_symbols = set(['PLANET', 'SUN', 'STAR', 'MOON', 'VORTEX'])

    def validate(self):
        return (self.color is None) == (self.symbol == 'VORTEX')


class Robot(namedtuple('Robot', 'color')):
    available_colors = set(['RED', 'BLUE', 'GREEN', 'YELLOW'])


class BoardQuadrant(namedtuple('BoardQuadrant', 'walls symbols')):
    _directions = {
            'UP_RIGHT': (0, (0, 0)),
            'UP_LEFT': (90, (-1, 0)),
            'DOWN_LEFT': (180, (-1, -1)),
            'DOWN_RIGHT': (-90, (0, -1)),
        }

    @classmethod
    def construct(cls, walls, symbols):
        return cls(walls, symbols)

    def __add__(self, other):
        walls = self.walls.union(other.walls)
        symbols = self.symbols.union(other.symbols)
        return self.construct(walls, symbols)

    @classmethod
    def _translate(cls, quadrant, v):
        walls = frozenset(
            map(lambda x: x.translate(v), quadrant.walls)
        )
        symbols = frozenset(
            map(lambda x: (x[0].translate(v), x[1]), quadrant.symbols)
        )
        return cls(walls, symbols)

    def translate(self, v):
        return self._translate(self, v)

    @classmethod
    def _rotate(cls, quadrant, a):
        walls = frozenset(map(lambda x: x.rotate(a), quadrant.walls))
        symbols = frozenset(
            map(lambda x: (x[0].rotate(a), x[1]), quadrant.symbols)
        )
        return cls(walls, symbols)

    def rotate(self, a):
        return self._rotate(self, a)

    def orient(self, direction):
        a, v = self._directions[direction]
        return self.rotate(a).translate(v)


class Board(namedtuple('Board', 'walls symbols')):
    center = (8, 8)

    @classmethod
    def from_quadrant(cls, up_right, up_left, down_left, down_right):
        q1 = up_right.orient('UP_RIGHT').translate(cls.center)
        q2 = up_left.orient('UP_LEFT').translate(cls.center)
        q3 = down_left.orient('DOWN_LEFT').translate(cls.center)
        q4 = down_right.orient('DOWN_RIGHT').translate(cls.center)
        walls = q1.walls | q2.walls | q3.walls | q4.walls
        symbols = q1.symbols | q2.symbols | q3.symbols | q4.symbols
        return cls(walls, symbols)
