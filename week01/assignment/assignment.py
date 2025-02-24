"""
Course: CSE 251 
Lesson Week: 01
File: assignment.py 
Author: Tim Taylor

Purpose: Drawing with Python Turtle

The follow program will draw a series of shapes - squares, circles, triangles
and rectangles.  

There is a Python class called cse251Turtle that is used to hold the drawing
commands that are created by the program.  This is required because threads can
not draw to the screen - only the main thread can do this.

Instructions:

- Find the "TODO" comment below and add your code that will use threads.
- You are not allowed to use any other Python modules/packages than the packages
  currently imported below.
- You can create other functions if needed.
- No global variables.

"""

import math
import threading 
from cse251turtle import *

# Include CSE 251 common Python files. 
import os, sys
sys.path.append('../../code')   # Do not change the path.
from cse251 import *

def draw_square(tur, x, y, side, color='black'):
    """Draw Square"""
    tur.move(x, y)
    tur.setheading(0)
    tur.color(color)
    for _ in range(4):
        tur.forward(side)
        tur.right(90)


def draw_circle(tur, x, y, radius, color='red'):
    """Draw Circle"""
    steps = 8
    circumference = 2 * math.pi * radius

    # Need to adjust starting position so that (x, y) is the center
    x1 = x - (circumference // steps) // 2
    y1 = y
    tur.move(x1 , y1 + radius)

    tur.setheading(0)
    tur.color(color)
    for _ in range(steps):
        tur.forward(circumference / steps)
        tur.right(360 / steps)


def draw_rectangle(tur, x, y, width, height, color='blue'):
    """Draw a rectangle"""
    tur.move(x, y)
    tur.setheading(0)
    tur.color(color)
    tur.forward(width)
    tur.right(90)
    tur.forward(height)
    tur.right(90)
    tur.forward(width)
    tur.right(90)
    tur.forward(height)
    tur.right(90)


def draw_triangle(tur, x, y, side, color='green'):
    """Draw a triangle"""
    tur.move(x, y)
    tur.setheading(0)
    tur.color(color)
    for _ in range(4):
        tur.forward(side)
        tur.left(120)


def draw_coord_system(tur, x, y, size=300, color='black'):
    """Draw corrdinate lines"""
    tur.move(x, y)
    for i in range(4):
        tur.forward(size)
        tur.backward(size)
        tur.left(90)

def draw_squares(tur):
    """Draw a group of squares"""
    for x in range(-300, 350, 200):
        for y in range(-300, 350, 200):
            draw_square(tur, x - 50, y + 50, 100)

def draw_threaded_squares(tur, lock=threading.Lock()):
    for x in range(-300, 350, 100):
        for y in range(-300, 350, 200):
            lock.acquire()
            draw_square(tur, x - 50, y + 50, 100)
            lock.release()

def draw_circles(tur):
    """Draw a group of circles"""
    for x in range(-300, 350, 200):
        for y in range(-300, 350, 200):
            draw_circle(tur, x, y-2, 50)

def draw_threaded_circles(tur, lock=threading.Lock()):
    for x in range(-300, 350, 100):
        for y in range(-300, 350, 200):
            lock.acquire()
            draw_circle(tur, x, y-2, 50)
            lock.release()

def draw_triangles(tur):
    """Draw a group of triangles"""
    for x in range(-300, 350, 200):
        for y in range(-300, 350, 200):
            draw_triangle(tur, x-30, y-30+10, 60)

def draw_threaded_triangles(tur, lock=threading.Lock()):
    for x in range(-300, 350, 100):
        for y in range(-300, 350, 200):
            lock.acquire()
            draw_triangle(tur, x-30, y-30+10, 60)
            lock.release()

def draw_rectangles(tur):
    """Draw a group of Rectangles"""
    for x in range(-300, 350, 200):
        for y in range(-300, 350, 200):
            draw_rectangle(tur, x-10, y+5, 20, 15)

def draw_threaded_rectangles(tur, lock=threading.Lock()):
    for x in range(-300, 350, 100):
        for y in range(-300, 350, 200):
            lock.acquire()
            draw_rectangle(tur, x-10, y+5, 20, 15)
            lock.release()

def run_no_threads(tur, log, main_turtle):
    """Draw different shapes without using threads"""

    # Draw Coords system
    tur.pensize(0.5)
    draw_coord_system(tur, 0, 0, size=375)
    tur.pensize(4)

    log.write('-' * 50)
    log.start_timer('Start Drawing No Threads')
    tur.move(0, 0)

    draw_squares(tur)
    draw_circles(tur)
    draw_triangles(tur)
    draw_rectangles(tur)

    log.step_timer('All drawing commands have been created')

    tur.move(0, 0)
    log.write(f'Number of Drawing Commands: {tur.get_command_count()}')

    # Play the drawing commands that were created
    tur.play_commands(main_turtle)
    log.stop_timer('Total drawing time')
    tur.clear()


def run_with_threads(tur, log, main_turtle):
    """Draw different shapes using threads"""

    # Draw Coors system
    tur.pensize(0.5)
    draw_coord_system(tur, 0, 0, size=375)
    tur.pensize(4)
    log.write('-' * 50)
    log.start_timer('Start Drawing With Threads')
    tur.move(0, 0)

    lock = threading.Lock()

    tRect = threading.Thread(target=draw_threaded_rectangles, args=(tur, lock,))
    tCirc = threading.Thread(target=draw_threaded_circles, args=(tur, lock,))
    tTria = threading.Thread(target=draw_threaded_triangles, args=(tur, lock,))
    tSqua = threading.Thread(target=draw_threaded_squares, args=(tur, lock,))

    tRect.start()
    tCirc.start()
    tSqua.start()
    tTria.start()

    tRect.join()
    tCirc.join()
    tSqua.join()
    tTria.join()

    log.step_timer('All drawing commands have been created')

    log.write(f'Number of Drawing Commands: {tur.get_command_count()}')

    # Play the drawing commands that were created
    tur.play_commands(main_turtle)
    log.stop_timer('Total drawing time')
    tur.clear()


def main():
    """Main function - DO NOT CHANGE"""

    log = Log(show_terminal=True)

    # create a Screen Object
    screen = turtle.Screen()

    # Screen configuration
    screen.setup(800, 800)

    # Make turtle Object
    main_turtle = turtle.Turtle()
    main_turtle.speed(0)

    # Special CSE 251 Turtle Class
    turtle251 = CSE251Turtle()

    # Test 1 - Drawing with no threads
    run_no_threads(turtle251, log, main_turtle)
    
    main_turtle.clear()

    # Test 2 - Drawing with threads
    run_with_threads(turtle251, log, main_turtle)

    # Waiting for user to close window
    turtle.done()


if __name__ == "__main__":
    main()
