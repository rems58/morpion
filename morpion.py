import random
import os
from time import *
os.system('cls')

 
def ask_int(message: str, min: int, max: int):
    run = True
    while run:
        try:
            check: int = int(input(message))
            if min <= check <= max :
                break
            else:
                print(f'veuillez rentrer un nombre entre {min} et {max}')
        except ValueError:
            print("veuillez rentrer un nombre valide")
    return check
 
 
available = []
 
def init_available(grid):
 
    for i in range(grid_length):
        for j in range(grid_length):
            if grid[i][j] == " ":
                available.append((i,j))
    return available
 
grid_length = ask_int("Choisissez la taille de la grille entre 3 et 10000 ", 3, 10000)
winning_symbol_count = ask_int(f"Choisissez le nombre de symbol consécutif gagnants entre 3 et {grid_length} ", 3, grid_length)
 
 
 
 
 
def check_win_next_turn(grid, symbol) -> tuple[int, int]:
    for i in range(len(available)):
        coordinates = available[i]
 
        line = coordinates[0]
        column = coordinates[1]
 
        #DEBUG
        #print(column)
 
        grid[line][column] = symbol #mettre un symbol dans la 2e grid
        if check_win(grid, symbol, line, column):
            grid[line][column] = " "
            return (line, column)
 
 
        grid[line][column] = " "
 
    return (None, None)
 
 
def display_grid(grid):
    for line in grid:
        print(" | ".join(line))
        print("-" * (3*(grid_length+1)))
 
 
def get_symbol_in_grid(grid, line, column) -> str:
    if not 0 <= line < grid_length or not 0 <= column < grid_length :
        return " "
 
    return grid[line][column]
 
 
def check_align(grid, line, column, dx, dy, symbol):
        number_valid = 1
        for i in range(1, winning_symbol_count):
            if get_symbol_in_grid(grid, line + dx * i, column + dy * i) != symbol:
                break
            number_valid += 1
 
        for i in range(1, winning_symbol_count):
            if get_symbol_in_grid(grid, line - dx * i, column - dy * i) != symbol:
                break
            number_valid += 1
 
        return number_valid >= winning_symbol_count
 
def check_win(grid, symbol, line ,column):
    return(
    check_align(grid, line, column, 1, 0, symbol) or
    check_align(grid, line, column, 0, 1, symbol) or
    check_align(grid, line, column, 1, 1, symbol) or
    check_align(grid, line, column, 1, -1, symbol) 
    )
 
 
def ia_turn(grid, ia_symbol, player_symbol):
    chrono = time()
    line, column = check_win_next_turn(grid, ia_symbol)
    if line == None:
        line, column = check_win_next_turn(grid, player_symbol)
        if line == None:
            coordinates = random.choice(available)
            line = coordinates[0]
            column = coordinates[1]
 
 
    grid[line][column] = ia_symbol
    available.pop(available.index((line, column)))
    print(time()- chrono)
 
 
 
 
 
def play():
    grid = [[" " for _ in range(grid_length)] for _ in range(grid_length)]
    turn = "X"
 
 
    available = init_available(grid)
 
    while True:
        #display_grid(grid)
 
        if turn == "X":
            print(f"tour du joueur {turn}")
            line = ask_int(f"Choisissez une ligne entre 0 et {grid_length-1}  ", 0, grid_length-1)
            column = ask_int(f"Choisissez une colonne entre 0 et {grid_length-1}  ", 0, grid_length-1)
 
 
 
            if grid[line][column] == " ":
                available.pop(available.index((line,column)))
                grid[line][column] = turn
            else:
                print("Cette case est déjà occupée. Essayez à nouveau.")
                continue
        else:
            print(f"tour de l'IA {turn}")
            ia_turn(grid, "O", "X")
 
        if check_win(grid, turn, line, column):
            display_grid(grid)
            if turn == "X":
                print(f"Le joueur {turn} a gagné ! Félicitations !")
            else:
                print(f"L'IA {turn} a gagné !")
            break
        elif " " not in [cell for row in grid for cell in row]:
            display_grid(grid)
            print("Match nul !")
            break
 
        turn = "O" if turn == "X" else "X"
 
if __name__ == "__main__":
    play()