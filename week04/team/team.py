"""
Course: CSE 251
Lesson Week: 04
File: team.py
Author: Brother Comeau

Purpose: Team Activity

Instructions:

- See in I-Learn

"""

import threading
import queue
import requests

# Include cse 251 common Python files
import os, sys
sys.path.append('../../code')   # Do not change the path.
from cse251 import *

RETRIEVE_THREADS = 38       # Number of retrieve_threads
NO_MORE_VALUES = 'No more'  # Special value to indicate no more items in the queue

def retrieve_thread(q, log):
    """ Process values from the data_queue """

    while True:
        url = q.get()
        if url == NO_MORE_VALUES:
            q.put(url)
            break
        
        r = requests.get(url).json()
        log.write(r['name'])

def file_reader(q, file_name, log):
    """ This thread reading the data file and places the values in the data_queue """

    with open(file_name) as f:
        line = f.readline().strip()
        q.put(line)
        while line:
            line = f.readline().strip()
            if line == '':
                continue
            q.put(line)

    log.write('finished reading file')

    q.put(NO_MORE_VALUES)


def main():
    """ Main function """

    log = Log(show_terminal=True)
    threads = []

    q = queue.Queue()
    sem = threading.Semaphore(1)

    for i in range(RETRIEVE_THREADS):
        threads.append(threading.Thread(target=retrieve_thread, args=(q, log)))
    threads.append(threading.Thread(target=file_reader, args=(q, 'data.txt', log)))

    log.start_timer()

    for t in threads:
        t.start()
    for t in threads:
        t.join()
    val = ""
    while not val == NO_MORE_VALUES:
        val = q.get()

    log.stop_timer('Time to process all URLS')


if __name__ == '__main__':
    main()




