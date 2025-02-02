#!/usr/bin/env python3

"""
program simulation of the Monty Hall problem.

author: Christopher Sprague
"""

import random
import sys
import time

"""
program usage statement
"""
def usage():
    print("usage: <script> [-p] [-n=(number_of_tests)] [-h]")
    print(" -p      turn on print statements for reports of each test")
    print(" -n=(#)      specify the number of tests to run. more tests=higher accuracy")
    print(" -d=(#)      specify the number of doors in the simulation.")
    print(" -h      print usage/help statement")

"""
@param exposed_list: list of int. List of doors exposed to be goats (min 1.)
@param chosen: int. The _initially_ player-selected door #
@param switch: bool. Whether to switch doors to the unrevealed.
"""
def which_door(exposed_list: list, chosen: int, switch: bool):
    if not switch:
        return chosen
    #  TODO This is wickedly inefficient xdd
    doors =  [i for i in range(1,num_doors+1)]
    for door in doors:
        if chosen != door and door not in exposed_list:
            return door
    raise Exception('No doors left - logic bug :(')

"""
@param switch_door: boolean. Whether to switch door in this simulation run.
@param PRINT: boolean. Print detailed test run info.
"""
def runMonty(switch_dooor: bool, PRINT: bool = False) -> int:
    if PRINT : print('----- Simulation Start -----')
    the_car = random.randint(1,num_doors) # where the car is
    if PRINT : print("Car door           = " + str(the_car))

    your_door = random.randint(1,num_doors) # the door you pick.
    if PRINT : print("The door you chose = " + str(your_door))

    # Reveal all doors except the one you choose and 1 other
    exposed_list = []
    for i in range(1, num_doors+1):
        if i != the_car and i != your_door:
            exposed_list.append(i)
    # The number of exposed doors must equal the total number of doors less 2
    # If the number of doors left unexposed here is 1, congrats, we know algorithmically your initial choice was the car
    # But we still gotta make things fair
    if len(exposed_list) > (num_doors - 2):
        # We've exposed too much! Pick one at random to un-expose
        random_door = random.randint(0,len(exposed_list)-1)
        exposed_list.pop(random_door)
    
    if PRINT : print("Revealed (goats)   = " + str(exposed_list))

    your_selection=0
    if PRINT : print("Switch             = " + str(switch_dooor))
    your_selection = which_door(exposed_list,your_door,switch_dooor)
    if your_selection == the_car:
        if PRINT : print("You win!")
        return 1
    else:
        if PRINT : print("Sorry, you lose! (Alternatively, if you were trying to get the goat, you win!)")
        return 0

def main(num_tests=100000, PRINT=False):
    win_switch=0
    win_no_switch=0
    sim_start = time.time()
    for i in range (0,(int)(num_tests)):
        win_switch += runMonty(True, PRINT)
        win_no_switch += runMonty(False, PRINT)
    sim_end = time.time()
    # NOTE: win_switch + win_no_switch != 100 (necessarily - these trials are completely independent of each other)
    print("Success rate when switching doors: "+ str((float)(win_switch) / \
        float(num_tests) * 100) + "%")
    print("Success rate when NOT switching doors: " +str((float)(win_no_switch) / \
        float(num_tests) * 100) + "%")
    print("Total simulation time = " + str(sim_end-sim_start))

PRINT=False
num_tests=100000
num_doors=3

for arg_num in range (0, len(sys.argv)):
    if sys.argv[arg_num] == "-h" or sys.argv[arg_num] == "--help":
        usage()
    elif sys.argv[arg_num] == "-p":
        PRINT=True
    elif sys.argv[arg_num][:3] == "-n=":
        num_tests = sys.argv[arg_num][3:]
        if num_tests == "":
            print("Bad format for num tests, aborting..." % sys.argv[arg_num][3:])
            sys.exit(2)
        try:
            num_tests = int(num_tests)
        except ValueError:
            print("Bad value or format issue for number of tests, got '%s', aborting..." % sys.argv[arg_num][3:])
            sys.exit(4)
        if num_tests < 0:
            print("Bad number of tests '%d', aborting..."%num_tests) # negative numbers, stop it nerds
            sys.exit(5)
    elif sys.argv[arg_num][:3] == "-d=":
        num_doors = sys.argv[arg_num][3:]
        if num_doors == "":
            print("Bad format for num doors, aborting..." % sys.argv[arg_num][3:])
            sys.exit(2)
        try:
            num_doors = int(num_doors)
        except ValueError:
            print("Bad value or format issue for number of doors, got '%s', aborting..." % sys.argv[arg_num][3:])
            sys.exit(4)
        if num_doors < 3:
            print("Bad number of doors '%d', must be >= 3; aborting..."%num_doors)
            sys.exit(5)

print("Number of simulations: " + str(num_tests))
print("Number of doors per simulation: " + str(num_doors))

main(num_tests, PRINT)

