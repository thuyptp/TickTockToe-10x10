#!/usr/bin/env python3
from math import inf as infinity
from random import choice
import platform
import time
from os import system

HUMAN = -1
COMP = +1

board = [[0]*10 for i in range(10)] #board 10x10

#create a list contains all non-null lines of the board 
def set_lines_list(state):
    lines_list = []
    
    for row in state: #take 10 rows
        line = ""
        for cell in row:
            line += str(cell)
        if "1" in line:
            lines_list.append(line)
        
    for col_index in range(0,10): #take 10 collumns
        col = ""
        row_index = 0
        while row_index < 10:
            col += str(state[row_index][col_index])
            row_index += 1
        if "1" in col:
            lines_list.append(col)

    #take cross in right side
    right_cross = ""
    for i in range(0, 10): #main cross
        right_cross += str(state[i][i])
        if "1" in right_cross:
            lines_list.append(right_cross)
    
    for i in range(0, 5):
        right_cross = ""
        j = 0
        while (j + i + 1) < 10:
            right_cross += str(state[j][j+i+1])
            j += 1
        if "1" in right_cross:
            lines_list.append(right_cross)
            
    for i in range(0,5):
        right_cross = ""
        j = 0
        while (j + i + 1) < 10:
          right_cross += str(state[j+1+i][j])
          j += 1
        if "1" in right_cross:
            lines_list.append(right_cross)
        
    #take cross in left side   
    for i in range(0, 6):
        left_cross = ""
        j = 0
        while(i+4-j) >= 0 and (i+4-j) <=9:
            left_cross += str(state[j][i+4-j])
            j += 1
        if "1" in left_cross:
            lines_list.append(left_cross)
        
    for i in range(0,5):
        left_cross = ""
        j = 1
        while (10-j) >= 0 and (10-j) <= 9 and i+j <=9:
            left_cross += str(state[j+i][10-j])
            j += 1
        if "1" in left_cross:
            lines_list.append(left_cross)
            
    return lines_list

def evaluate(state):
    if wins(state, COMP):
        score = +1000
    elif wins(state, HUMAN):
        score = -1000
    else:
        score = totalscore(state)
    return score

def totalscore(state):
    lines = set_lines_list(state)
    score = 0
    count_4human = 0
    count_4human_1 = 0
    count_3human = 0
    count_2human = 0
    count_4comp = 0
    count_4comp_1 = 0
    count_3comp = 0
    count_2comp = 0
    for line in lines:
        count_4human_1 += line.count("1-1-1-1-10") + line.count("0-1-1-1-11") + line.count("-10-1-1-1") + line.count("-1-10-1-1") + line.count("-1-1-10-1")
        count_4human += line.count("0-1-1-1-10")
        count_3human += line.count("0-1-1-10")
        count_2human += line.count("0-1-10")
        count_4comp_1 += line.count("-111110") + line.count("11101") + line.count("11011") + line.count("10111") + line.count("01111-1")
        count_4comp += line.count("011110")
        count_3comp += line.count("01110")
        count_2comp += line.count("0110")
    score = (count_4comp * 500) + (count_4comp_1 * 300) + (count_3comp * 100) + (count_2comp * 20) - (count_4human * 500) - (count_4human_1 *300) - (count_3human * 100) - count_2human * 20

    return score

def wins(state, player):
    lines = set_lines_list(state)
    player = str(player)
    win_state = player * 5
    for line in lines:
        if win_state in line and line[line.find(win_state)-1] != "-": #incase of -111110 may be win state
            return True
    return False

def game_over(state):
    return wins(state, HUMAN) or wins(state, COMP)

#get all cells around choosen cells
def limit_emptycells(state):
    cells = []
    for x, row in enumerate(state):
        for y, cell in enumerate(row):
            if cell != 0:
                if x- 1 >= 0 and state[x-1][y] == 0 and [x-1,y] not in cells:
                    cells.append([x-1, y])
                if x + 1 <= 9 and state[x+1][y] == 0 and [x+1,y] not in cells:
                    cells.append([x+1, y])
                if y - 1 >=0 and state[x][y-1] == 0 and [x,y-1] not in cells:
                    cells.append([x, y-1])
                if y + 1 <= 9 and state[x][y+1] == 0 and [x,y+1] not in cells:
                    cells.append([x, y+1])
                if x- 1 >= 0 and y + 1 <= 9 and state[x-1][y+1] == 0 and [x-1,y+1] not in cells:
                    cells.append([x-1, y+1])
                if y -1 >= 0 and x - 1 >= 0 and state[x-1][y-1] == 0 and [x-1,y-1] not in cells:
                    cells.append([x-1, y-1])
                if y + 1 <= 9 and x + 1 <=9 and state[x+1][y+1] == 0 and [x+1,y+1] not in cells:
                    cells.append([x+1, y+1])
                if y - 1 >= 0 and x + 1 <=9 and state[x+1][y-1] == 0 and [x+1,y-1] not in cells:
                    cells.append([x+1, y-1])
    return cells

