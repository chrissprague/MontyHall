#!/usr/bin/python

"""
program simulation of the Monty Hall problem.

author: Christopher Sprague
"""

import random , sys

"""
program usage statement
"""
def usage():
	print("usage: python3 MontyHall.py [-p] [-n=(number_of_tests)] [-h]")
	print(" -p 		turn on print statements for reports of each test")
	print(" -n=(#)		specify the number of tests to run. more tests=higher accuracy")
	print(" -h 		print usage/help statement")

"""
given an exposed door, a door that was initially chosen before the exposition,
and a boolean asking whether or not the player will switch doors, determine
which door will ultimately be selected in this test.
"""
def which_door(exposed, chosen, switch):
	if not switch:
		return chosen
	doors =  [1 , 2 , 3]
	for door in doors:
		if chosen != door and exposed != door:
			return door

"""
run the tests.
with PRINT set to True, each test will report what happens (the door that
was picked, exposed, selected afterwards, etc.)

switcherino is also a boolean which is used to specify whether or not in this
test we are considering the case in which the user picks the first door or
if they switch the door after the goat is exposed.
"""
def runMonty(switcherino, PRINT=False):
	the_car = random.randint(1,3) # where the car is

	door = random.randint(1,3) # the door you pick.
	if PRINT : print("door chosen is " + (str)(door))

	exposed = random.randint(1,3) # the door that Monty Hall reveals to be goat-infused
	while exposed == door or exposed == the_car: # it won't be your door and it won't be the car.
		exposed = random.randint(1,3)
	if PRINT : print("the host reveals that door " + (str)(exposed) + " is actually a goat")

	your_selection=0
	if switcherino:
		if PRINT : print("you decide to switch doors. --- ",)
	else:
		if PRINT : print("you decide to choose the same door. --- ",)
	your_selection = which_door(exposed,door,switcherino)
	if your_selection == the_car:
		if PRINT : print("success, you've won the car!")
		return 1
	else:
		if PRINT : print("sorry, you lose! try again next time! (alternatively, if you were trying to get the goat, you win!)")
		return 0

"""
main program fxn
"""
def main(num_tests=100000, PRINT=False):
	win_switch=0
	win_no_switch=0
	for i in range (0,(int)(num_tests)):
		win_switch += runMonty(True, PRINT)
		win_no_switch += runMonty(False, PRINT)
	# NOTE: 	win_switch + win_no_switch != 100 (necessarily - these trials are completely independent of each other)
	print("Success rate when switching doors: "+(str)((float)(win_switch) / \
		(float)(num_tests) * 100) + "%")
	print("Success rate when NOT switching doors: "+(str)((float)(win_no_switch) / \
		(float)(num_tests) * 100) + "%")

PRINT=False
num_tests=100000
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
	elif sys.argv[arg_num] != 'python' and sys.argv[arg_num] != 'MontyHall.py':
		print("Unrecognized option '%s', aborting..." % sys.argv[arg_num])
		sys.exit(3)

print("Number of tests (more tests = higher accuracy) " + (str)(num_tests))
main(num_tests, PRINT)

