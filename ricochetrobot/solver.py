import logging
import random


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