def empty_cells(state):
    cells = []

    for x, row in enumerate(state):
        for y, cell in enumerate(row):
            if cell == 0:
                cells.append([x, y])

    return cells


def valid_move(x, y):
    if [x, y] in empty_cells(board):
        return True
    else:
        return False


def set_move(x, y, player):
    if valid_move(x, y):
        board[x][y] = player
        return True
    else:
        return False


def minimax(state, depth, player, alpha, beta):
    if player == COMP:
        best = [-1, -1, -infinity]
    else:
        best = [-1, -1, +infinity]

    if depth == 0 or game_over(state):
        score = evaluate(state)
        return [-1, -1, score]

    for cell in limit_emptycells(state):
        x, y = cell[0], cell[1]
        state[x][y] = player
        score = minimax(state, depth - 1, -player, alpha, beta)
        state[x][y] = 0
        score[0], score[1] = x, y
        if player == COMP:
            if score[2] > best[2]:
                best = score  # max value
            if best[2] > alpha:
                alpha = best[2]
            if beta <= best[2]:
                break
        else:
            if score[2] < best[2]:
                best = score  # min value
            if best[2] < beta:
                beta = best[2]
            if best[2] <= alpha:
                break
    return best


def clean():
    """
    Clears the console
    """
    os_name = platform.system().lower()
    if 'windows' in os_name:
        system('cls')
    else:
        system('clear')


def render(state, c_choice, h_choice):
    chars = {
        -1: h_choice,
        +1: c_choice,
        0: ' '
    }
    str_line = '-------------------------------------------------------'

    print('\n' + str_line)
    print(f'| ' '  |', end='')
    for x in range(1, 11):
        print(f'| {x} |', end='')
    print('\n' + str_line)

    y = 0
    for row in state:
        print(f'| {y} |', end='')
        for cell in row:
            symbol = chars[cell]
            print(f'| {symbol} |', end='')
        print('\n' + str_line)
        y += 1


def ai_turn(c_choice, h_choice):
    depth = len(empty_cells(board))
    if depth == 0 or game_over(board):
        return

    clean()
    print(f'Computer turn [{c_choice}]')
    render(board, c_choice, h_choice)

    if depth == 100:
        x = choice(range(0,10))
        y = choice(range(0,10))
    else:
        move = minimax(board, 3, COMP, -infinity, +infinity)
        x, y = move[0], move[1]

    set_move(x, y, COMP)
    time.sleep(1)

def human_turn(c_choice, h_choice):
    depth = len(empty_cells(board))
    if depth == 0 or game_over(board):
        return

    # Dictionary of valid moves
    move = -1
    moves = {}
    index = 0
    for i in range(0, 10):
        for j in range(0,10):
            moves[index + 1] = [i,j]
            index = index + 1

    clean()
    print(f'Human turn [{h_choice}]')
    render(board, c_choice, h_choice)

    while move < 1 or move > 100:
        try:
            move = int(input('Use numpad (1..100): '))
            coord = moves[move]
            can_move = set_move(coord[0], coord[1], HUMAN)

            if not can_move:
                print('Bad move')
                move = -1
        except (EOFError, KeyboardInterrupt):
            print('Bye')
            exit()
        except (KeyError, ValueError):
            print('Bad choice')


def main():
    """
    Main function that calls all functions
    """
    clean()
    h_choice = ''  # X or O
    c_choice = ''  # X or O
    first = ''  # if human is the first

    # Human chooses X or O to play
    while h_choice != 'O' and h_choice != 'X':
        try:
            print('')
            h_choice = input('Choose X or O\nChosen: ').upper()
        except (EOFError, KeyboardInterrupt):
            print('Bye')
            exit()
        except (KeyError, ValueError):
            print('Bad choice')

    # Setting computer's choice
    if h_choice == 'X':
        c_choice = 'O'
    else:
        c_choice = 'X'

    # Human may starts first
    clean()
    while first != 'Y' and first != 'N':
        try:
            first = input('First to start?[y/n]: ').upper()
        except (EOFError, KeyboardInterrupt):
            print('Bye')
            exit()
        except (KeyError, ValueError):
            print('Bad choice')

    # Main loop of this game
    while len(empty_cells(board)) > 0 and not game_over(board):
        if first == 'N':
            ai_turn(c_choice, h_choice)
            first = ''

        human_turn(c_choice, h_choice)
        ai_turn(c_choice, h_choice)

    # Game over message
    if wins(board, HUMAN):
        clean()
        print(f'Human turn [{h_choice}]')
        render(board, c_choice, h_choice)
        print('YOU WIN!')
    elif wins(board, COMP):
        clean()
        print(f'Computer turn [{c_choice}]')
        render(board, c_choice, h_choice)
        print('YOU LOSE!')
    else:
        clean()
        render(board, c_choice, h_choice)
        print('DRAW!')

    exit()


if __name__ == '__main__':
    main()
