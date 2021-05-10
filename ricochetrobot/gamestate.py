from collections import namedtuple
import itertools as it
import json
import hashlib

from . import elements as el


class GameState(namedtuple('GameState', 'walls symbols robots goal')):
    directions = set(['UP', 'DOWN', 'LEFT', 'RIGHT'])
    direction_map = {
        'UP': (0, 1),
        'DOWN': (0, -1),
        'LEFT': (-1, 0),
        'RIGHT': (1, 0)
    }
    colors = set(['RED', 'BLUE', 'GREEN', 'YELLOW'])

    def __init__(self, walls, symbols, robots, goal):
        self.walls_map = dict(map(lambda x: (x[1], x[0]), walls))
        self.symbols_map = dict(map(lambda x: (x[1], x[0]), symbols))
        self.robots_map = dict(map(lambda x: (x[1], x[0]), robots))

    @classmethod
    def construct(cls, walls, symbols, robots, goal):
        return cls(walls, symbols, robots, goal)

    @classmethod
    def construct_from_board(cls, board, robots, goal):
        return cls(board.walls, board.symbols, robots, goal)

    def actions(self):
        return it.product(self.directions, self.colors)

    def goal_achieved(self):
        if self.goal == el.Symbol(None, 'VORTEX'):
            res = self.symbols_map[self.goal] in self.robots_map.values()
        else:
            robot = el.Robot(self.goal.color)
            res = self.robots_map[robot] == self.symbols_map[self.goal]
        return res

    def asdict(self):
        data = {
            'walls': sorted(tuple(self.walls)),
            'symbols': sorted(tuple(self.symbols)),
            'robots': sorted(tuple(self.robots)),
            'goal': self.goal
        }
        return data

    @classmethod
    def fromdict(cls, data):
        walls = set(map(
            lambda x: el.Coordinate(x[0], x[1]), data['walls']
        ))
        symbols = set(map(
            lambda x: (
                el.Coordinate(x[0][0], x[0][1]),
                el.Symbol(x[1][0], x[1][1])
            ),
            data['symbols']
        ))
        robots = set(map(
            lambda x: (
                el.Coordinate(x[0][0], x[0][1]),
                el.Robot(x[1][0])
            ),
            data['robots']
        ))
        goal = el.Symbol(data['goal'][0], data['goal'][1])
        return cls(walls, symbols, robots, goal)

    def json(self):
        return json.dumps(self.asdict())

    @classmethod
    def json_loads(cls, jsonstring):
        data = json.loads(jsonstring)
        return cls.fromdict(data)

    def hex(self):
        return hashlib.sha1(self.json().encode('utf-8')).hexdigest()

    def act(self, action):
        direction, color = action
        vector_x, vector_y = self.direction_map[direction]
        robot = el.Robot(color)
        robot_pos = self.robots_map[robot]

        wall = el.Coordinate(
            x=(robot_pos.x + vector_x / 2),
            y=(robot_pos.y + vector_y / 2)
        )
        next_robot_pos = el.Coordinate(
            x=(robot_pos.x + vector_x),
            y=(robot_pos.y + vector_y)
        )
        while (
            (wall not in self.walls)
            and (next_robot_pos not in self.robots_map.values())
        ):
            robot_pos = el.Coordinate(
                x=(robot_pos.x + vector_x),
                y=(robot_pos.y + vector_y)
            )
            next_robot_pos = el.Coordinate(
                x=(robot_pos.x + vector_x),
                y=(robot_pos.y + vector_y)
            )
            wall = el.Coordinate(
                x=(robot_pos.x + vector_x / 2),
                y=(robot_pos.y + vector_y / 2)
            )

        robots = self.robots.difference(set([(self.robots_map[robot], robot)]))
        robots = robots.union(set([(robot_pos, robot)]))

        new_state = self.construct(
            walls=self.walls,
            symbols=self.symbols,
            robots=robots,
            goal=self.goal
        )
        return new_state
