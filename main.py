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

cols = 20
width, height = 800, 800
scr = pygame.display.set_mode((width, height))
cells = [[Cell(scr, c, r, cols) for r in range(cols)] for c in range(cols)]
cells = np.array(cells)
stack = []
current = cells[0][0]
clock = pygame.time.Clock()
end = None
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

while True:
    pygame.display.update()
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            exit()
    for cell in cells.flatten():
        cell.blit()
