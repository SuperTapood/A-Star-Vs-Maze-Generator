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
    current.rect(current.green)
    for eve in pygame.event.get():
        if eve.type == pygame.QUIT:
            exit()
    pygame.display.update()
    return


active_cell = [0, 0]
cols = 70
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
    path = []
    start_node.g_score = 0
    start_node.f_score = h(start_node)
    open_set = [start_node]
    current = cells[0][0]
    i = 0
    while True:
        i += 1
        print(i)
        if not current.visited:
            current.visited = True
        pals = current.has_valid_pals(cells)
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
        draw()
        if not stack:
            break
        current = stack.pop()

    # done generating

    while True:
        scr.fill((0, 0, 0))
        # clock.tick(200)
        if not open_set:
            print("AAA")
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
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
        for cell in cells.flatten():
            cell.blit()
        current.draw_green()
        pygame.display.update()

    par = current
    start = time()
    while True:
        while True:
            try:
                path.append(par)
                par = par.parent
            except Exception as e:
                # print(e)
                break
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
        for cell in cells.flatten():
            cell.blit()
        for cell in path:
            if cell is not None:
                cell.red = (0, 255, 0)
        pygame.display.update()
        if time() - start >= 0.2:
            break
    for cell in cells.flatten():
        cell.reset()
