import logging
import random
import heapq as hq
import math
from collections import defaultdict

from .elements import Coordinate, Robot


class Logger:
    _start_log = "Game Start state : {state}, Goal : {goal}"
    _step_log = "Current state : {current_state}, Action : {action}, New state : {next_state}"
    _end_log = "Game End state : {state}, Goal : {goal}"
    _format = "%(asctime)s | %(name)s:%(process)d | %(message)s"

    def __init__(self, name):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.INFO)
        ch = logging.StreamHandler()
        formatter = logging.Formatter(self._format)
        ch.setFormatter(formatter)
        self.logger.addHandler(ch)

    def log_start(self, state):
        self.logger.info(
            self._start_log.format(
                state=state.hex(),
                goal=state.goal
            )
        )

    def log_step(self, current_state, next_state, action):
        self.logger.info(
            self._step_log.format(
                current_state=current_state.hex(),
                next_state=next_state.hex(),
                action=action
            )
        )

    def log_end(self, state):
        self.logger.info(
            self._end_log.format(
                state=state.hex(),
                goal=state.goal
            )
        )

class Heuristic:
    @staticmethod
    def uniform(state):
        return 0 if state.goal_achieved() else 1
    
    @staticmethod
    def heatmap(state):
        _heatmap = dict()
        goalpos = state.symbols_map[state.goal]
        goalpos = (int(goalpos.x), int(goalpos.y))
        positions = [goalpos]
        _heatmap[goalpos] = 0
        while positions:
            pos = positions.pop(0)
            posx, posy = pos
            h_walls = list(filter(lambda w: w.y == float(posy), state.walls))
            h0 = math.ceil(max(filter(lambda w: w.x < posx, h_walls), key=lambda w: w.x).x)
            h1 = math.ceil(min(filter(lambda w: w.x > posx, h_walls), key=lambda w: w.x).x)
            v_walls = list(filter(lambda w: w.x == float(posx), state.walls))
            v0 = math.ceil(max(filter(lambda w: w.y < posy, v_walls), key=lambda w: w.y).y)
            v1 = math.ceil(min(filter(lambda w: w.y > posy, v_walls), key=lambda w: w.y).y)
            
            cells = [(x, posy) for x in range(h0, h1)] + [(posx, y) for y in range(v0, v1)]
            for c in cells:
                if c not in _heatmap:
                    _heatmap[c] = _heatmap[pos] + 1
                    positions.append(c)
        return _heatmap

    @staticmethod
    def heuristic_heatmap(heatmap, state):
        robot = Robot(state.goal.color)
        pos = state.robots_map[robot]
        return heatmap[pos]


class RandomWalkerSolver:
    name = 'RandomWalker'
    properties = {
        'optimal': False,
        'behavior': 'random'
    }

    def __init__(self, gamestate, seed=None):
        self.initial_gamestate = gamestate
        self._randomizer = random.Random(seed)
        self.history = list()
        self.logger = Logger(self.name)

    def solve(self):
        current_node = self.initial_gamestate
        rand = self._randomizer

        self.logger.log_start(current_node)
        while not current_node.goal_achieved():
            action = rand.choice(sorted(list(current_node.actions())))
            new_node = current_node.act(action)
            self.logger.log_step(current_node, new_node, action)
            current_node = new_node
            self.history.append((current_node, action, new_node))

        self.logger.log_end(current_node)
        return self.initial_gamestate, current_node, self.history

    def compute_path(self, start_node, end_node):
        iterator = iter(self.history)
        path = [next(iterator)]
        for previous_node, action, current_node in iterator:
            if current_node != path[-1][2]:
                path.append((previous_node, action, current_node))
        return path


class BFSSolver:
    name = 'BreathFirstSearch'
    properties = {
        'optimal': True,
        'behavior': 'stochastic'
    }

    def __init__(self, gamestate):
        self.initial_gamestate = gamestate
        self.logger = Logger(self.name)
        self.history = list()
        self.prevtree = dict()

    def solve(self):
        current_node = self.initial_gamestate
        frontier = list()
        discovered = set()

        self.logger.log_start(current_node)
        discovered.add(current_node)
        while not current_node.goal_achieved():
            for action in current_node.actions():
                node = current_node.act(action)
                if node != current_node and node not in discovered:
                    # self.logger.log_step(current_node, node, action)
                    discovered.add(node)
                    frontier.append((current_node, action, node))

            previous_node, action, current_node = frontier.pop(0)
            self.prevtree[current_node] = (previous_node, action)
            self.history.append((previous_node, action, current_node))

        self.logger.log_end(current_node)
        return self.initial_gamestate, current_node, self.history, self.prevtree

    def compute_path(self, start_node, end_node):
        path = []
        current_node = end_node

        while current_node != start_node:
            previous_node, action = self.prevtree[current_node]
            path.insert(0, (previous_node, action, current_node))
            current_node = previous_node
        return path


class AStarSolver:
    name = 'A*Search'
    properties = {
        'optimal': True,
        'behavior': 'stochastic'
    }

    def __init__(self, gamestate):
        self.initial_gamestate = gamestate
        self.logger = Logger(self.name)
        self.tree = dict()
        heatmap = Heuristic.heatmap(gamestate)
        self.heuristic = lambda s: Heuristic.heuristic_heatmap(heatmap, s)

    def compute_path(self, end_node):
        path = []
        current = end_node

        while current in self.tree:
            parent, action = self.tree[current]
            path.insert(0, (parent, action, current))
            current = parent
        return path
    
    def solve(self):
        priority_queue = list()
        gscore_map = defaultdict(lambda : float('inf'))
        gscore_map[self.initial_gamestate] = 0
        fscore_map = defaultdict(lambda : float('inf'))
        fscore_map[self.initial_gamestate] = self.heuristic(self.initial_gamestate)
        hq.heappush(priority_queue, (fscore_map[self.initial_gamestate], self.initial_gamestate))
        
        self.logger.log_start(self.initial_gamestate)
        while priority_queue:
            _, current = hq.heappop(priority_queue)
            if current.goal_achieved():
                self.logger.log_end(current)
                return self.initial_gamestate, current, self.tree
            
            for action in current.actions():
                node = current.act(action)
                gscore = gscore_map[current] + 1
                if gscore < gscore_map[node]:
                    # self.logger.log_step(current, node, action)
                    self.tree[node] = (current, action)
                    gscore_map[node] = gscore
                    fscore_map[node] = gscore_map[node] + self.heuristic(node)
                    if node not in priority_queue:
                        hq.heappush(priority_queue, (fscore_map[node], node))
        
        self.logger.log_end(current)
        return 'No path found'