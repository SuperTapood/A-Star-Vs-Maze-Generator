import pygame


class Cell:
    def __init__(self, scr, i, j, amount):
        self.scr = scr
        self.i = i
        self.j = j
        self.visited = False
        self.visited_star = False
        self.current = False
        self.green = (0, 255, 0)
        self.purple = (137, 41, 133)
        self.red = (255, 0, 0)
        self.black = (0,) * 3
        self.white = (255,) * 3
        self.amount = amount
        self.w = int(600 / amount)
        self.right, self.left, self.down, self.up = True, True, True, True
        self.parent = None
        self.g_score = 9999999999999999999999999
        self.f_score = 9999999999999999999999999
        self.wall = False
        self.in_path = False
        return

    def get_valid_pals(self, cells):
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
        return [cell for cell in pals if not cell.visited]

    def get_pals(self, cells):
        pals = []
        # right pal
        if self.i != 0 and not self.left:
            pals.append(cells[self.i - 1][self.j])
        # left pal
        if self.i + 1 < self.amount and not self.right:
            pals.append(cells[self.i + 1][self.j])
        # down pal
        if self.j != 0 and not self.up:
            pals.append(cells[self.i][self.j - 1])
        # up pal
        if self.j + 1 < self.amount and not self.down:
            pals.append(cells[self.i][self.j + 1])
        return [cell for cell in pals if cell.visited_star == False]

    def draw_rect(self, color):
        pygame.draw.rect(self.scr, color, (self.i * self.w + 100, self.j * self.w + 100, self.w, self.w))
        return

    def blit(self):
        if self.in_path:
            self.draw_rect(self.green)
        elif self.visited_star:
            self.draw_rect(self.red)
        elif self.visited:
            self.draw_rect(self.purple)
        else:
            self.draw_rect(self.black)
        self.draw_lines()
        return

    def draw_lines(self):
        top_left = (int(self.i * self.w) + 100, int(self.j * self.w) + 100)
        top_right = (int((self.i + 1) * self.w) + 100, int(self.j * self.w) + 100)
        bottom_left = (int(self.i * self.w) + 100, int(((self.j + 1) * self.w)) + 100)
        button_right = (int((self.i + 1) * self.w) + 100, int((self.j + 1) * self.w) + 100)
        if self.up:
            pygame.draw.line(self.scr, self.white, top_left, top_right, int(self.w / 3))
        if self.left:
            pygame.draw.line(self.scr, self.white, top_left, bottom_left, int(self.w / 3))
        if self.right:
            pygame.draw.line(self.scr, self.white, top_right, button_right, int(self.w / 3))
        if self.down:
            pygame.draw.line(self.scr, self.white, bottom_left, button_right, int(self.w / 3))
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

    def reset(self):
        self.__init__(self.scr, self.i, self.j, self.amount)
        return

    pass
