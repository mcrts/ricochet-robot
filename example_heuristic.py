import pprint

import ricochetrobot as rr
el = rr.elements

board = el.Board.from_quadrant(
    rr.quadrant.BLUE_1,
    rr.quadrant.RED_1,
    rr.quadrant.GREEN_1,
    rr.quadrant.YELLOW_1,
)
gs = rr.gamestate.GameState.construct_from_board(
    board,
    frozenset([
        (el.Coordinate(3, 7), el.Robot('RED')),
        (el.Coordinate(2, 8), el.Robot('GREEN')),
        (el.Coordinate(0, 2), el.Robot('BLUE')),
        (el.Coordinate(15, 14), el.Robot('YELLOW'))
    ]),
    el.Symbol('RED', 'STAR')
)

heatmap = rr.solver.Heuristic.heatmap(gs)
print(rr.solver.Heuristic.heuristic_heatmap(heatmap, gs))
