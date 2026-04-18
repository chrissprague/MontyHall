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
    
    parser.add_argument('-v', '--verbose',
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
    
    parser.add_argument('--physical',
                       action='store_true',
                       help='Run the detailed, physical simulation model.')

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
    print("usage: <script> [-v] [-n=(number_of_tests)] [-d=(number_of_doors)] [-h]")
    print(" -v      turn on print statements for reports of each test")
    print(" -n=(#)      specify the number of tests to run. more tests=higher accuracy")
    print(" -d=(#)      specify the number of doors in the simulation.")
    print(" --physical      run the physical simulation model instead of the deduction method.")
    print(" -h      print usage/help statement")
    sys.exit(0)

def which_door(exposed_list: list, chosen: int, switch: bool, num_doors: int):
    if not switch:
        return chosen
    # Since we know there's exactly one unexposed door besides the chosen one,
    # we can find it by checking the one exposed door
    for door in range(1, num_doors + 1):
        if door != chosen and door not in exposed_list:
            return door
    raise Exception('No doors left - logic bug :(')

def run_physical_method(switch_door: bool, verbose: bool = False, num_doors: int = 3, num_tests: int = 1, start_time=0):
    win_switch = 0
    win_no_switch = 0

    if verbose : print('----- Simulation Start -----')

    for i in range(num_tests):
        the_car = random.randint(1, num_doors) # where the car is
        your_door = random.randint(1, num_doors) # the door you pick.

        if verbose : print(f"\n--- Test {i+1} ---")
        if verbose : print("Car door           = " + str(the_car))
        if verbose : print("The door you chose = " + str(your_door))

        # We only need to expose enough doors to leave one other option besides the chosen door
        # First, find a door that's not the car and not the chosen door to keep unrevealed
        keep_unrevealed = None
        for j in range(1, num_doors + 1):
            if j != the_car and j != your_door:
                keep_unrevealed = j
                break

        # Now we know all other doors except your_door and keep_unrevealed are exposed
        exposed_list = [i for i in range(1, num_doors + 1)
                       if i != your_door and i != keep_unrevealed]

        if verbose : print("Revealed (goats)   = " + str(exposed_list))
        if verbose : print("Switch             = " + str(switch_door))

        # Pass num_doors to which_door
        your_selection = which_door(exposed_list, your_door, switch_door, num_doors)

        if your_selection == the_car:
            if verbose : print("You win!")
            win_switch += 1
        else:
            if verbose : print("Sorry, you lose! (Alternatively, if you were trying to get the goat, you win!)")
            win_no_switch += 1

    return win_switch, win_no_switch

def run_deduction_method(num_tests: int, num_doors: int, verbose: bool, start_time=0):
    win_switch = 0
    win_no_switch = 0

    # Run single simulation and track both outcomes
    for i in range(num_tests):
        # We are simulating the *initial* random choice only.
        the_car = random.randint(1, num_doors)
        your_door = random.randint(1, num_doors)

        # If you stick with your door
        if your_door == the_car:
            win_no_switch += 1

        # If you switch, you win if you didn't pick the car initially
        if your_door != the_car:
            win_switch += 1
    
    return win_switch, win_no_switch

def print_simulation_summary(win_switch: int, win_no_switch: int, num_tests: int, time_taken: float):
    print("\n" + "="*50)
    print("           SIMULATION SUMMARY")
    print("="*50)
    print(f"Success rate when switching doors: {(win_switch / num_tests * 100):.2f}%")
    print(f"Success rate when NOT switching doors: {(win_no_switch / num_tests * 100):.2f}%")
    print(f"Total simulation time = {time_taken:.4f}")
    print("="*50)


if __name__ == '__main__':
    # Keep track of start time for accurate output reporting
    start_time = time.time()

    args = parse_args()
    
    # Set necessary variables from args
    verbose = args.verbose
    num_tests = args.num_tests
    num_doors = args.doors
    
    print(f"Number of simulations: {num_tests:,}")
    print(f"Number of doors per simulation: {num_doors}")
    
    # Determine which method to run
    if args.physical:
        print("\n--- Running physical simulation model. ---")
        win_s, win_n = run_physical_method(False, verbose, num_doors, num_tests, start_time)
        print_simulation_summary(win_s, win_n, num_tests, time.time() - start_time)
    else:
        print("\n--- Running deductive method (default). ---")
        win_s, win_n = run_deduction_method(num_tests, num_doors, verbose, start_time)
        print_simulation_summary(win_s, win_n, num_tests, time.time() - start_time)
