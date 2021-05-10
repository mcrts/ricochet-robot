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
        (el.Coordinate(12, 4), el.Robot('GREEN')),
        (el.Coordinate(14, 4), el.Robot('BLUE')),
        (el.Coordinate(0, 2), el.Robot('YELLOW'))
    ]),
    el.Symbol('RED', 'STAR')
)

solver = rr.solver.AStarSolver(gs)
start_state, end_state, tree = solver.solve()
print('Solved in {} steps !'.format(len(tree)))

path = solver.compute_path(end_state)
path = list(map(lambda x: (x[0].hex(), x[1], x[2].hex()), path))
print('Optimal path use {} steps !'.format(len(path)))
pprint.pprint(path, width=160)

state = gs
for _, action, _ in path:
    new_state = state.act(action)
    state = new_state
print(state.goal_achieved())
