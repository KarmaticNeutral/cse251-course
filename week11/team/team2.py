"""
Course: CSE 251
Lesson Week: 11
File: team2.py
Author: Brother Comeau

Purpose: Team Activity 2: Queue, Pipe, Stack

Instructions:

Part 1:
- Create classes for Queue_t, Pipe_t and Stack_t that are thread safe.
- You can use the List() data structure in your classes.
- Once written, test them using multiple threads.

Part 2
- Create classes for Queue_p, Pipe_p and Stack_p that are process safe.
- You can use the List() data structure in your classes.
- Once written, test them using multiple processes.

Queue methods:
    - constructor(<no arguments>)
    - size()
    - get()
    - put(item)

Stack methods:
    - constructor(<no arguments>)
    - push(item)
    - pop()

Steps:
1) write the Queue_t and test it with threads.
2) write the Queue_p and test it with processes.
3) Implement Stack_t and test it 
4) Implement Stack_p and test it 

Note: Testing means having lots of concurrency/parallelism happening.  Also
some methods for lists are thread safe - some are not.

"""
import time
import threading
import multiprocessing as mp

# -------------------------------------------------------------------
class Queue_t:
    def __init__(self):
        self.data = []
        self.lock = threading.Lock()

    def size(self):
        self.lock.acquire()
        size = len(self.data)
        self.lock.release()
        return size

    def get(self):
        self.lock.acquire()
        val = self.data.pop()
        self.lock.release()
        return val

    def put(self, item):
        self.lock.acquire()
        self.data.insert(0, item)
        self.lock.release()

# -------------------------------------------------------------------
class Stack_t:
    def __init__(self):
        self.data = []
        self.lock = threading.Lock()

    def push(self, item):
        self.lock.acquire()
        self.data.append(item)
        self.lock.release()
    
    def pop(self):
        self.lock.acquire()
        val = self.data.pop()
        self.lock.release()
        return val

# -------------------------------------------------------------------
class Queue_p:
    def __init__(self):
        self.data = []
        self.lock = mp.Lock()

    def size(self):
        self.lock.acquire()
        size = len(self.data)
        self.lock.release()
        return size

    def get(self):
        self.lock.acquire()
        val = self.data.pop()
        self.lock.release()
        return val

    def put(self, item):
        self.lock.acquire()
        self.data.insert(0, item)
        self.lock.release()
    

# -------------------------------------------------------------------
class Stack_p:
    def __init__(self):
        self.data = []
        self.lock = threading.Lock()

    def push(self, item):
        self.lock.acquire()
        self.data.append(item)
        self.lock.release()
    
    def pop(self):
        self.lock.acquire()
        val = self.data.pop()
        self.lock.release()
        return val

def enqueue(q, start, end):
    for i in range(start, end):
        print(i)
        q.put(i)

def dequeue(q):
    while q.size() > 0:
        print(q.get())

def testQueueT(threadCount):
    qt = Queue_t()
    threads = []
    for i in range(threadCount):
        threads.append(threading.Thread(target=enqueue, args=(qt, (i + 1) * 10, (i + 1) * 20)))

    for t in threads:
        t.start()
    for t in threads:
        t.join()

    threads = []
    for i in range(threadCount):
        threads.append(threading.Thread(target=dequeue, args=(qt,)))
    
    for t in threads:
        t.start()
    for t in threads:
        t.join()

def testQueueP(processCount):
    qp = Queue_p()
    processes = []
    for i in range(processCount):
        processes.append(mp.Process(target=enqueue, args=(qp, (i + 1) * 10, (i + 1) * 20)))

    for p in processes:
        p.start()
    for p in processes:
        p.join()

    processes = []
    for i in range(processCount):
        processes.append(mp.Process(target=dequeue, args=(qt,)))
    
    for p in processes:
        p.start()
    for p in processes:
        p.join()

def main():
    print("Queue Thread Test")
    testQueueT(5)
    print("Queue Process Test")
    testQueueP(5)
    
if __name__ == '__main__':
    main()
