"""
1. generate the maze
2. reset the cells
3. A*
"""
import random
from time import time

import numpy as np
import pygame

from cell import Cell


def h(node):
    # return np.sqrt(np.square(node.i - end_node.i) + np.square(node.j - end_node.j))
    return np.abs(node.i - end_node.i) + \
           np.abs(node.j - end_node.j)


def get_min(arr):
    min_item = arr[0]
    mini = min_item.f_score
    for i in range(1, len(arr)):
        if arr[i].f_score < mini:
            min_item = arr[i]
            mini = min_item.f_score
    return min_item


def draw():
    scr.fill((0, 0, 0))
    for c in cells.flatten():
        c.blit()
    current.draw_rect(current.green)
    for eve in pygame.event.get():
        if eve.type == pygame.QUIT:
            exit()
    pygame.display.update()
    return


active_cell = [0, 0]
cols = 50
width, height = 800, 800
scr = pygame.display.set_mode((width, height))
clock = pygame.time.Clock()
end = None
stack = []
path = []
cells = [[Cell(scr, c, r, cols) for r in range(cols)] for c in range(cols)]
cells = np.array(cells)
start_node = cells[0][0]
end_node = cells[-1][-1]

while True:
    stack = []
    start_node.g_score = 0
    start_node.f_score = h(start_node)
    open_set = [start_node]
    current = cells[0][0]
    while True:
        if not current.visited:
            current.visited = True
        pals = current.get_valid_pals(cells)
        if pals:
            stack.append(current)
            index = random.randint(0, len(pals) - 1)
            pal = pals[index]
            current.remove_walls(pal)
            current = pal
            stack.append(current)
        # for maze generation with bigger boards, you might want to comment
        # this function out, it will make the maze generation instant bc
        # python won't need to render anything
        # draw()
        if not stack:
            break
        current = stack.pop()

    # this will fix draw errors if the draw call on line 77 is commented out
    # otherwise this is meaningless
    draw()
    # done generating
    while True:
        # clock.tick(40)
        if not open_set:
            # no solution
            break
        current = get_min(open_set)
        current.visited_star = True
        if current == end_node:
            break
        open_set.remove(current)
        for neighbor in current.get_pals(cells):
            if current.g_score < neighbor.g_score and not neighbor.wall:
                neighbor.parent = current
                neighbor.g_score = current.g_score
                neighbor.f_score = neighbor.g_score + h(neighbor)
                if neighbor not in open_set:
                    open_set.append(neighbor)
        current.blit()
        pygame.display.update()
        for eve in pygame.event.get():
            if eve.type == pygame.QUIT:
                exit()
    par = current
    start = time()
    while True:
        while True:
            try:
                # may raise AttributeError for NoneType and "parent"
                par.in_path = True
                par = par.parent
            except AttributeError as e:
                # the path only needs to be drawn once bc its static
                draw()
                # break bc this means the path ended
                break
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
        pygame.display.update()
        # display the path for what may or may not be 0.2 seconds
        if time() - start >= 0.2:
            break
    for cell in cells.flatten():
        cell.reset()
