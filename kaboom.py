from multiprocessing.connection import answer_challenge
import random
import re
import time
import os
import sys
import subprocess

from numpy import true_divide

gridDimension = 8
attemptsLeft = 24
allShips = shipsLeft = []
debug = True
grid = [['·' for x in range(gridDimension)] for y in range(gridDimension)]
alphabet = "abcdefgh"
debug = False
forfeit = False

messages = ["      KABOOM !",
            "      SPLOOSH...", 
            "      Already shot here, try other coordinates!",
            "      VICTORY !!", 
            "      GAME OVER..."]

# Prints grid
def print_grid(int=-1):
    global alphabet, attemptsLeft, shipsLeft, messages
    print("\n     1 2 3 4 5 6 7 8\n    -----------------")
    for x in range(gridDimension):
        print(alphabet[x], end=")   ")


        for y in range(gridDimension):
            print(grid[x][y], end=" ")
        if x == 1:
            if int > -1:
                print(messages[int], end="")
        if x == 4:
            print(f"      Attempts left: {attemptsLeft}", end="")
        if x == 5:
            print(f"      Ships left: {len(shipsLeft)}", end="")
        print("")
    print("")

# Generates random coordinates for a ship of X size.
def generate_coordinates(size):
    global grid, allShips
    coordinates = []
    
    base = [random.randint(0, 7), random.randint(0, 7)]
    direction = random.choice(["up", "down", "left", "right"])
    
    if direction == "up":
        if (base[0] - (size - 1)) < 0:
            base[0] = size - 1
        for i in range(((base[0]) - size + 1), (base[0] + 1)):
                coordinates.append([i, base[1]])
                
    elif direction == "down":
        if (base[0] + (size - 1)) > 7:
            base[0] = 7 - (size - 1)
        for i in range(base[0], base[0] + size):
            coordinates.append([i, base[1]])
            
    elif direction == "left":
        if (base[1] - (size - 1)) < 0:
            base[1] = 0 + (size - 1)
        for i in range(((base[1]) - size + 1), (base[1] + 1)):
            coordinates.append([base[0], i])
            
    else:
        if (base[1] + (size - 1)) > 7:
            base[1] = 7 - (size - 1)
        for i in range(base[1], (base[1] + size)):
           coordinates.append([base[0], i])

    return coordinates

# (bool) Checks if coordinates already exist in the allShips list.
def legal(coordinates):
    for boats in allShips:
        for boat in boats:
            for coordinate in coordinates:
                if coordinate == boat:
                    return False
    return True

# Main function to generates all three ships.
def initiate_ships():
    global shipsLeft, debug
    for i in range(4, 1, -1):
        coordinates = generate_coordinates(i)
        while not legal(coordinates):
            coordinates = generate_coordinates(i)
        allShips.append(coordinates)
    shipsLeft = allShips.copy()
    
    if debug == True:
        for ships in shipsLeft:
            for ship in ships:
                grid[ship[0]][ship[1]] = "O"
    
    print_grid()


def get_input():
    global alphabet
    while True:
        guess = input("WHAT'S YOUR GUESS? ").lower()
        if re.match(r'[a-h]{1}-[1-8]{1}$', guess):
            
            # Converts input to readable data.
            guess = [int(alphabet.index(guess[0])), int(guess[-1]) - 1]
            return guess
        elif guess == "forfeit":
            return guess
        elif guess == "exit":
            exit()
        print('Invalid input, please try again! (ex: A-1, "exit" to leave)')

def endgame():
    while True:
        answer = input("WANNA PLAY AGAIN ? ").lower()
        if answer in ["y", "yes", "n", "no"]:
            return answer
        elif answer == "exit":
            exit()
        print('Invalid input, please try again! ("yes" or "no")')

def kaboom(coordinates):
    global grid, shipsLeft
    # Already hit that spot:
    if grid[coordinates[0]][coordinates[1]] in ["·", "O"]:
        for ships in shipsLeft:
            for ship in ships:
                if coordinates == ship:
                    remove_ship(shipsLeft, ships, ship)
                    return 0
        return 1
    else:
        return 2
    
def remove_ship(list, ships, ship):
    ships.remove(ship)
    if ships == []:
        list.remove(ships)

def game_over():
    for ships in shipsLeft:
        for ship in ships:
            grid[ship[0]][ship[1]] = "O"
    return 4


def main():
    global grid, debug, attemptsLeft, shipsLeft, forfeit, debug

    print("\n--------- WELCOME TO SPLOOSH KABOOM! ---------")
    initiate_ships()

    while not (attemptsLeft == 0 or shipsLeft == 0):
        guess = get_input()
        
        print("\n----------------------------------------------")
        
        if guess == "forfeit":
            attemptsLeft = 0
            forfeit = True
            break
        elif kaboom(guess) == 0:
            grid[guess[0]][guess[1]] = "X"
            attemptsLeft = attemptsLeft - 1
            print_grid(0)
        elif kaboom(guess) == 1:
            grid[guess[0]][guess[1]] = "~"
            attemptsLeft = attemptsLeft - 1
            print_grid(1)
        else:
            print_grid(2)
        
    if shipsLeft == 0:
        print_grid(3)
    if attemptsLeft == 0:
        print_grid(game_over())
    
    
    if endgame() in ["y", "yes"]:
        print("\nRestarting the game...")
        time.sleep(1.5)
        subprocess.call([sys.executable, os.path.realpath(__file__)] +
sys.argv[1:])
    else:
        print("\nThanks for playing! <3")
        time.sleep(1.5)
        exit()
        

main()

