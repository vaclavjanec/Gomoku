import pygame
from pygame.locals import *
import math

pygame.init()

WIDTH = 500
HEIGHT = 500
LINE_WIDTH = 6
N = 5  # Board size
WINNING_LENGTH = 4  # Number of consecutive symbols to win
MAX_DEPTH = 3 #strenght of the AI

# Colors
GREEN = (0, 255, 0)
ORANGE = (255, 165, 0)
RED = (255, 0, 0)
GRID_COLOR = (50, 50, 50)
BG_COLOR = (0, 0, 0)

# Initialize display
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Gomoku")

# Initialize board
def init_board(n):
    return [['' for _ in range(n)] for _ in range(n)]

board = init_board(N)

# Player selection
selected_player = None

while selected_player not in ['X', 'O']:
    screen.fill(BG_COLOR)
    font = pygame.font.SysFont(None, 40)
    text = font.render("Choose X or O:", True, GREEN)
    screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - text.get_height() // 2))
    pygame.display.update()

    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.unicode.upper() in ['X', 'O']:
                selected_player = event.unicode.upper()

# Set players
if selected_player == 'X':
    human_player = 'X'
    ai_player = 'O'
else:
    human_player = 'O'
    ai_player = 'X'

def draw_grid():
    screen.fill(BG_COLOR)
    for x in range(1, N):
        pygame.draw.line(screen, GRID_COLOR, (0, x * 100), (WIDTH, x * 100), LINE_WIDTH)
        pygame.draw.line(screen, GRID_COLOR, (x * 100, 0), (x * 100, HEIGHT), LINE_WIDTH)

def draw_board():
    x_pos = 0
    for x in board:
        y_pos = 0
        for y in x:
            if y == 'X':
                pygame.draw.line(screen, GREEN, (y_pos * 100 + 15, x_pos * 100 + 15),
                                 (y_pos * 100 + 85, x_pos * 100 + 85), LINE_WIDTH)
                pygame.draw.line(screen, GREEN, (y_pos * 100 + 15, x_pos * 100 + 85),
                                 (y_pos * 100 + 85, x_pos * 100 + 15), LINE_WIDTH)
            elif y == 'O':
                pygame.draw.circle(screen, ORANGE, (y_pos * 100 + 50, x_pos * 100 + 50), 38, LINE_WIDTH)
            y_pos += 1
        x_pos += 1

def evaluate_function(board, ai_player, human_player):
    ai_score = 0
    length = len(board)

    def score_line(line):
        score = 0
        line_length = len(line)

        for i in range(line_length - WINNING_LENGTH + 1):
            window = line[i:i + WINNING_LENGTH]
            if all(cell == ai_player for cell in window):
                score += 10000
            elif all(cell == human_player for cell in window):
                score -= 10000
            else:
                for k in range(WINNING_LENGTH - 3):
                    if line[i + k] == '' and line[i + k + 1] == ai_player and line[i + k + 2] == '' and \
                       line[i + k + 3] == ai_player and i + k + 3 < line_length:
                        score += 10000

                for k in range(WINNING_LENGTH):
                    if i + k < line_length:
                        if line[i + k] == ai_player:
                            if i + k + 1 < line_length and line[i + k + 1] == '':
                                score += 1000
                            else:
                                score += 500
                        elif line[i + k] == human_player:
                            if i + k + 1 < line_length and line[i + k + 1] == '':
                                score -= 1000
                            else:
                                score -= 500

        return score

    for row in board:
        ai_score += score_line(row)

    for col in range(length):
        column = [board[row][col] for row in range(length)]
        ai_score += score_line(column)

    for i in range(length - WINNING_LENGTH + 1):
        for j in range(length - WINNING_LENGTH + 1):
            diagonal1 = [board[i + k][j + k] for k in range(WINNING_LENGTH)]
            if len(diagonal1) == WINNING_LENGTH:
                ai_score += score_line(diagonal1)
            diagonal2 = [board[i + k][j + WINNING_LENGTH - 1 - k] for k in range(WINNING_LENGTH)]
            if len(diagonal2) == WINNING_LENGTH:
                ai_score += score_line(diagonal2)

    return ai_score

def is_moves_left(board):
    for row in board:
        if '' in row:
            return True
    return False

def check_win(board, player):
    for i in range(N):
        for j in range(N - WINNING_LENGTH + 1):
            if all(board[i][j + k] == player for k in range(WINNING_LENGTH)):
                return True, [(i, j + k) for k in range(WINNING_LENGTH)]
            if all(board[j + k][i] == player for k in range(WINNING_LENGTH)):
                return True, [(j + k, i) for k in range(WINNING_LENGTH)]

    for i in range(N - WINNING_LENGTH + 1):
        for j in range(N - WINNING_LENGTH + 1):
            if all(board[i + k][j + k] == player for k in range(WINNING_LENGTH)):
                return True, [(i + k, j + k) for k in range(WINNING_LENGTH)]
            if all(board[i + k][j + WINNING_LENGTH - 1 - k] == player for k in range(WINNING_LENGTH)):
                return True, [(i + k, j + WINNING_LENGTH - 1 - k) for k in range(WINNING_LENGTH)]

    return False, []

