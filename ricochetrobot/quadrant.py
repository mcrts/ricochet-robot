from . import elements as el

EMPTY = el.BoardQuadrant(walls=frozenset(), symbols=frozenset())
BASE = el.BoardQuadrant(
    symbols=frozenset(),
    walls=frozenset([
        el.Coordinate(0.5, 0),
        el.Coordinate(0, 0.5),
        el.Coordinate(7.5, 0),
        el.Coordinate(7.5, 1),
        el.Coordinate(7.5, 2),
        el.Coordinate(7.5, 3),
        el.Coordinate(7.5, 4),
        el.Coordinate(7.5, 5),
        el.Coordinate(7.5, 6),
        el.Coordinate(7.5, 7),
        el.Coordinate(0, 7.5),
        el.Coordinate(1, 7.5),
        el.Coordinate(2, 7.5),
        el.Coordinate(3, 7.5),
        el.Coordinate(4, 7.5),
        el.Coordinate(5, 7.5),
        el.Coordinate(6, 7.5),
        el.Coordinate(7, 7.5),
    ])
)

RED_1 = BASE + el.BoardQuadrant(
    walls=frozenset([
        el.Coordinate(1.5, 0),
        el.Coordinate(4.5, 2),
        el.Coordinate(3.5, 5),
        el.Coordinate(1.5, 5),
        el.Coordinate(2.5, 7),
        el.Coordinate(1, 6.5),
        el.Coordinate(2, 0.5),
        el.Coordinate(3, 4.5),
        el.Coordinate(5, 1.5),
        el.Coordinate(7, 3.5)
    ]),
    symbols=frozenset([
        (el.Coordinate(2, 0), el.Symbol('RED', 'SUN')),
        (el.Coordinate(5, 2), el.Symbol('BLUE', 'STAR')),
        (el.Coordinate(3, 5), el.Symbol('GREEN', 'MOON')),
        (el.Coordinate(1, 6), el.Symbol('YELLOW', 'PLANET'))
    ])
)

GREEN_1 = BASE + el.BoardQuadrant(
    walls=frozenset([
        el.Coordinate(2.5, 1),
        el.Coordinate(5.5, 1),
        el.Coordinate(0.5, 4),
        el.Coordinate(5.5, 6),
        el.Coordinate(1.5, 7),
        el.Coordinate(1, 4.5),
        el.Coordinate(2, 0.5),
        el.Coordinate(5, 6.5),
        el.Coordinate(6, 0.5),
        el.Coordinate(7, 2.5),
    ]),
    symbols=frozenset([
        (el.Coordinate(2, 1), el.Symbol('BLUE', 'PLANET')),
        (el.Coordinate(6, 1), el.Symbol('YELLOW', 'STAR')),
        (el.Coordinate(1, 4), el.Symbol('RED', 'MOON')),
        (el.Coordinate(5, 6), el.Symbol('GREEN', 'SUN')),
    ])
)

YELLOW_1 = BASE + el.BoardQuadrant(
    walls=frozenset([
        el.Coordinate(4.5, 0),
        el.Coordinate(2.5, 1),
        el.Coordinate(5.5, 2),
        el.Coordinate(2.5, 4),
        el.Coordinate(7.5, 6),
        el.Coordinate(3.5, 7),
        el.Coordinate(1, 5.5),
        el.Coordinate(2, 1.5),
        el.Coordinate(3, 3.5),
        el.Coordinate(5, -0.5),
        el.Coordinate(6, 2.5),
        el.Coordinate(7, 4.5),
    ]),
    symbols=frozenset([
        (el.Coordinate(5, 0), el.Symbol(None, 'VORTEX')),
        (el.Coordinate(2, 1), el.Symbol('GREEN', 'PLANET')),
        (el.Coordinate(6, 2), el.Symbol('BLUE', 'MOON')),
        (el.Coordinate(3, 4), el.Symbol('RED', 'STAR')),
        (el.Coordinate(1, 6), el.Symbol('YELLOW', 'SUN')),
    ])
)

BLUE_1 = BASE + el.BoardQuadrant(
    walls=frozenset([
        el.Coordinate(3.5, 2),
        el.Coordinate(1.5, 3),
        el.Coordinate(5.5, 4),
        el.Coordinate(3.5, 5),
        el.Coordinate(3.5, 7),
        el.Coordinate(2, 2.5),
        el.Coordinate(3, 4.5),
        el.Coordinate(4, 2.5),
        el.Coordinate(5, 4.5),
        el.Coordinate(7, 1.5),
    ]),
    symbols=frozenset([
        (el.Coordinate(4, 2), el.Symbol('BLUE', 'SUN')),
        (el.Coordinate(2, 3), el.Symbol('GREEN', 'STAR')),
        (el.Coordinate(3, 5), el.Symbol('YELLOW', 'MOON')),
        (el.Coordinate(5, 4), el.Symbol('RED', 'PLANET')),
    ])
)
