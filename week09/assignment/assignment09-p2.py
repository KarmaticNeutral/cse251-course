"""
Course: CSE 251 
Lesson Week: 09
File: assignment09-p2.py 
Author: Tim Taylor

Purpose: Part 2 of assignment 09, finding the end position in the maze

Instructions:
- Do not create classes for this assignment, just functions
- Do not use any other Python modules other than the ones included
- Each thread requires a different color by calling get_color()


This code is not interested in finding a path to the end position,
However, once you have completed this program, describe how you could 
change the program to display the found path to the exit position.

What would be your strategy?  

One approach that I know would work is to have each thread track its own
path and the paths of all of its child threads. This way we could check the
last value of each child thread when they finish running and if any of them
has a last value that is the same as the finish location of the maze, we
would then prepend the current thread's path onto the path of the thread
that ended at the finish point and continue passing it back up until we
reach the top and then return the whole path.

Why would it work?

Python lists can be manipulated from within a thread as they are passed
by reference.

"""
import math
import threading 
from screen import Screen
from maze import Maze

import cv2

# Include cse 251 common Python files - Dont change
import os, sys
sys.path.append('../../code')   # Do not change the path.
from cse251 import *

SCREEN_SIZE = 800
COLOR = (0, 0, 255)
COLORS = (
    (0,0,255),
    (0,255,0),
    (255,0,0),
    (255,255,0),
    (0,255,255),
    (255,0,255),
    (128,0,0),
    (128,128,0),
    (0,128,0),
    (128,0,128),
    (0,128,128),
    (0,0,128),
    (72,61,139),
    (143,143,188),
    (226,138,43),
    (128,114,250)
)

# Globals
current_color_index = 0
thread_count = 0
stop = False

def get_color():
    """ Returns a different color when called """
    global current_color_index
    if current_color_index >= len(COLORS):
        current_color_index = 0
    color = COLORS[current_color_index]
    current_color_index += 1
    return color


def solve_find_end(maze):
    """ finds the end position using threads.  Nothing is returned """
    # When one of the threads finds the end position, stop all of them
    global thread_count
    global stop
    thread_count = 0
    stop = False
    (row, col) = maze.get_start_pos()
    maze.move(row, col, COLOR)
    path_helper(maze, row, col, get_color())
    return path

def path_helper(maze, row, col, color):
    global stop
    global thread_count
    if stop == True:
        return
    if maze.at_end(row, col):
        stop = True
        return 
    moves = maze.get_possible_moves(row, col)
    #print(f'Location: {row, col} \nMoves: {moves} \n\n')
    if len(moves) > 0:
        (nrow, ncol) = moves[0]
        maze.move(nrow, ncol, color)
        path_helper(maze, nrow, ncol, color)
        threads = []
        for m in moves[1:]:
            (nrow, ncol) = m
            if maze.can_move_here(nrow, ncol):
                ncolor = get_color()
                maze.move(nrow, ncol, ncolor)
                threads.append(threading.Thread(target=path_helper, args=(maze, nrow, ncol, ncolor)))
                thread_count += 1
        for t in threads:
            t.start()
        for t in threads:
            t.join()


def find_end(log, filename, delay):
    """ Do not change this function """

    global thread_count

    # create a Screen Object that will contain all of the drawing commands
    screen = Screen(SCREEN_SIZE, SCREEN_SIZE)
    screen.background((255, 255, 0))

    maze = Maze(screen, SCREEN_SIZE, SCREEN_SIZE, filename, delay=delay)

    solve_find_end(maze)

    log.write(f'Number of drawing commands = {screen.get_command_count()}')
    log.write(f'Number of threads created  = {thread_count}')

    done = False
    speed = 1
    while not done:
        if screen.play_commands(speed): 
            key = cv2.waitKey(0)
            if key == ord('+'):
                speed = max(0, speed - 1)
            elif key == ord('-'):
                speed += 1
            elif key != ord('p'):
                done = True
        else:
            done = True



def find_ends(log):
    """ Do not change this function """

    files = (
        ('verysmall.bmp', True),
        ('verysmall-loops.bmp', True),
        ('small.bmp', True),
        ('small-loops.bmp', True),
        ('small-odd.bmp', True),
        ('small-open.bmp', False),
        ('large.bmp', False),
        ('large-loops.bmp', False)
    )

    log.write('*' * 40)
    log.write('Part 2')
    for filename, delay in files:
        log.write()
        log.write(f'File: {filename}')
        find_end(log, filename, delay)
    log.write('*' * 40)


def main():
    """ Do not change this function """
    sys.setrecursionlimit(5000)
    log = Log(show_terminal=True)
    find_ends(log)



if __name__ == "__main__":
    main()