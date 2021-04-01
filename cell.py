import pygame


class Cell:
    def __init__(self, scr, i, j, amount):
        self.scr = scr
        self.i = i
        self.j = j
        self.visited = False
        self.current = False
        self.green = (0, 255, 0)
        self.red = (137, 41, 133)
        self.black = (0, 0, 0)
        self.amount = amount
        self.w = int(600 / amount)
        self.right, self.left, self.down, self.up = True, True, True, True
        return

    def has_valid_pals(self, cells):
        pals = []
        # right pal
        if self.i != 0:
            pals.append(cells[self.i - 1][self.j])
        # left pal
        if self.i + 1 < self.amount:
            pals.append(cells[self.i + 1][self.j])
        # down pal
        if self.j != 0:
            pals.append(cells[self.i][self.j - 1])
        # up pal
        if self.j + 1 < self.amount:
            pals.append(cells[self.i][self.j + 1])
        return [cell for cell in pals if cell.visited == False]

    def rect(self, color):
        pygame.draw.rect(self.scr, color, (self.i * self.w + 100, self.j * self.w + 100, self.w, self.w))
        return

    def blit(self):
        if self.visited:
            self.rect(self.red)
        else:
            self.rect(self.black)
        self._blit()
        return

    def _blit(self):
        top_left = (int(self.i * self.w) + 100, int(self.j * self.w) + 100)
        top_right = (int((self.i + 1) * self.w) + 100, int(self.j * self.w) + 100)
        bottom_left = (int(self.i * self.w) + 100, int(((self.j + 1) * self.w)) + 100)
        button_right = (int((self.i + 1) * self.w) + 100, int((self.j + 1) * self.w) + 100)
        if self.up:
            pygame.draw.line(self.scr, (255, 255, 255), top_left, top_right, int(self.w / 3))
        if self.left:
            pygame.draw.line(self.scr, (255, 255, 255), top_left, bottom_left, int(self.w / 3))
        if self.right:
            pygame.draw.line(self.scr, (255, 255, 255), top_right, button_right, int(self.w / 3))
        if self.down:
            pygame.draw.line(self.scr, (255, 255, 255), bottom_left, button_right, int(self.w / 3))
        # line(surface, color, start_pos, end_pos, width)
        return

    def remove_walls(self, other):
        if self.i > other.i:
            # left
            self.left, other.right = False, False
        if self.j > other.j:
            # up
            self.up, other.down = False, False
        if self.i < other.i:
            # right
            self.right, other.left = False, False
        if self.j < other.j:
            # down
            self.down, other.up = False, False
        return

    pass
