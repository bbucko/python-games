import copy
import sys

import pygame
from pygame.locals import *


FPS = 30
BOARD_SIZE = 50
WINDOW_SIZE = 800
CELL_SIZE = WINDOW_SIZE / BOARD_SIZE
BORDER_SIZE = 0
PLAY_RATE = 100

# Set colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

DISPLAYSURF = pygame.display.set_mode((WINDOW_SIZE, WINDOW_SIZE), 0, 32)
DISPLAYSURF.fill(WHITE)

# prepare variables
EMPTY = 'empty'
ALIVE = 'alive'
DEAD = 'dead'
STEP = 'step'
AUTO = 'auto'
board = []


def initialize_board():
    for i in range(0, BOARD_SIZE):
        if len(board) < BOARD_SIZE:
            board.append([])
        for j in range(0, BOARD_SIZE):
            if len(board[i]) < BOARD_SIZE:
                board[i].append(EMPTY)
    for i in range(0, BOARD_SIZE):
        board[int(BOARD_SIZE / 2)][i] = ALIVE


def draw_rect(i, j, cell_color):
    pygame.draw.rect(DISPLAYSURF, BLACK, (i * CELL_SIZE, j * CELL_SIZE, CELL_SIZE, CELL_SIZE))
    pygame.draw.rect(DISPLAYSURF, cell_color, (BORDER_SIZE + i * CELL_SIZE, BORDER_SIZE + j * CELL_SIZE, CELL_SIZE - 2 * BORDER_SIZE, CELL_SIZE - 2 * BORDER_SIZE))


def draw_board():
    for i in range(0, BOARD_SIZE):
        for j in range(0, BOARD_SIZE):
            square = board[i][j]
            if square == EMPTY:
                draw_rect(j, i, WHITE)
            elif square == ALIVE:
                draw_rect(j, i, RED)
            elif square == DEAD:
                draw_rect(j, i, GREEN)


def calculate_neighbours(i, j, previous_board):
    # X X X
    # X O X
    # X X X

    try:
        if 0 < j < BOARD_SIZE - 1 and 0 < i < BOARD_SIZE - 1:
            return check_alive(previous_board, i, j, True, True, True, True, True, True, True, True)
        elif i == 0:
            if j == 0:
                return check_alive(previous_board, i, j, False, False, False, False, True, False, True, True)
            elif j == BOARD_SIZE - 1:
                return check_alive(previous_board, i, j, False, True, True, False, True, False, False, False)
            else:
                return check_alive(previous_board, i, j, False, True, True, False, True, False, True, True)
        elif i == BOARD_SIZE - 1:
            if j == 0:
                return check_alive(previous_board, i, j, False, False, False, True, False, True, True, False)
            elif j == BOARD_SIZE - 1:
                return check_alive(previous_board, i, j, True, True, False, True, False, False, False, False)
            else:
                return check_alive(previous_board, i, j, True, True, False, True, False, True, True, False)
    except:
        print("error at: {} {}".format(i, j))
        pygame.quit()
        sys.exit()


def check_alive(previous_board, i, j, lt, t, rt, l, r, lb, b, rb):
    # (-1, -1) (0, -1) (+1, -1)
    # (-1, 0) (0, 0) (+1, 0)
    # (-1, +1) (0, +1) (+1, +1)

    count = 0
    if lt:
        count += 1 * previous_board[i - 1][j - 1] == ALIVE
    if t:
        count += 1 * previous_board[i][j - 1] == ALIVE
    if rt:
        count += 1 * previous_board[i + 1][j - 1] == ALIVE
    if l:
        count += 1 * previous_board[i - 1][j] == ALIVE
    if r:
        count += 1 * previous_board[i + 1][j] == ALIVE
    if lb:
        count += 1 * previous_board[i - 1][j + 1] == ALIVE
    if b:
        count += 1 * previous_board[i][j + 1] == ALIVE
    if rb:
        count += 1 * previous_board[i + 1][j + 1] == ALIVE
    return count


def tick():
    previous_board = copy.deepcopy(board)

    for i in range(0, BOARD_SIZE):
        for j in range(0, BOARD_SIZE):
            neighbours = calculate_neighbours(i, j, previous_board)

            if previous_board[i][j] == ALIVE:
                if neighbours == 2 or neighbours == 3:
                    board[i][j] = ALIVE
                else:
                    board[i][j] = DEAD
            else:
                if neighbours == 3:
                    board[i][j] = ALIVE
                elif board[i][j] == DEAD:
                    board[i][j] = DEAD
                else:
                    board[i][j] = EMPTY


def main():
    fps_clock = pygame.time.Clock()
    pygame.init()
    pygame.display.set_caption('Game of live!')
    mode = STEP
    millis_passed = 0

    tick_rate = PLAY_RATE
    while True:
        millis_passed += fps_clock.tick(30)
        DISPLAYSURF.fill(WHITE)
        draw_board()

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                key = pygame.key.get_pressed()
                if key[pygame.K_SPACE]:
                    if mode == STEP:
                        tick()
                if key[pygame.K_p]:
                    mode = AUTO
                if key[pygame.K_s]:
                    mode = STEP
                if key[pygame.K_m]:
                    if mode == STEP:
                        mode = AUTO
                    elif mode == AUTO:
                        mode = STEP
                if key[pygame.K_q]:
                    pygame.quit()
                    sys.exit()
                if key[pygame.K_1]:
                    tick_rate = 100
                if key[pygame.K_2]:
                    tick_rate = 200
                if key[pygame.K_3]:
                    tick_rate = 300

        if mode == AUTO and millis_passed > tick_rate:
            millis_passed = 0
            tick()

        pygame.display.update()


initialize_board()
main()