def minimax(board, depth, alpha, beta, is_maximizing, ai_player, human_player, max_depth):
    if check_win(board, ai_player)[0]:
        return 10000 + depth
    if check_win(board, human_player)[0]:
        return -10000 - depth
    if not is_moves_left(board) or depth == max_depth:
        return evaluate_function(board, ai_player, human_player)

    if is_maximizing:
        best = -math.inf
        for i in range(N):
            for j in range(N):
                if board[i][j] == '':
                    board[i][j] = ai_player
                    move_val = minimax(board, depth + 1, alpha, beta, False, ai_player, human_player, max_depth)
                    board[i][j] = ''
                    best = max(best, move_val)
                    alpha = max(alpha, best)
                    if beta <= alpha:
                        break
        return best
    else:
        best = math.inf
        for i in range(N):
            for j in range(N):
                if board[i][j] == '':
                    board[i][j] = human_player
                    move_val = minimax(board, depth + 1, alpha, beta, True, ai_player, human_player, max_depth)
                    board[i][j] = ''
                    best = min(best, move_val)
                    beta = min(beta, best)
                    if beta <= alpha:
                        break
        return best

def ai_move(board, ai_player, human_player, max_depth):
    best_val = -math.inf
    best_move = (-1, -1)

    for i in range(N):
        for j in range(N):
            if board[i][j] == '':
                board[i][j] = ai_player
                move_val = minimax(board, 0, -math.inf, math.inf, False, ai_player, human_player, max_depth)
                board[i][j] = ''
                if move_val > best_val:
                    best_val = move_val
                    best_move = (i, j)

    board[best_move[0]][best_move[1]] = ai_player
    return best_move

def human_move(board, pos):
    cell_x, cell_y = pos[1] // 100, pos[0] // 100
    if 0 <= cell_x < N and 0 <= cell_y < N and board[cell_x][cell_y] == '':
        board[cell_x][cell_y] = human_player
        return True
    return False

# Main game loop
run = True
clicked = False

while run:
    draw_grid()
    draw_board()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.MOUSEBUTTONDOWN and not clicked:
            clicked = True
        if event.type == pygame.MOUSEBUTTONUP and clicked:
            clicked = False
            pos = pygame.mouse.get_pos()
            if human_move(board, pos):
                draw_grid()
                draw_board()
                pygame.display.update()
                win, win_sequence = check_win(board, human_player)
                if win:
                    print("Human wins!")
                    for cell in win_sequence:
                        if board[cell[0]][cell[1]] == 'X':
                            pygame.draw.line(screen, RED, (cell[1] * 100 + 15, cell[0] * 100 + 15),
                                             (cell[1] * 100 + 85, cell[0] * 100 + 85), LINE_WIDTH)
                            pygame.draw.line(screen, RED, (cell[1] * 100 + 15, cell[0] * 100 + 85),
                                             (cell[1] * 100 + 85, cell[0] * 100 + 15), LINE_WIDTH)
                        elif board[cell[0]][cell[1]] == 'O':
                            pygame.draw.circle(screen, RED, (cell[1] * 100 + 50, cell[0] * 100 + 50), 38, LINE_WIDTH)
                    pygame.display.update()
                    run = False
                elif not is_moves_left(board):
                    print("It's a draw!")
                    run = False
                else:
                    ai_move(board, ai_player, human_player, MAX_DEPTH)
                    draw_grid()
                    draw_board()
                    pygame.display.update()
                    win, win_sequence = check_win(board, ai_player)
                    if win:
                        print("AI wins!")
                        for cell in win_sequence:
                            if board[cell[0]][cell[1]] == 'X':
                                pygame.draw.line(screen, RED, (cell[1] * 100 + 15, cell[0] * 100 + 15),
                                                 (cell[1] * 100 + 85, cell[0] * 100 + 85), LINE_WIDTH)
                                pygame.draw.line(screen, RED, (cell[1] * 100 + 15, cell[0] * 100 + 85),
                                                 (cell[1] * 100 + 85, cell[0] * 100 + 15), LINE_WIDTH)
                            elif board[cell[0]][cell[1]] == 'O':
                                pygame.draw.circle(screen, RED, (cell[1] * 100 + 50, cell[0] * 100 + 50), 38,
                                                   LINE_WIDTH)
                        pygame.display.update()
                        run = False
                    elif not is_moves_left(board):
                        print("It's a draw!")
                        run = False
    pygame.display.update()


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

pygame.quit()





