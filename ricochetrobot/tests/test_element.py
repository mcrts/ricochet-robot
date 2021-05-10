from .. import elements as el


class TestCoordinate:
    def test_translate_to10_10(self):
        c = el.Coordinate(0, 0)
        v = (10, 10)
        assert c.translate(v) == el.Coordinate(10, 10)

    def test_rotate_90(self):
        c = el.Coordinate(1, 0)
        a = 90
        assert c.rotate(a) == el.Coordinate(0, 1)

    def test_rotate_minus90(self):
        c = el.Coordinate(1, 0)
        a = -90
        assert c.rotate(a) == el.Coordinate(0, -1)

    def test_rotate_minus90_on_decimal_value(self):
        c = el.Coordinate(0.5, 0)
        a = -90
        assert c.rotate(a) == el.Coordinate(0, -0.5)


class TestSymbol:
    def test_valdiate(self):
        assert el.Symbol(None, 'VORTEX').validate() is True
        assert el.Symbol(None, 'STAR').validate() is False
        assert el.Symbol('GREEN', 'STAR').validate() is True
        assert el.Symbol('GREEN', 'VORTEX').validate() is False


class TestQuadrant:
    def test_walls_in(self):
        q = el.BoardQuadrant(
            walls=frozenset([el.Coordinate(0, 0)]),
            symbols=frozenset([])
        )
        assert el.Coordinate(0, 0) in q.walls

    def test_symbols_in(self):
        q = el.BoardQuadrant(
            walls=frozenset([el.Coordinate(0, 0)]),
            symbols=frozenset([(el.Coordinate(2, 0), el.Symbol('RED', 'SUN'))])
        )
        assert el.Coordinate(0, 0) in q.walls

    def test_translate(self):
        q = el.BoardQuadrant(
            walls=frozenset([el.Coordinate(0, 0)]),
            symbols=frozenset([(el.Coordinate(2, 0), el.Symbol('RED', 'SUN'))])
        )
        q_res = q.translate((1, 0))

        symbols = frozenset([(el.Coordinate(3, 0), el.Symbol('RED', 'SUN'))])
        assert q_res.walls == frozenset([el.Coordinate(1, 0)])
        assert q_res.symbols == symbols

    def test_rotate(self):
        q = el.BoardQuadrant(
            walls=frozenset([el.Coordinate(1, 0)]),
            symbols=frozenset([(el.Coordinate(2, 0), el.Symbol('RED', 'SUN'))])
        )
        q_res = q.rotate(90)
        symbols = frozenset([(el.Coordinate(0, 2), el.Symbol('RED', 'SUN'))])
        assert q_res.walls == frozenset([el.Coordinate(0, 1)])
        assert q_res.symbols == symbols

    def test_orient(self):
        q = el.BoardQuadrant(
            walls=frozenset([el.Coordinate(1, 0)]),
            symbols=frozenset([(el.Coordinate(2, 0), el.Symbol('RED', 'SUN'))])
        )
        q_res = q.orient('UP_LEFT')
        symbols = frozenset([(el.Coordinate(-1, 2), el.Symbol('RED', 'SUN'))])
        assert q_res.walls == frozenset([el.Coordinate(-1, 1)])
        assert q_res.symbols == symbols
