MontyHall
=========

A concise python script to help in understanding how the Monty Hall problem/paradox works.
Fun fact: Working out the problem in code actually helps make it a lot clearer.

From [this site](http://marilynvossavant.com/game-show-problem/): <BR />
>Suppose you’re on a game show, and you’re given the choice of three doors. Behind one door is a car, behind the others, goats. You pick a door, say #1, and the host, who knows what’s behind the doors, opens another door, say #3, which has a goat. He says to you, "Do you want to pick door #2?" Is it to your advantage to switch your choice of doors? <BR />...<BR />
>Yes; you should switch. The first door has a 1/3 chance of winning, but the second door has a 2/3 chance. Here’s a good way to visualize what happened. Suppose there are a million doors, and you pick door #1. Then the host, who knows what’s behind the doors and will always avoid the one with the prize, opens them all except door #777,777. You’d switch to that door pretty fast, wouldn’t you?

Usage:

	python3 MontyHall.py [-p] [-n=(number-of-tests)] [-h]
		-p      turn on print statements for reports of each test
		-n=(#)  specify the number of tests to run. more tests=higher accuracy
		-h      print usage/help statement

Program is python 2 and 3 compatible.

