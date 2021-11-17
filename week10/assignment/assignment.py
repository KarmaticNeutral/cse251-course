"""
Course: CSE 251
Lesson Week: 10
File: assignment.py
Author: Timothy Taylor

Purpose: assignment for week 10 - reader writer problem

Instructions:

- Review TODO comments

- writer: a process that will send numbers to the reader.  
  The values sent to the readers will be in consecutive order starting
  at value 1.  Each writer will use all of the sharedList buffer area
  (ie., BUFFER_SIZE memory positions)

- reader: a process that receive numbers sent by the writer.  The reader will
  accept values until indicated by the writer that there are no more values to
  process.  Display the numbers received by printing them to the console.

- Create 2 writer processes

- Create 2 reader processes

- You can use sleep() statements for any process.

- You are able (should) to use lock(s) and semaphores(s).  When using locks, you can't
  use the arguments "block=False" or "timeout".  Your goal is to make your
  program as parallel as you can.  Over use of lock(s) or lock(s) in the wrong
  place will slow down your code.

- You must use ShareableList between the two processes.  This shareable list
  will contain different "sections".  There can only be one shareable list used
  between your processes.
  1) BUFFER_SIZE number of positions for data transfer. This buffer area must
	 act like a queue - First In First Out.
  2) current value used by writers for consecutive order of values to send
  3) Any indexes that the processes need to keep track of the data queue
  4) Any other values you need for the assignment

- Not allowed to use Queue(), Pipe(), List() or any other data structure.

- Not allowed to use Value() or Array() or any other shared data type from 
  the multiprocessing package.

Add any comments for me:


"""
import random
from multiprocessing.managers import SharedMemoryManager
import multiprocessing as mp
import time

BUFFER_SIZE = 10
NEXT_VALUE = BUFFER_SIZE
READ_INDEX = BUFFER_SIZE + 1
WRITE_INDEX = BUFFER_SIZE + 2
DONE_INDEX = BUFFER_SIZE + 3
READ_COUNT = BUFFER_SIZE + 4

WRITERS = 2
READERS = 2

def printSharedList(sharedList):
	print(sharedList)
	print(f'Next Val: {sharedList[NEXT_VALUE]}')
	print(f'Read Index: {sharedList[READ_INDEX]}')
	print(f'Write Index: {sharedList[WRITE_INDEX]}')
	print(f'Finished Processes: {sharedList[DONE_INDEX]}')
	print(f'Read Values: {sharedList[READ_COUNT]}')

def writer(id, sharedList, listLock, items_to_send):
	for _ in range(items_to_send):
		listLock.acquire()
		while sharedList[READ_INDEX] == (sharedList[WRITE_INDEX] + 1) % BUFFER_SIZE:
			listLock.release()
			#print(f'Writer #{id}:')
			#printSharedList(sharedList)
			time.sleep(0.1)
			listLock.acquire()
		sharedList[sharedList[WRITE_INDEX]] = sharedList[NEXT_VALUE]
		sharedList[NEXT_VALUE] += 1
		sharedList[WRITE_INDEX] = (sharedList[WRITE_INDEX] + 1) % BUFFER_SIZE
		listLock.release()
	listLock.acquire()
	sharedList[DONE_INDEX] += 1
	#print(f'Writer #{id} Done')
	#printSharedList(sharedList)
	listLock.release()
	

def reader(id, sharedList, listLock):
	while True:
		listLock.acquire()
		if sharedList[READ_INDEX] == sharedList[WRITE_INDEX]:
			if sharedList[DONE_INDEX] == WRITERS:
				listLock.release()
				#print(f'Reader #{id} Done')
				#printSharedList(sharedList)
				break
			else:
				listLock.release()
				#print(f'Reader #{id}:')
				#printSharedList(sharedList)
				time.sleep(0.1)
		else:
			#print(sharedList[sharedList[READ_INDEX]])
			sharedList[sharedList[READ_INDEX]] = 0
			sharedList[READ_INDEX] = (sharedList[READ_INDEX] + 1) % 10
			sharedList[READ_COUNT] += 1
			listLock.release()
			

def main():
	# This is the number of values that the writer will send to the reader
	items_to_send = random.randint(10, 100)
	#print(items_to_send)

	smm = SharedMemoryManager()
	smm.start()

	# TODO - Create a ShareableList to be used between the processes
	sharedList = mp.shared_memory.ShareableList([0] * (BUFFER_SIZE + 5))
	
	# TODO - Create any lock(s) or semaphore(s) that you feel you need
	listLock = mp.Lock()

	# TODO - create reader and writer processes
	writers = []
	remainder = items_to_send % WRITERS
	for i in range(WRITERS):
		writers.append(mp.Process(target=writer, args=(i, sharedList, listLock, items_to_send // WRITERS if i < remainder else (items_to_send // WRITERS) + 1)))
	readers = []
	for i in range(READERS):
		readers.append(mp.Process(target=reader, args=(i, sharedList, listLock)))

	# TODO - Start the processes and wait for them to finish
	for w in writers:
		w.start()
	for r in readers:
		r.start()
	for w in writers:
		w.join()
	for r in readers:
		r.join()

	print(f'{items_to_send} values sent')
	# TODO - Display the number of numbers/items received by the reader.
	#        Can not use "items_to_send", must be a value collected
	#        by the reader processes.
	# print(f'{<your variable>} values received')
	print(f'{sharedList[READ_COUNT]} values read')

	smm.shutdown()


if __name__ == '__main__':
	main()
