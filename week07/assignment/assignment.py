"""
Course: CSE 251
Lesson Week: 07
File: assingnment.py
Author: Tim Taylor
Purpose: Process Task Files

Instructions:  See I-Learn

I ran a test on a limited sample of 100 of each task
with a varied number of threads to test each pool for all
sizes from 1 to 4. I found that with my 4 core computer, 
the fastest pool sizes were:
Primes: 1
Word: 2
Text: 1
Sum: 1
APICall: 1

"""

from datetime import datetime, timedelta
import requests
import threading
import multiprocessing as mp
from matplotlib.pylab import plt
import numpy as np
import glob
import math 
import itertools

# Include cse 251 common Python files - Dont change
import os, sys
sys.path.append('../../code')   # Do not change the path.
from cse251 import *

TYPE_PRIME  = 'prime'
TYPE_WORD   = 'word'
TYPE_UPPER  = 'upper'
TYPE_SUM    = 'sum'
TYPE_NAME   = 'name'

# Global lists to collect the task results
result_primes = []
result_words = []
result_upper = []
result_sums = []
result_names = []

class API_Call(threading.Thread):
    def __init__(self, URL, requestTitle):
        threading.Thread.__init__(self)
        self.URL = URL
        self.requestTitle = requestTitle

    def run(self):
        response = requests.get(self.URL)

        if response.status_code == 200:
            self.data = response.json()
        else:
            print("Error Executing " + self.requestTitle + " Request")

def is_prime(n: int):
    """Primality test using 6k+-1 optimization.
    From: https://en.wikipedia.org/wiki/Primality_test
    """
    if n <= 3:
        return n > 1
    if n % 2 == 0 or n % 3 == 0:
        return False
    i = 5
    while i ** 2 <= n:
        if n % i == 0 or n % (i + 2) == 0:
            return False
        i += 6
    return True
 
def task_prime(value):
    return f'{value} is prime' if is_prime(value) else f'{value} is not prime'

def task_word(word):
    with open("words.txt") as f:
        while True:
            line = f.readline()
            if not line:
                return f'{word} not found *****'
            if word == line.strip():
                return f'{word} Found'

def task_upper(text):
    return text.upper()

def task_sum(start_value, end_value):
    total = sum(range(start_value, end_value + 1))
    return f'sum of {start_value} to {end_value} = {total}'

def task_name(url):
    call = API_Call(url, "URL Task: {url}")
    call.start()
    call.join()
    return f'{url} has name {call.data[TYPE_NAME]}' if call.data else f'{url} had an error receiving the information'

def main():
    log = Log(show_terminal=True)
    # lists = [
    #     range(1, 4),
    #     range(1, 4),
    #     range(1, 4),
    #     range(1, 4),
    #     range(1, 4),
    # ]
    # for prime_size, word_size, text_size, sum_size, url_size in itertools.product(*lists):
    #     for attempts in range(2):
    log.start_timer()

    # TODO Create process pools
    prime_pool = mp.Pool(1) #prime_size)
    word_pool = mp.Pool(2) #word_size)
    text_pool = mp.Pool(1) #text_size)
    sum_pool = mp.Pool(1) #sum_size)
    url_pool = mp.Pool(1) #url_size)

    count = 0
    task_files = glob.glob("*.task")
    for filename in task_files:
        task = load_json_file(filename)
        #print(task)
        count += 1
        task_type = task['task']
        if task_type == TYPE_PRIME:
            prime_pool.apply_async(task_prime, args=(task['value'],), callback = result_primes.append)
        elif task_type == TYPE_WORD:
            word_pool.apply_async(task_word, args=(task['word'],), callback = result_words.append)
        elif task_type == TYPE_UPPER:
            text_pool.apply_async(task_upper, args=(task['text'],), callback = result_upper.append)
        elif task_type == TYPE_SUM:
            sum_pool.apply_async(task_sum, args=(task['start'], task['end']), callback = result_sums.append)
        elif task_type == TYPE_NAME:
            url_pool.apply_async(task_name, args=(task['url'],), callback = result_names.append)
        else:
            log.write(f'Error: unknown task type {task_type}')

    # TODO start and wait pools
    prime_pool.close()
    word_pool.close()
    text_pool.close()
    sum_pool.close()
    url_pool.close()
    prime_pool.join()
    word_pool.join()
    text_pool.join()
    sum_pool.join()
    url_pool.join()

    # Do not change the following code (to the end of the main function)
    def log_list(lst, log):
        for item in lst:
            log.write(item)
        log.write(' ')
    
    log.write('-' * 80)
    log.write(f'Primes: {len(result_primes)}')
    log_list(result_primes, log)

    log.write('-' * 80)
    log.write(f'Words: {len(result_words)}')
    log_list(result_words, log)

    log.write('-' * 80)
    log.write(f'Uppercase: {len(result_upper)}')
    log_list(result_upper, log)

    log.write('-' * 80)
    log.write(f'Sums: {len(result_sums)}')
    log_list(result_sums, log)

    log.write('-' * 80)
    log.write(f'Names: {len(result_names)}')
    log_list(result_names, log)

    log.write(f'Primes: {len(result_primes)}')
    log.write(f'Words: {len(result_words)}')
    log.write(f'Uppercase: {len(result_upper)}')
    log.write(f'Sums: {len(result_sums)}')
    log.write(f'Names: {len(result_names)}')
    # log.write(f'Prime Size: {prime_size}')
    # log.write(f'Word Size: {word_size}')
    # log.write(f'Uppercase Size: {text_size}')
    # log.write(f'Sum Size: {sum_size}')
    # log.write(f'Name Size: {url_size}')
    log.stop_timer(f'Finished processes {count} tasks')

if __name__ == '__main__':
    main()
