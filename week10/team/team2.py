"""
Course: CSE 251
Lesson Week: 10
File: team2.py
Author: Brother Comeau
Instructions:
- Look for the TODO comments
"""

import time
import threading
import mmap

# -----------------------------------------------------------------------------
def reverse_file(filename):
    """ Display a file in reverse order using a mmap file. """
    # TODO add code here
    with open(filename, mode="r", encoding="utf8") as file_obj:
        with mmap.mmap(file_obj.fileno(), length=0, access=mmap.ACCESS_READ) as mmap_obj:
            print(mmap_obj[::-1])

# -----------------------------------------------------------------------------
def promote_letter_a(filename):
    """ 
    change the given file with these rules:
    1) when the letter is 'a', uppercase it
    2) all other letters are changed to the character '.'

    You are not creating a different file.  Change the file using mmap file.
    """
    # TODO add code here

    with open(filename, mode="r+", encoding="utf8") as file_obj:
        with mmap.mmap(file_obj.fileno(), length=0, access=mmap.ACCESS_WRITE) as mmap_obj:
            print(mmap_obj[:300])
            for i in range(mmap_obj.size()):
                mmap_obj[i] = 65 if mmap_obj[i] == 97 else 46
            print(mmap_obj[:300])
            


# -----------------------------------------------------------------------------
def promote_letter_a_threads(filename, N):
    """ 
    change the given file with these rules:
    1) when the letter is 'a', uppercase it
    2) all other letters are changed to the character '.'

    You are not creating a different file.  Change the file using mmap file.

    Use N threads to process the file where each thread will be 1/N of the file.
    """
    # TODO add code here
    def helper(start, end):
        print(mmap_obj[:start+30])
        for i in range(start, end):
            mmap_obj[i] = 65 if mmap_obj[i] == 97 else 46
        print(mmap_obj[:start+30])

    with open(filename, mode="r+", encoding="utf8") as file_obj:
        with mmap.mmap(file_obj.fileno(), length=0, access=mmap.ACCESS_WRITE) as mmap_obj:
            threads = []
            size = mmap_obj.size()
            chunk = size // N
            for n in range(N):
                if (n == N - 1):
                    threads.append(threading.Thread(target=helper, args=(chunk * n, size - 1)))
                else:
                    threads.append(threading.Thread(target=helper, args=(n * chunk, ((n + 1) * chunk) - 1)))
            for t in threads:
                t.start()
            for t in threads:
                t.join()

# -----------------------------------------------------------------------------
def main():
    reverse_file('data.txt')
    
    # TODO
    # When you get the function promote_letter_a() working
    #  1) Comment out the promote_letter_a() call
    #  2) run create_Data_file.py again to re-create the "letter_a.txt" file
    #  3) Uncomment the function below
    # promote_letter_a_threads('letter_a.txt')

if __name__ == '__main__':
    main()
