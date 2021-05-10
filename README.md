&#9817; Ricochet Robot Modelization - Python Implementaton
=======================

[Ricochet Robot](https://en.wikipedia.org/wiki/Ricochet_Robot) is a puzzle board game designed by Alex RANDOLPH in 1999. 

Because of the game's concept, it is an interesting playground for optimization algorithm. 
This package is a Python implementation of the game's modelization.


Example
-----

```python
import ricochetrobot as rr
el = rr.elements

board = el.Board.from_quadrant(
    rr.quadrant.BLUE_1,
    rr.quadrant.RED_1,
    rr.quadrant.GREEN_1,
    rr.quadrant.YELLOW_1,
)
state = rr.gamestate.GameState.construct_from_board(
    board=board,
    robots=frozenset([
        (el.Coordinate(3, 7), el.Robot('RED')),
        (el.Coordinate(2, 8), el.Robot('GREEN')),
        (el.Coordinate(0, 2), el.Robot('BLUE')),
        (el.Coordinate(15, 14), el.Robot('YELLOW'))
    ]),
    goal=el.Symbol('RED', 'STAR')
)

state = state.act(('RIGHT', 'RED'))
state = state.act(('UP', 'RED'))
state = state.act(('RIGHT', 'GREEN'))
state = state.act(('DOWN', 'RED'))
state = state.act(('RIGHT', 'RED'))
state = state.act(('DOWN', 'RED'))
state = state.act(('LEFT', 'RED'))
print(state.goal_achieved())
```

Installation
-----

This package requires no dependencies.
You can install ricochetrobot using setup.py if you have downloaded the source package locally:

```bash
$ python setup.py build
$ sudo python setup.py install
```

or with pip

```bash
$ pip install .
```

To Do
-----

-   HTML Render
-   A* solver
-   Improve logging
-   Add docstring
-   Add annotations
-   Import all quadrant
-   Upload to PyPI

Pull requests are encouraged!
