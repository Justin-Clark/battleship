#!/usr/bin/env python3
# Justin Clark, Kaden Roof
# 2021/11/11

# battleship.py

import random

''' The BattleShip Game! '''

DEBUG = False

EMPTY = " "

human_ship_count = 0
computer_ship_count = 0

TRC = '\u2510' # Top right corner
TLC = '\u250c' # Top left corner
BRC = '\u2518' # Bottom right corner
BLC = '\u2514' # Bottom left corner
THRZ = '\u252c' # Top horizontal bar
BHRZ = '\u2534' # Bottom horizontal bar
HRZ = '\u2500' # Horizontal bar
VRT = '\u2502' # Vertical bar
LVRT = '\u251c' #Left vertical bar
RVRT = '\u2524' # Right Vertical bar
MVRT = '\u253c' # Middle vertical bar

TROW = f"  {TLC}{(HRZ+THRZ)*9}{HRZ}{TRC}"
MROW = f"  {LVRT}{(HRZ+MVRT)*9}{HRZ}{RVRT}"
BROW = f"  {BLC}{(HRZ+BHRZ)*9}{HRZ}{BRC}"

HIT = "H"
MISS = "M"

ships = { "destroyer" : "D", "cruiser" : "C", "sub" : "S", "battleship" : "B", "carrier" : "A" }

player_positions = {}
computer_positions = {}

def setup_blank_board():
    ''' Make new Board dictionary from a-t and 0-9'''
    board = {}
    for letter in "abcdefghijklmnopqrst":
        for column in "0123456789":
            board[letter+column] = EMPTY

    return board

def display_instructions():
    ''' Displays the instructions to the screen '''
    print("""
                                                                    === Off Brand Battleship ===
            Instructions!:

            1. place your pieces on the board
            2. tell the computer whether or not you feel the need to go first or not...
            3. depending on who goes first, a player will attack on the opposite player's board and a "X" for hit will appear or an "M" for miss will appear on both boards
            4. once every one of a player's ships have been destroyed, the game will end and the player with ships still standing will be the victor

         """)

    input("Press any button to start...\n")

def display_board(b):
    '''display the fleet and attack boards'''
    print("          FLEET        \t\t          ATTACK")
    print()
    print("   0 1 2 3 4 5 6 7 8 9 \t\t   0 1 2 3 4 5 6 7 8 9 ")
    print(f"{TROW}\t\t{TROW}")
    for r in ['ak','bl','cm','dn','eo','fp','gq','hr','is','jt']:
        # Display the fleet and attack rows side by side
        r0, r1 =r[0], r[1]
        print(f" {r0}{VRT}", end='')
        # Fleet Row
        for c in "0123456789":
            print(f"{b[r0+c]}{VRT}", end='')

        # Attack Row
        print(f"\t\t{r1} {VRT}", end='')
        for c in "0123456789":
            print(f"{b[r1+c]}{VRT}", end='')

        print()
        if r != 'jt':
            print(f"{MROW}\t\t{MROW}")

        else: # print bottom of grid
            print(f"{BROW}\t\t{BROW}")

def human_board_setup(board):
    ''' make a new board with player inputs and return it '''
    player_board = dict(board)

    print("                                                                         === Planning Phase! ===\n")

    for ship in ships:
        print("Multiple inputs are accepted and are neccesary for every ship!")
        positions = input(f"Enter your positions for the {ships[ship]} (letter, number): ")
        
        positions = positions.replace(" ", "")
        positions = positions.split(",")

        if DEBUG:
            print(positions)

        for position in positions:
            print(position)
            player_board[position] = ships[ship]


            global human_ship_count
            human_ship_count += 1

    return player_board

def computer_board_setup(board):
    ''' Setup arbitrary positions for the computer '''
    #computer_board = dict(board)

    global computer_ship_count

    if not DEBUG:
        # Carrier
        for i in range(5):
            computer_board["a"+str(i)] = "A"
            computer_ship_count += 1
        
        # Battleship
        for i in range(4):
            computer_board["b"+str(i)] = "B"
            computer_ship_count += 1

        # Submarine
        for i in range(3):
            computer_board["c"+str(i)] = "S"
            computer_ship_count += 1

        # Cruiser
        for i in range(3):
            computer_board["d"+str(i)] = "C"
            computer_ship_count += 1

        # Destroyer
        for i in range(3):
            computer_board["e"+str(i)] = "D"
            computer_ship_count += 1
    else:
        computer_board["a0"] = "A"
        computer_ship_count += 1
        
        computer_board["a1"] = "A"
        computer_ship_count += 1

    return computer_board

def yes_or_no():
    ''' Ask the user for yes or no and return it '''
    first = False

    answer = input("Would you like to go first? (y/n): ")

    if answer.lower() == "y":
        first = True
    elif answer.lower() == "n":
        first = False

    return first

def attack(person):
    ''' attacks the opposing board '''

    global human_ship_count
    global computer_ship_count

    if person != "computer":
        coordinates = input("Where do you want to attack?: ")
    else:
        comp_cords = "klmnopqrst"
        coordinates = comp_cords[random.randint(0, len(comp_cords) - 1)] + str(random.randint(0, 9))

    actual_coordinates = actual_coords(coordinates)

    if person == "human":
        if computer_board[actual_coordinates] != EMPTY:
            print(f"Hit! at position {coordinates}\n")
            human_board[coordinates] = "X"
            computer_board[actual_coordinates] = "X"
            computer_ship_count -= 1

        elif computer_board[actual_coordinates] == EMPTY:
            print(f"Miss! at position {coordinates}\n")
            human_board[coordinates] = "M"

    elif person == "computer":
        if human_board[actual_coordinates] != EMPTY:
            print(f"Hit! at position {coordinates}\n")
            computer_board[coordinates] = "X"
            human_board[actual_coordinates] = "X"
            human_ship_count -= 1
        
        elif human_board[actual_coordinates] == EMPTY:
            print(f"Miss! at position {coordinates}\n")
            computer_board[coordinates] = "M"

def actual_coords(coords):
    ''' Convert the coordinates to the enemy coordinates or vice versa '''
    alpha = "abcdefghijklmnopqrst"
    letter = coords[0]
    actual_index = alpha.find(letter)-10
    actual_coordinates = alpha[actual_index] + coords[1]

    return actual_coordinates

display_instructions()

# Setup
human_board = setup_blank_board()
human_board = human_board_setup( human_board )

computer_board = setup_blank_board()
computer_board = computer_board_setup( computer_board )

#print("Human Board")
#display_board( human_board )

if DEBUG:
    print("Computer Board")
    display_board( computer_board )

first = "human"

if yes_or_no():
    print("Human is going first")
    print("Hahahaha, it looks like you need it!")

    first = "human"
else:
    print("Computer is going first")
    print("Don't get too cocky -_-, it will be your undoing\n")

    first = "computer"

done = False

# Gameplay
while not done:

    done = False

    if human_ship_count == 0:
        print("< You Lose >")

        print("Here was the computer's board!")
        display_board(computer_board)

        done = True
        break

    if computer_ship_count == 0:
        print(" < You Win >")
        
        print("Here was the computer's board!")
        display_board(human_board)

        done = True
        break

    if first == "human":

        if DEBUG:
            print("==== Human Board ====")
        
        display_board(human_board)

        if DEBUG:
            print(computer_board)

        print("\n === Human is going... === \n")
        attack(first)
        first = "computer"
    elif first == "computer":

        if DEBUG:
            print("==== Computer Board ====")
            display_board(computer_board)
        print("=== Computer is going... ===")
        attack(first)
        first = "human"

print("Game is Done!")
