import pygame
from colors import *


class Node:
    def __init__(self, row, col, width, num_rows):
        self.row = row
        self.col = col

        # Keep track of coordinate on the screen
        self.x = row * width
        self.y = col * width

        self.color = WHITE
        self.neighbors = []
        self.width = width
        self.num_rows = num_rows

    def get_pos(self):
        return self.row, self.col

    def is_visited(self):
        return self.color == RED

    def not_visited(self):
        return self.color == GRAY

    def is_obstacle(self):
        return self.color == BLACK

    def is_start(self):
        return self.color == ORANGE

    def is_end(self):
        return self.color == TEAL

    def reset(self):
        self.color = WHITE

    def mark_start(self):
        self.color = ORANGE

    def mark_visited(self):
        self.color = RED

    def mark_not_visited(self):
        self.color = GRAY

    def mark_obstacle(self):
        self.color = BLACK

    def mark_end(self):
        self.color = TEAL

    def mark_path(self):
        self.color = GREEN

    def draw(self, win):
        # The last argument is the position and shape
        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.width))

    def update_neighbors(self, grid):
        # build the neighbors list of valid nodes
        # that could be neighbors
        # diagonal nodes are not neighbors

        self.neighbors = []

        # DOWN ONE ROW
        if (
            self.row < self.num_rows - 1
            and not grid[self.row + 1][self.col].is_obstacle()
        ):
            self.neighbors.append(grid[self.row + 1][self.col])
        # UP ONE ROW
        if self.row > 0 and not grid[self.row - 1][self.col].is_obstacle():
            self.neighbors.append(grid[self.row - 1][self.col])
        # RIGHT ONE COLUMN
        if (
            self.col < self.num_rows - 1
            and not grid[self.row][self.col + 1].is_obstacle()
        ):
            self.neighbors.append(grid[self.row][self.col + 1])
        # LEFT ONE COLUMN
        if self.col > 0 and not grid[self.row][self.col - 1].is_obstacle():
            self.neighbors.append(grid[self.row][self.col - 1])

    def __lt__(self, other):
        # Handles what happens when you compare two Nodes
        # Other Node is always greater than self
        return False


def h(p1, p2):
    # Calculates the distance between two points
    # Manhatten distance is used

    x1, y1 = p1
    x2, y2 = p2

    return abs(x1 - x2) + abs(y1 - y2)


def create_path(came_from, current, draw):
    while current in came_from:
        current = came_from[current]
        current.mark_path()
        draw()
