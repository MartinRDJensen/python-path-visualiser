from queue import PriorityQueue
import pygame


def create_path(came_from, current, draw):
    while current in came_from:
        current = came_from[current]
        current.mark_path()
        draw()


def h(p1, p2):
    # Calculates the distance between two points
    # Manhatten distance is used

    x1, y1 = p1
    x2, y2 = p2

    return abs(x1 - x2) + abs(y1 - y2)


def algorithm(draw, grid, start, end):
    # use the lambda
    count = 0
    open_lst = PriorityQueue()
    # (f-score, insertion_id, start)
    open_lst.put((0, count, start))

    # Dictionary to keep track of the path
    came_from = {}

    # g_score keeps track of the current shortest
    # distance from the start node to this current node
    g_score = {node: float("inf") for row in grid for node in row}
    g_score[start] = 0

    # keeps track of predicted distance
    # from this node to the end node
    f_score = {node: float("inf") for row in grid for node in row}
    # Estimate distance from start to end
    f_score[start] = h(start.get_pos(), end.get_pos())

    # Used to check if anything is in the PriorityQueue
    open_lst_hash = {start}
    while not open_lst.empty():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
        # we index by 2 because we store the (fscore, insertion_ID for tiebreaker, node)
        # pop the node from the priority queue and sync with the hash
        current = open_lst.get()[2]
        open_lst_hash.remove(current)
        if current == end:
            create_path(came_from, end, draw)
            current.mark_end()
            return True
        for neighbor in current.neighbors:
            # Since the neighbor are 1 node away we add one
            # to whatever the length to current node is
            tmp_g_score = g_score[current] + 1
            # Update if better path
            if tmp_g_score < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = tmp_g_score
                f_score[neighbor] = tmp_g_score + h(neighbor.get_pos(), end.get_pos())

                if neighbor not in open_lst_hash:
                    count += 1
                    open_lst.put((f_score[neighbor], count, neighbor))
                    open_lst_hash.add(neighbor)
                    neighbor.mark_not_visited()
        draw()
        # if node we just considered not start
        # then mark it as closed
        if current != start:
            current.mark_visited()
    return False
