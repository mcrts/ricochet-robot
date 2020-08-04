from .. import quadrant
from .. import gamestate
from .. import elements as el


class TestGameState:
    def setup(self):
        board = el.Board.from_quadrant(
            quadrant.BLUE_1,
            quadrant.RED_1,
            quadrant.GREEN_1,
            quadrant.YELLOW_1,
        )
        self.gs1 = gamestate.GameState.construct_from_board(
            board,
            set([
                (el.Coordinate(3, 2), el.Robot('RED')),
                (el.Coordinate(14, 2), el.Robot('GREEN')),
                (el.Coordinate(3, 15), el.Robot('BLUE')),
                (el.Coordinate(15, 14), el.Robot('YELLOW'))
            ]),
            el.Symbol('RED', 'STAR')
        )
        self.gs2 = gamestate.GameState.construct_from_board(
            board,
            set([
                (el.Coordinate(12, 4), el.Robot('RED')),
                (el.Coordinate(14, 2), el.Robot('GREEN')),
                (el.Coordinate(3, 15), el.Robot('BLUE')),
                (el.Coordinate(15, 14), el.Robot('YELLOW'))
            ]),
            el.Symbol('RED', 'STAR')
        )
        self.gs3 = gamestate.GameState.construct_from_board(
            board,
            set([
                (el.Coordinate(12, 4), el.Robot('RED')),
                (el.Coordinate(14, 2), el.Robot('GREEN')),
                (el.Coordinate(3, 15), el.Robot('BLUE')),
                (el.Coordinate(15, 14), el.Robot('YELLOW'))
            ]),
            el.Symbol(None, 'VORTEX')
        )
        self.gs4 = gamestate.GameState.construct_from_board(
            board,
            set([
                (el.Coordinate(12, 4), el.Robot('RED')),
                (el.Coordinate(14, 2), el.Robot('GREEN')),
                (el.Coordinate(8, 2), el.Robot('BLUE')),
                (el.Coordinate(15, 14), el.Robot('YELLOW'))
            ]),
            el.Symbol(None, 'VORTEX')
        )

    def test_actions(self):
        actions = self.gs1.actions()
        assert ('DOWN', 'BLUE') in set(actions)

    def test_goal_achieved(self):
        assert self.gs1.goal_achieved() is False
        assert self.gs2.goal_achieved() is True

    def test_goal_achieved_vortex(self):
        assert self.gs3.goal_achieved() is False
        assert self.gs4.goal_achieved() is True

    def test_json(self):
        s = self.gs1.json()
        gs = gamestate.GameState.json_loads(s)
        assert gs == self.gs1
        assert gs != self.gs2

    def test_hex(self):
        s = self.gs1.json()
        gs = gamestate.GameState.json_loads(s)
        assert gs.hex() == self.gs1.hex()
        assert gs.hex() != self.gs2.hex()

    def test_act_against_wall(self):
        action = ('DOWN', 'GREEN')
        robot = el.Robot('GREEN')
        res = self.gs1.act(action)
        assert res.robots_map[robot] == el.Coordinate(14, 0)

    def test_act_against_robot(self):
        action = ('UP', 'GREEN')
        robot = el.Robot('GREEN')
        gs = gamestate.GameState.construct(
            walls=self.gs1.walls,
            symbols=self.gs1.symbols,
            robots=set([
                (el.Coordinate(12, 4), el.Robot('RED')),
                (el.Coordinate(14, 2), el.Robot('GREEN')),
                (el.Coordinate(8, 2), el.Robot('BLUE')),
                (el.Coordinate(14, 10), el.Robot('YELLOW'))
            ]),
            goal=self.gs1.goal
        )
        res = gs.act(action)
        assert res.robots_map[robot] == el.Coordinate(14, 9)

    def test_act_dont_move(self):
        action = ('UP', 'GREEN')
        robot = el.Robot('GREEN')
        gs = gamestate.GameState.construct(
            walls=self.gs1.walls,
            symbols=self.gs1.symbols,
            robots=set([
                (el.Coordinate(12, 4), el.Robot('RED')),
                (el.Coordinate(14, 2), el.Robot('GREEN')),
                (el.Coordinate(8, 2), el.Robot('BLUE')),
                (el.Coordinate(14, 3), el.Robot('YELLOW'))
            ]),
            goal=self.gs1.goal
        )
        res = gs.act(action)
        assert res.robots_map[robot] == el.Coordinate(14, 2)
        assert res == gs
