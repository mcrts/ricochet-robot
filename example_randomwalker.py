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
        (el.Coordinate(3, 2), el.Robot('RED')),
        (el.Coordinate(14, 2), el.Robot('GREEN')),
        (el.Coordinate(3, 15), el.Robot('BLUE')),
        (el.Coordinate(15, 14), el.Robot('YELLOW'))
    ]),
    el.Symbol('RED', 'STAR')
)

solver = rr.solver.RandomWalkerSolver(gs, seed=1)
start_state, end_state, history = solver.solve()
print('Solved in {} steps !'.format(len(history)))
path = solver.compute_path(start_state, end_state)
print('Solved in {} steps (trimmed) !'.format(len(path)))

state = gs
for _, action, _ in path:
    new_state = state.act(action)
    state = new_state
print(state.goal_achieved())
