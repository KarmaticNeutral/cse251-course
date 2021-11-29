"""
Course: CSE 251
Lesson Week: 11
File: Assignment.py
"""

import time
import random
import multiprocessing as mp
from multiprocessing.managers import SharedMemoryManager

# number of cleaning staff and hotel guests
CLEANING_STAFF = 2
HOTEL_GUESTS = 5

# Run program for this number of seconds
TIME = 60

STARTING_PARTY_MESSAGE =  'Turning on the lights for the party vvvvvvvvvvvvvv'
STOPPING_PARTY_MESSAGE  = 'Turning off the lights  ^^^^^^^^^^^^^^^^^^^^^^^^^^'

STARTING_CLEANING_MESSAGE =  'Starting to clean the room >>>>>>>>>>>>>>>>>>>>>>>>>>>>>'
STOPPING_CLEANING_MESSAGE  = 'Finish cleaning the room <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<'

PARTY_COUNT = 0
CLEAN_COUNT = 1
LIGHT = 2
PEOPLE_COUNT = 3

# -----------------------------------------------------------------------------
def cleaner_waiting():
    time.sleep(random.uniform(0, 2))

# -----------------------------------------------------------------------------
def cleaner_cleaning(id):
    print(f'Cleaner {id}')
    time.sleep(random.uniform(0, 2))

# -----------------------------------------------------------------------------
def guest_waiting():
    time.sleep(random.uniform(0, 2))

# -----------------------------------------------------------------------------
def guest_partying(id):
    print(f'Guest {id}')
    time.sleep(random.uniform(0, 1))

# -----------------------------------------------------------------------------
def cleaner(id, sharedList, end_time, cleaningLock, partyLock):
    """
    do the following for TIME seconds
    cleaner will wait to try to clean the room (cleaner_waiting())
    get access to the room
        display message STARTING_CLEANING_MESSAGE
        Take some time cleaning (cleaner_cleaning())
        display message STOPPING_CLEANING_MESSAGE
    """
    while time.time() < end_time:
        cleaner_waiting()
        with partyLock:
            if(sharedList[LIGHT] == 0):
                with cleaningLock:
                    print(STARTING_CLEANING_MESSAGE)
                    cleaner_cleaning(id)
                    print(STOPPING_CLEANING_MESSAGE)
                    sharedList[CLEAN_COUNT] += 1

# -----------------------------------------------------------------------------
def guest(id, sharedList, end_time, partyLock):
    """
    do the following for TIME seconds
    guest will wait to try to get access to the room (guest_waiting())
    get access to the room
        display message STARTING_PARTY_MESSAGE if this guest is the first one in the room
        Take some time partying (guest_partying())
        display message STOPPING_PARTY_MESSAGE if the guest is the last one leaving in the room
    """
    while time.time() < end_time:
        guest_waiting()
        with partyLock:
            if(sharedList[LIGHT] == 0):
                print(STARTING_PARTY_MESSAGE)
                sharedList[LIGHT] = 1
            sharedList[PEOPLE_COUNT] += 1

        guest_partying(id)

        with partyLock:
            sharedList[PEOPLE_COUNT] -= 1

            if(sharedList[PEOPLE_COUNT] == 0):
                print(STOPPING_PARTY_MESSAGE)
                sharedList[LIGHT] = 0
                sharedList[PARTY_COUNT] += 1
                
# -----------------------------------------------------------------------------
def main():
    # TODO - add any variables, data structures, processes you need
    # TODO - add any arguments to cleaner() and guest() that you need
    smm = SharedMemoryManager()
    smm.start()

    sharedList = smm.ShareableList([0] * 4)
    cleaningLock = mp.Lock()
    partyLock = mp.Lock()

    # Start time of the running of the program. 
    start_time = time.time()
    end_time = start_time + TIME

    processes = []
    for i in range(CLEANING_STAFF):
        processes.append(mp.Process(target=cleaner, args=(i + 1, sharedList, end_time, cleaningLock, partyLock)))
    for i in range(HOTEL_GUESTS):
        processes.append(mp.Process(target=guest, args=(i + 1, sharedList, end_time, partyLock)))
    
    for t in processes:
        t.start()
    for t in processes:
        t.join()

    # Results
    print(f'Room was cleaned {sharedList[CLEAN_COUNT]} times, there were {sharedList[PARTY_COUNT]} parties')

    smm.shutdown()

if __name__ == '__main__':
    main()

