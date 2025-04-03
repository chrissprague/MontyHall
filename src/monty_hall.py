#!/usr/bin/env python3

"""
program simulation of the Monty Hall problem.

author: Christopher Sprague
"""

import random
import sys
import time
import argparse

def parse_args():
    parser = argparse.ArgumentParser(
        description='Simulate the Monty Hall problem to demonstrate probability outcomes.',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    parser.add_argument('-p', '--print',
                       action='store_true',
                       help='Print detailed information for each test run')
    
    parser.add_argument('-n', '--num-tests',
                       type=int,
                       default=100000,
                       help='Number of test runs to perform (default: 100000)')
    
    parser.add_argument('-d', '--doors',
                       type=int,
                       default=3,
                       help='Number of doors in the simulation (default: 3)')
    
    args = parser.parse_args()
    
    # Validate arguments
    if args.doors < 3:
        parser.error("Number of doors must be >= 3")
    if args.num_tests < 1:
        parser.error("Number of tests must be positive")
        
    return args

"""
program usage statement
"""
def usage():
    print("usage: <script> [-p] [-n=(number_of_tests)] [-d=(number_of_doors)] [-h]")
    print(" -p      turn on print statements for reports of each test")
    print(" -n=(#)      specify the number of tests to run. more tests=higher accuracy")
    print(" -d=(#)      specify the number of doors in the simulation.")
    print(" -h      print usage/help statement")
    sys.exit(0)

"""
@param exposed_list: list of int. List of doors exposed to be goats (min 1.)
@param chosen: int. The _initially_ player-selected door #
@param switch: bool. Whether to switch doors to the unrevealed.
"""
def which_door(exposed_list: list, chosen: int, switch: bool):
    if not switch:
        return chosen
    # Since we know there's exactly one unexposed door besides the chosen one,
    # we can find it by checking the one exposed door
    for door in range(1, num_doors + 1):
        if door != chosen and door not in exposed_list:
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

    # We only need to expose enough doors to leave one other option besides the chosen door
    # First, find a door that's not the car and not the chosen door to keep unrevealed
    keep_unrevealed = None
    for i in range(1, num_doors + 1):
        if i != the_car and i != your_door:
            keep_unrevealed = i
            break

    # Now we know all other doors except your_door and keep_unrevealed are exposed
    exposed_list = [i for i in range(1, num_doors + 1)
                   if i != your_door and i != keep_unrevealed]

    if PRINT : print("Revealed (goats)   = " + str(exposed_list))
    if PRINT : print("Switch             = " + str(switch_dooor))

    your_selection=0
    your_selection = which_door(exposed_list,your_door,switch_dooor)
    if your_selection == the_car:
        if PRINT : print("You win!")
        return 1
    else:
        if PRINT : print("Sorry, you lose! (Alternatively, if you were trying to get the goat, you win!)")
        return 0

def main(num_tests=100000, PRINT=False):
    win_switch = 0
    win_no_switch = 0
    sim_start = time.time()

    # Run single simulation and track both outcomes
    for i in range(num_tests):
        the_car = random.randint(1, num_doors)
        your_door = random.randint(1, num_doors)

        # If you stick with your door
        if your_door == the_car:
            win_no_switch += 1

        # If you switch, you win if you didn't pick the car initially
        # (because Monty must reveal all other goats, leaving you the car)
        if your_door != the_car:
            win_switch += 1

    sim_end = time.time()

    print("Success rate when switching doors: "+ str((float)(win_switch) / \
        float(num_tests) * 100) + "%")
    print("Success rate when NOT switching doors: " +str((float)(win_no_switch) / \
        float(num_tests) * 100) + "%")
    print("Total simulation time = " + str(sim_end-sim_start))

if __name__ == '__main__':
    args = parse_args()
    
    # Set global variables from args
    PRINT = args.print
    num_tests = args.num_tests
    num_doors = args.doors
    
    print(f"Number of simulations: {num_tests}")
    print(f"Number of doors per simulation: {num_doors}")
    
    main(num_tests, PRINT)

