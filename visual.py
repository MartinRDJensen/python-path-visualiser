import pygame
import math
from node import Node
from colors import *
from algos import algorithm

WIDTH = 800
WINDOW = pygame.display.set_mode((WIDTH, WIDTH))
pygame.display.set_caption("Path Finding Visualizer")


def create_grid(num_rows, width):
    grid = []
    # Calculate the gap between each row
    # also corresponds to the size of Node
    gap = width // num_rows

    for i in range(num_rows):
        grid.append([])
        for j in range(num_rows):
            node = Node(i, j, gap, num_rows)
            grid[i].append(node)

    return grid


def draw_grid(win, num_rows, width):
    gap = width // num_rows
    for i in range(num_rows):
        pygame.draw.line(win, GREY, (0, i * gap), (width, i * gap))
        for j in range(num_rows):
            pygame.draw.line(win, GREY, (j * gap, 0), (j * gap, width))


def draw(win, grid, num_rows, width):
    win.fill(WHITE)
    for row in grid:
        for node in row:
            node.draw(win)
    draw_grid(win, num_rows, width)

    # Take whatever is drawn and update it on the display
    pygame.display.update()


def get_clicked_pos(pos, num_rows, width):
    gap = width // num_rows
    y, x = pos

    row = y // gap
    col = x // gap

    return row, col


def main(win, width):
    ROWS = 50
    grid = create_grid(ROWS, width)

    start = None
    end = None

    run = True
    started = False

    # def draw(win, grid, num_rows, width):
    while run:
        draw(win, grid, ROWS, width)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            # Once algorithm is running
            # User can only quit
            if started:
                continue
            # If left mouse button clicked
            if pygame.mouse.get_pressed()[0]:
                pos = pygame.mouse.get_pos()
                row, col = get_clicked_pos(pos, ROWS, width)
                node = grid[row][col]

                # make sure we cannot overwrite start and end
                if not start and node != end:
                    start = node
                    start.mark_start()
                elif not end and node != start:
                    end = node
                    node.mark_end()
                # elif node != end and node != start:
                elif node not in (end, start):
                    node.mark_obstacle()

            # if right mouse button clicked
            elif pygame.mouse.get_pressed()[2]:
                pos = pygame.mouse.get_pos()
                row, col = get_clicked_pos(pos, ROWS, width)
                node = grid[row][col]
                node.reset()
                if node == start:
                    start = None
                elif node == end:
                    end = None
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and start and end:
                    for row in grid:
                        for node in row:
                            node.update_neighbors(grid)
                    # pass draw() as an argument
                    # draw is called each time to lambda is run
                    algorithm(lambda: draw(win, grid, ROWS, width), grid, start, end)
                if event.key == pygame.K_c:
                    start = None
                    end = None
                    grid = create_grid(ROWS, width)
    pygame.quit()


main(WINDOW, WIDTH)
