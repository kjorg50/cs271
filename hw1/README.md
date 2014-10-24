# HW1 - Server Synchronization

* Kyle Jorgensen
* CS 271
* Oct 24, 2014

Queries multiple time servers around the world and uses the responses to synchronize the machine local clock. I used Marzullo's algorithm, but then added extra logic for when the time intervals do not overlap. It looks at all the ranges and then finds the two with the smallest difference, then it creates a new range with the endpoints being the midpoints of these two ranges. See my report for a more detailed summary.

## Usage

To run the program, use `python clock_syc.py`