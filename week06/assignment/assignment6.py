"""
Course: CSE 251
Lesson Week: 06
File: assignment.py
Author: Tim Taylor
Purpose: Processing Plant
Instructions:
- Implement the classes to allow gifts to be created.
"""

import random
import multiprocessing as mp
import os.path
import time

# Include cse 251 common Python files - Don't change
import os, sys
sys.path.append('../../code')   # Do not change the path.
from cse251 import *

CONTROL_FILENAME = 'settings.txt'
BOXES_FILENAME   = 'boxes.txt'

# Settings consts
MARBLE_COUNT = 'marble-count'
CREATOR_DELAY = 'creator-delay'
BAG_COUNT = 'bag-count'
BAGGER_DELAY = 'bagger-delay'
ASSEMBLER_DELAY = 'assembler-delay'
WRAPPER_DELAY = 'wrapper-delay'

# Signal const
NO_MORE = "No More"

# No Global variables

class Bag():
    """ bag of marbles - Don't change for the 93% """

    def __init__(self):
        self.items = []

    def add(self, marble):
        self.items.append(marble)

    def get_size(self):
        return len(self.items)

    def __str__(self):
        return str(self.items)


class Gift():
    """ Gift of a large marble and a bag of marbles - Don't change for the 93% """

    def __init__(self, large_marble, marbles):
        self.large_marble = large_marble
        self.marbles = marbles

    def __str__(self):
        marbles = str(self.marbles)
        marbles = marbles.replace("'", "")
        return f'Large marble: {self.large_marble}, marbles: {marbles[1:-1]}'


class Marble_Creator(mp.Process):
    """ This class "creates" marbles and sends them to the bagger """

    colors = ('Gold', 'Orange Peel', 'Purple Plum', 'Blue', 'Neon Silver', 
        'Tuscan Brown', 'La Salle Green', 'Spanish Orange', 'Pale Goldenrod', 'Orange Soda', 
        'Maximum Purple', 'Neon Pink', 'Light Orchid', 'Russian Violet', 'Sheen Green', 
        'Isabelline', 'Ruby', 'Emerald', 'Middle Red Purple', 'Royal Orange', 'Big Dip O’ruby', 
        'Dark Fuchsia', 'Slate Blue', 'Neon Dark Green', 'Sage', 'Pale Taupe', 'Silver Pink', 
        'Stop Red', 'Eerie Black', 'Indigo', 'Ivory', 'Granny Smith Apple', 
        'Maximum Blue', 'Pale Cerulean', 'Vegas Gold', 'Mulberry', 'Mango Tango', 
        'Fiery Rose', 'Mode Beige', 'Platinum', 'Lilac Luster', 'Duke Blue', 'Candy Pink', 
        'Maximum Violet', 'Spanish Carmine', 'Antique Brass', 'Pale Plum', 'Dark Moss Green', 
        'Mint Cream', 'Shandy', 'Cotton Candy', 'Beaver', 'Rose Quartz', 'Purple', 
        'Almond', 'Zomp', 'Middle Green Yellow', 'Auburn', 'Chinese Red', 'Cobalt Blue', 
        'Lumber', 'Honeydew', 'Icterine', 'Golden Yellow', 'Silver Chalice', 'Lavender Blue', 
        'Outrageous Orange', 'Spanish Pink', 'Liver Chestnut', 'Mimi Pink', 'Royal Red', 'Arylide Yellow', 
        'Rose Dust', 'Terra Cotta', 'Lemon Lime', 'Bistre Brown', 'Venetian Red', 'Brink Pink', 
        'Russian Green', 'Blue Bell', 'Green', 'Black Coral', 'Thulian Pink', 
        'Safety Yellow', 'White Smoke', 'Pastel Gray', 'Orange Soda', 'Lavender Purple',
        'Brown', 'Gold', 'Blue-Green', 'Antique Bronze', 'Mint Green', 'Royal Blue', 
        'Light Orange', 'Pastel Blue', 'Middle Green')

    def __init__(self, delay, parent_conn, marble_count):
        mp.Process.__init__(self)
        self.parent_conn = parent_conn
        self.marble_count = marble_count
        self.delay = delay

    def run(self):
        '''
        for each marble:
            send the marble (one at a time) to the bagger
              - A marble is a random name from the colors list above
            sleep the required amount
        Let the bagger know there are no more marbles
        '''
        for _ in range(self.marble_count):
            self.parent_conn.send(random.choice(self.colors))
            time.sleep(self.delay)
        self.parent_conn.send(NO_MORE)
        self.parent_conn.close()
        
