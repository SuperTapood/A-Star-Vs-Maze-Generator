"""
1. Choose the initial cell, mark it as visited and push it to the stack
2. While the stack is not empty
    1. Pop a cell from the stack and make it a current cell
    2. If the current cell has any neighbours which have not been visited
        1. Push the current cell to the stack
        2. Choose one of the unvisited neighbours
        3. Remove the wall between the current cell and the chosen cell
        4. Mark the chosen cell as visited and push it to the stack
"""

import random

import numpy as np
import pygame

from cell import Cell


def h(node):
    # pythagoras theroem
    return np.sqrt(np.square(abs(node.i - end_node.i)) + np.square(abs(node.j - end_node.j)))


def get_min(arr):
    min_item = arr[0]
    mini = min_item.f_score
    for i in range(1, len(arr)):
        if arr[i].f_score < mini:
            min_item = arr[i]
            mini = min_item.f_score
    return min_item


while True:
    active_cell = [0, 0]
    cols = 20
    width, height = 800, 800
    scr = pygame.display.set_mode((width, height))
    cells = [[Cell(scr, c, r, cols) for r in range(cols)] for c in range(cols)]
    cells = np.array(cells)
    stack = []
    current = cells[0][0]
    clock = pygame.time.Clock()
    end = None
    start_node = cells[0][0]
    end_node = cells[-1][-1]
    start_node.g_score = 0
    start_node.f_score = h(start_node)
    open_set = [start_node]
    path = []
    while True:
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
        scr.fill((0, 0, 0))
        for cell in cells.flatten():
            cell.blit()
        current.rect(current.green)
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                exit()
        pygame.display.update()
        if not stack:
            break
        current = stack.pop()

    # done generating

    while True:
        scr.fill((0, 0, 0))
        clock.tick(50)
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
                if not neighbor in open_set:
                    open_set.append(neighbor)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
        for cell in cells.flatten():
            cell.blit()
        current.draw_green()
        pygame.display.update()

    par = current
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
                cell.draw_green()
        pygame.display.update()
