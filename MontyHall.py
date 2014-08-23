#!/usr/bin/python
import random , sys

def which_door(exposed, chosen, switch):
	if not switch:
		return chosen
	doors =  [1 , 2 , 3]
	for door in doors:
		if chosen != door and exposed != door:
			return door

def do_the_stuff(switcherino, PRINT=False):
	the_car = random.randint(1,3) # where the car is

	door = random.randint(1,3) # the door you pick.
	if PRINT : print "door chosen is " + (str)(door)

	exposed = random.randint(1,3) # the door that Monty Hall reveals to be goat-infused
	while exposed == door or exposed == the_car: # it won't be your door and it won't be the car.
		exposed = random.randint(1,3)
	if PRINT : print "the host reveals that door " + (str)(exposed) + " is actually a goat"

	your_selection=0
	if switcherino:
		if PRINT : print "you decide to switch doors. --- ",
	else:
		if PRINT : print "you decide to choose the same door. --- ",
	your_selection = which_door(exposed,door,switcherino)
	if your_selection == the_car:
		if PRINT : print "success, you've won the car!"
		return 1
	else:
		if PRINT : print "sorry, you lose! try again next time!"
		return 0

def main(num_tests=1000, PRINT=False):
	number_of_successes_upon_switching_doors=0
	number_of_successes_upon_NOT_switching_doors=0
	for i in range (0,(int)(num_tests)):
		number_of_successes_upon_switching_doors += do_the_stuff(True, PRINT)
		number_of_successes_upon_NOT_switching_doors += do_the_stuff(False, PRINT)
	print "Success rate when switching doors: "+(str)((float)(number_of_successes_upon_switching_doors) / \
		(float)(num_tests) * 100) + "%"
	print "Success rate when NOT switching doors: "+(str)((float)(number_of_successes_upon_NOT_switching_doors) / \
		(float)(num_tests) * 100) + "%"

PRINT=False
num_tests=1000
for arg_num in range (0, len(sys.argv)):
	if sys.argv[arg_num] == "-p":
		PRINT=True
	if sys.argv[arg_num] == "-n":
		num_tests = sys.argv[(arg_num+1)] # will cause index out of bounds issues if you don't specify a # of tests

main(num_tests, PRINT)



