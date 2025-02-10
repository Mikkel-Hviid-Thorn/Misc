"""
@author: Mikkel Hviid Thorn

Minesweeper
"""

from random import randint #so one can make random integers


def make_list(a, x, y):
    # makes x times y array
    l = []
    for i in range(0, x):
        l += [[]]
        for j in range(0, y):
            l[i] += [a]
    return l


def neighbours(x, y):
    # makes a list of the neighbours for each element in an x times y array
    d = dict()
    for i in range(0, x):
        for j in range(0, y):
            d[i, j] = []  # there are 8 possible neighbours in the 2d grid, therefore 8 conditions
            if i < x - 1:
                d[i, j].append((i + 1, j))
            if i > 0:
                d[i, j].append((i - 1, j))
            if j < y - 1:
                d[i, j].append((i, j + 1))
            if j > 0:
                d[i, j].append((i, j - 1))
            if i < x - 1 and j < y - 1:
                d[i, j].append((i + 1, j + 1))
            if i > 0 and j < y - 1:
                d[i, j].append((i - 1, j + 1))
            if i < x - 1 and j > 0:
                d[i, j].append((i + 1, j - 1))
            if i > 0 and j > 0:
                d[i, j].append((i - 1, j - 1))
    return d


def place_bombs(x, y, antal):
    # places bombs in the x times y array and adds indication to each neighbouring element
    neighbour_dict = neighbours(x, y)
    b, k = make_list(0, x, y), 0
    while k < antal:
        m, n = randint(0, x - 1), randint(0, y - 1)  # choosing bomb coordinates
        if b[m][n] != 'X':
            b[m][n] = 'X'
            ld = neighbour_dict[m, n]
            for i, j in ld:  # adds 1 to each neighbour of the chosen bomb location
                if b[i][j] != 'X':
                    b[i][j] += 1
            k += 1
    return b


def clear(ms, b, m, n, x, y):
    # clears the neighbours of an element if they meet certain requirement
    neighbour_dict = neighbours(x, y)
    ld, no_x = neighbour_dict[m, n], True
    if b[m][n] == 0:  # clears if element has indication 0, therefore no bombs
        for i, j in ld:
            if b[i][j] != 'X' and ms[i][j] == '#':
                ms[i][j] = b[i][j]
                ms = clear(ms, b, i, j, x, y)
    elif b[m][n] in [1, 2, 3, 4, 5, 6, 7, 8]:  # checks if element has unknown bomb as neighbour
        for i, j in ld:
            if b[i][j] == 'X' and ms[i][j] == '#':
                no_x = False
    if no_x:  # clears if element has no unknown neighbouring bomb
        for i, j in ld:
            if ms[i][j] == '#':
                ms[i][j] = b[i][j]
                ms = clear(ms, b, i, j, x, y)
    return ms


def print_board(l, x, y):
    # prints the board for an x times y array
    print(' 0 |', end='')
    for i in range(1,x+1): #x axis
        print(f' {i} ', end='')
    print('\n'+'-'*3+'+'+'-'*3*x, end='')
    for i in range(1,y+1): #y axis
        print('\n   |')
        print(f' {i} |', end='')
        for j in range(0,x): #the board
            print(f' {l[j][i-1]} ', end='')
    return print('\n')
    

def minesweeper(x, y, antal):
    # plays minesweeper / setup first
    # ms is the visual board, b is the bombs and numbers
    ms, b, bombs, numbers = make_list('#', x, y), place_bombs(x, y, antal), [], []
    x_placements, y_placements = [f'{i}' for i in range(1, x + 1)], [f'{j}' for j in range(1, y + 1)]
    
    for i in range(0, x):  # saves location of bombs and numbers, used in win condition
        for j in range(0, y):
            if b[i][j] == 'X':
                bombs += [[i,j]]
            else:
                numbers += [[i,j]]
    
    while True:  # plays minesweeper
        print_board(ms, x, y)
        
        while True:  # input for left (clear) or right (flag) click
            choice = input('Clear (c) or flag (f):')
            if choice in ['c', 'f']:
                break
            
        while True:  # input for coordinate of the point
            coor = input('Coordinates (x,y):')
            c = coor.split(',')
            if len(c) == 2 and c[0] in x_placements and c[1] in y_placements:
                c = int(c[0]) - 1, int(c[1]) - 1
                break
        
        if choice == 'f':  # if choosing flag
            if ms[c[0]][c[1]] != 'F':
                ms[c[0]][c[1]] = 'F'
            elif ms[c[0]][c[1]] == 'F':
                ms[c[0]][c[1]] = '#'
        
        if choice == 'c':  # if choosing clear
            if ms[c[0]][c[1]] != 'F' and b[c[0]][c[1]] == 'X': #chose bomb
                print_board(b, x, y)
                return print('You lost')
            elif ms[c[0]][c[1]] != 'F': #didn't choose bomb
                ms[c[0]][c[1]] = b[c[0]][c[1]]
                clear(ms, b, c[0], c[1], x, y)
        
        win = True
        for bomb in bombs: #checks if all bombs are flagged
            if ms[bomb[0]][bomb[1]] == '#':
                win = False
        for number in numbers:
            if ms[number[0]][number[1]] == 'F':
                win = False
        
        if win == True: #meeting win condition
            print_board(ms, x, y)
            return print('You won')
        
        win = True
        for number in numbers: #checks if all numbers are clear
            if ms[number[0]][number[1]] == '#':
                win = False
        
        if win == True: #meeting win condition
            print_board(ms, x, y)
            return print('You won')


play = 'y'
while play == 'y':
    
    while True:  # input yes or no
        play = input('Play minesweeper (y/n):')
        if play in ['y', 'n']:
            break
    
    if play == 'n':
        break
        
    while True:
        options = input('Options for the game (length, width, number of bombs):')
        options = options.split(',')
        if options[0].isnumeric() == True and options[1].isnumeric() == True and options[2].isnumeric() == True:
            options = int(options[0]), int(options[1]), int(options[2])
            break
        
    minesweeper(options[0], options[1], options[2])
