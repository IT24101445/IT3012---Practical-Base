# agent.py
import random

class GreedyGridAgent:
    """A simple agent that tries to move around systematically to clear the grid."""

    def __init__(self):
        self.actions_pool = ['Up', 'Down', 'Left', 'Right']

    def sense_and_act(self, percept: dict) -> str:
        return random.choice(self.actions_pool)

class SimpleReflexAgent:

    def __init__(self):
        self.actions = ['Up', 'Down', 'Left', 'Right']

    def sense_and_act(self, percept: dict) -> str:

        if percept.get('food_here', False):
            return 'Up'

        if percept.get('wall_ahead', False):
            return 'Right'

        return 'Up'

class ModelBasedAgent:

    def __init__(self):
        self.visited_cells = set()
        self.relative_position = (0, 0)
        self.facing = 'Up'
        self.last_action = None
        self.last_percept = None

    def get_next_cell(self, direction):

        x, y = self.relative_position

        movement = {
            'Up': (0, 1),
            'Down': (0, -1),
            'Left': (-1, 0),
            'Right': (1, 0)
        }

        dx, dy = movement[direction]

        return (x + dx, y + dy)

    def turn_left(self, direction):

        return {
            'Up': 'Left',
            'Left': 'Down',
            'Down': 'Right',
            'Right': 'Up'
        }[direction]

    def turn_right(self, direction):

        return {
            'Up': 'Right',
            'Right': 'Down',
            'Down': 'Left',
            'Left': 'Up'
        }[direction]

    def sense_and_act(self, percept: dict):

        self.last_percept = dict(percept)

        self.visited_cells.add(self.relative_position)

        if percept.get('food_here', False):

            action = 'Up'

        elif percept.get('wall_ahead', False):

            right_direction = self.turn_right(self.facing)
            right_cell = self.get_next_cell(right_direction)

            if right_cell not in self.visited_cells:
                action = right_direction
                self.facing = right_direction
            else:
                left_direction = self.turn_left(self.facing)
                action = left_direction
                self.facing = left_direction

        else:

            forward_cell = self.get_next_cell(self.facing)

            if forward_cell in self.visited_cells:

                right_direction = self.turn_right(self.facing)
                right_cell = self.get_next_cell(right_direction)

                if right_cell not in self.visited_cells:
                    action = right_direction
                    self.facing = right_direction
                else:
                    left_direction = self.turn_left(self.facing)
                    action = left_direction
                    self.facing = left_direction

            else:
                action = self.facing

        self.last_action = action
        return action