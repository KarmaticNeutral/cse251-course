"""
Course: CSE 251
Lesson Week: 09
File: team2.py

Purpose: team activity - Dining philosophers problem

Problem statement

Five silent philosophers sit at a round table with bowls of spaghetti. Forks
are placed between each pair of adjacent philosophers.

Each philosopher must alternately think and eat. However, a philosopher can
only eat spaghetti when they have both left and right forks. Each fork can be
held by only one philosopher and so a philosopher can use the fork only if it
is not being used by another philosopher. After an individual philosopher
finishes eating, they need to put down both forks so that the forks become
available to others. A philosopher can only take the fork on their right or
the one on their left as they become available and they cannot start eating
before getting both forks.  When a philosopher is finished eating, they think 
for a little while.

Eating is not limited by the remaining amounts of spaghetti or stomach space;
an infinite supply and an infinite demand are assumed.

The problem is how to design a discipline of behavior (a concurrent algorithm)
such that no philosopher will starve

Instructions:

        **************************************************
        ** DO NOT search for a solution on the Internet **
        ** your goal is not to copy a solution, but to  **
        ** work out this problem.                       **
        **************************************************

- This is the same problem as last team activity.  However, you will implement a waiter.  
  When a philosopher wants to eat, it will ask the waiter if it can.  If the waiter 
  indicates that a philosopher can eat, the philosopher will pick up each fork and eat.  
  There must not be a issue picking up the two forks since the waiter is in control of 
  the forks and when philosophers eat.  When a philosopher is finished eating, it will 
  informs the waiter that he/she is finished.  If the waiter indicates to a philosopher
  that they can not eat, the philosopher will wait between 1 to 3 seconds and try again.

- You have Locks and Semaphores that you can use.
- Remember that lock.acquire() has an argument called timeout.
- philosophers need to think for 3 to 5 seconds when they get both forks.  
  When the number of philosophers has eaten MAX_MEALS times, stop the philosophers
  from trying to eat and any philosophers eating will put down their forks when finished.
- When a philosopher is not eating, it will think for 3 to 5 seconds.
- You want as many philosophers to eat and think concurrently.
- Design your program to handle N philosophers.
- Use threads for this problem.
- When you get your program working, how to you prove that no philosopher will starve?
  (Just looking at output from print() statements is not enough)
- Are the philosophers each eating and thinking the same amount?
- Using lists for philosophers and forks will help you in this program.
  for example: philosophers[i] needs forks[i] and forks[i+1] to eat


"""
import time
import threading


PHILOSOPHERS = 5
MAX_MEALS = PHILOSOPHERS * 100

class Waiter:
    def __init__(self):
        self.serving_lock = threading.Lock()
        self.is_eating = [False] * PHILOSOPHERS
        self.times_eaten = [0] * PHILOSOPHERS
    
    def canIEat(self, philosopherId):
        self.serving_lock.acquire()
        if min(self.times_eaten) > (self.times_eaten[philosopherId] - 3) and not self.is_eating[philosopherId - 1] and not self.is_eating[(philosopherId + 1) % PHILOSOPHERS]:
            self.times_eaten[philosopherId] += 1
            self.is_eating[philosopherId] = True
            self.serving_lock.release()
            return True
        self.serving_lock.release()
        return False

    def doneEating(self, philosopherId):
        self.is_eating[philosopherId] = False

    def allTimesEaten(self):
        return self.times_eaten

    def done(self):
        return MAX_MEALS <= sum(self.times_eaten)

def brain(id, leftFork, rightFork, waiter):
    def eat():
        if waiter.canIEat(id):
            leftFork.acquire()
            rightFork.acquire()
            print(str(id) + " is eating")
            time.sleep(0.5)
            leftFork.release()
            rightFork.release()
            waiter.doneEating(id)
        else:
            time.sleep(0.1)
            eat()

    def think():
        time.sleep(0.5)

    while True:
        eat()
        think()
        if waiter.done():
            break

def main():
    # TODO - create the waiter (A class would be best here)
    # TODO - create the forks
    # TODO - create PHILOSOPHERS philosophers
    # TODO - Start them eating and thinking
    # TODO - Display how many times each philosopher ate
    waiter = Waiter()
    forks = []
    for i in range(PHILOSOPHERS):
        forks.append(threading.Lock())
    phils = []
    for j in range(PHILOSOPHERS):
        phils.append(threading.Thread(target=brain,args=(j, forks[j], forks[(j + 1) % PHILOSOPHERS], waiter)))

    for p in phils:
        p.start()
    for p in phils:
        p.join()

    print(waiter.allTimesEaten())

if __name__ == '__main__':
    main()