class Bagger(mp.Process):
    """ Receives marbles from the marble creator, then there are enough
        marbles, the bag of marbles are sent to the assembler """
    def __init__(self, delay, size, child_conn, parent_conn):
        mp.Process.__init__(self)
        self.delay = delay
        self.size = size
        self.child_conn = child_conn
        self.parent_conn = parent_conn

    def run(self):
        '''
        while there are marbles to process
            collect enough marbles for a bag
            send the bag to the assembler
            sleep the required amount
        tell the assembler that there are no more bags
        '''
        bag = Bag()
        while True:
            mar = self.child_conn.recv()
            if mar == NO_MORE:
                break
            bag.add(mar)
            if bag.get_size() == self.size:
                self.parent_conn.send(bag)
                time.sleep(self.delay)
                bag = Bag()
        self.parent_conn.send(NO_MORE)
        self.parent_conn.close()

class Assembler(mp.Process):
    """ Take the set of marbles and create a gift from them.
        Sends the completed gift to the wrapper """
    marble_names = ('Lucky', 'Spinner', 'Sure Shot', 'The Boss', 'Winner', '5-Star', 'Hercules', 'Apollo', 'Zeus')

    def __init__(self, delay, count, child_conn, parent_conn):
        mp.Process.__init__(self)
        self.delay = delay
        self.count = count
        self.child_conn = child_conn
        self.parent_conn = parent_conn

    def run(self):
        '''
        while there are bags to process
            create a gift with a large marble (random from the name list) and the bag of marbles
            send the gift to the wrapper
            sleep the required amount
        tell the wrapper that there are no more gifts
        '''
        while True:
            bag = self.child_conn.recv()
            if bag == NO_MORE:
                break
            gift = Gift(random.choice(self.marble_names), bag)
            self.count.value += 1
            self.parent_conn.send(gift)
            time.sleep(self.delay)
        self.parent_conn.send(NO_MORE)
        self.parent_conn.close()

class Wrapper(mp.Process):
    """ Takes created gifts and wraps them by placing them in the boxes file """
    def __init__(self, delay, child_conn):
        mp.Process.__init__(self)
        self.delay = delay
        self.child_conn = child_conn

    def run(self):
        '''
        open file for writing
        while there are gifts to process
            save gift to the file with the current time
            sleep the required amount
        '''
        with open(BOXES_FILENAME, 'w') as f:
            while True:
                gift = self.child_conn.recv()
                if gift == NO_MORE:
                    break
                f.write(time.strftime("%H:%M:%S: ", time.gmtime()) + str(gift) + "\n")
                time.sleep(self.delay)


def display_final_boxes(filename, log):
    """ Display the final boxes file to the log file -  Don't change """
    if os.path.exists(filename):
        log.write(f'Contents of {filename}')
        with open(filename) as boxes_file:
            for line in boxes_file:
                log.write(line.strip())
    else:
        log.write_error(f'The file {filename} doesn\'t exist.  No boxes were created.')



def main():
    """ Main function """

    log = Log(show_terminal=True)

    log.start_timer()

    # Load settings file
    settings = load_json_file(CONTROL_FILENAME)
    if settings == {}:
        log.write_error(f'Problem reading in settings file: {CONTROL_FILENAME}')
        return

    log.write(f'Marble count                = {settings[MARBLE_COUNT]}')
    log.write(f'settings["creator-delay"]   = {settings[CREATOR_DELAY]}')
    log.write(f'settings["bag-count"]       = {settings[BAG_COUNT]}') 
    log.write(f'settings["bagger-delay"]    = {settings[BAGGER_DELAY]}')
    log.write(f'settings["assembler-delay"] = {settings[ASSEMBLER_DELAY]}')
    log.write(f'settings["wrapper-delay"]   = {settings[WRAPPER_DELAY]}')

    creator_parent, bagger_child = mp.Pipe()
    bagger_parent, assembler_child = mp.Pipe()
    assembler_parent, wrapper_child = mp.Pipe()

    gifts = mp.Value('i', 0)

    # delete final boxes file
    if os.path.exists(BOXES_FILENAME):
        os.remove(BOXES_FILENAME)

    log.write('Create the processes')
    processes = []
    processes.append(Marble_Creator(settings[CREATOR_DELAY], creator_parent, settings[MARBLE_COUNT]))
    processes.append(Bagger(settings[BAGGER_DELAY], settings[BAG_COUNT], bagger_child, bagger_parent))
    processes.append(Assembler(settings[ASSEMBLER_DELAY], gifts, assembler_child, assembler_parent))
    processes.append(Wrapper(settings[WRAPPER_DELAY], wrapper_child))

    log.write('Starting the processes')
    for p in processes:
        p.start()

    log.write('Waiting for processes to finish')
    for p in processes:
        p.join()

    display_final_boxes(BOXES_FILENAME, log)

    log.write(f'Total Gifts Made: {gifts.value}')



if __name__ == '__main__':
    main()

