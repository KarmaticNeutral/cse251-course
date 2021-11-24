/************************************
Course: cse 251
File: team1.java
Week: week 11 - team activity 1

Instructions:

- Main contains an array of 1,000 random values.  You will be creating
  threads to process this array.  If you find a prime number, display
  it to the console.

- DON'T copy/slice the array in main() for each thread.

Part 1:
- Create a class that is a sub-class of Thread.
- create 4 threads based on this class you created.
- Divide the array among the threads.

Part 2:
- Create a class on an interface or Runnable
- create 4 threads based on this class you created.
- Divide the array among the threads.

Part 3:
- Modify part1 or part 2 to handle any size array and any number
  of threads.

************************************/
import java.util.Random; 
import java.lang.Math;

class PrimeThread extends Thread {
  private int[] arr;
  private int start;
  private int end;

  PrimeThread(int[] arr, int start, int end) {
    this.arr = arr;
    this.start = start;
    this.end = end;
  }

  @Override
  public void run() {
    for (int i = this.start; i <= this.end; i++) {
      if (isPrime(this.arr[i])) {
        System.out.println(this.arr[i]);
      }
    }
  }
  
  private static boolean isPrime(int n) 
  { 
      // Corner cases 
      if (n <= 1) return false; 
      if (n <= 3) return true; 
    
      // This is checked so that we can skip  
      // middle five numbers in below loop 
      if (n % 2 == 0 || n % 3 == 0) return false; 
    
      for (int i = 5; i * i <= n; i = i + 6) 
        if (n % i == 0 || n % (i + 2) == 0) 
          return false; 
    
      return true; 
  }
}

class RunnablePrime implements Runnable {
  private int[] arr;
  private int start;
  private int end;

  public RunnablePrime(int[] arr, int start, int end) {
    this.arr = arr;
    this.start = start;
    this.end = end;
  }

  @Override
  public void run() {
    for (int i = this.start; i <= this.end; i++) {
      if (isPrime(this.arr[i])) {
        System.out.println(this.arr[i]);
      }
    }
  }
  
  private static boolean isPrime(int n) 
  { 
      // Corner cases 
      if (n <= 1) return false; 
      if (n <= 3) return true; 
    
      // This is checked so that we can skip  
      // middle five numbers in below loop 
      if (n % 2 == 0 || n % 3 == 0) return false; 
    
      for (int i = 5; i * i <= n; i = i + 6) 
        if (n % i == 0 || n % (i + 2) == 0) 
          return false; 
    
      return true; 
  }
}

class Main {

  static boolean isPrime(int n) 
  { 
      // Corner cases 
      if (n <= 1) return false; 
      if (n <= 3) return true; 
    
      // This is checked so that we can skip  
      // middle five numbers in below loop 
      if (n % 2 == 0 || n % 3 == 0) return false; 
    
      for (int i = 5; i * i <= n; i = i + 6) 
        if (n % i == 0 || n % (i + 2) == 0) 
          return false; 
    
      return true; 
  }

  public static void main(String[] args) {
    System.out.println("Hello world!");

    // create instance of Random class 
    Random rand = new Random(); 

    int count = 1000;
    int[] array = new int[count];
    for (int i = 0; i < count; i++) 
    {
      array[i] = Math.abs(rand.nextInt());
    }

    System.out.println("Primes the First");

    int threadCount = 4;
    PrimeThread[] threads = new PrimeThread[threadCount];
    for (int i = 0; i < threadCount; i++) {
      if (i == threadCount - 1) {
        threads[i] = new PrimeThread(array, i * (count / threadCount), count - 1);
      } else {
        threads[i] = new PrimeThread(array, i * (count / threadCount), ((i + 1) * (count / threadCount)) - 1);
      }
      threads[i].start();
    }

    System.out.println("Primes the Second");

    Thread[] runnableThreads = new Thread[threadCount];
    for (int i = 0; i < threadCount; i++) {
      if (i == threadCount - 1) {
        runnableThreads[i] = new Thread(
          new RunnablePrime(array, i * (count / threadCount), count - 1)
        );
      } else {
        runnableThreads[i] = new Thread(
          new RunnablePrime(array, i * (count / threadCount), ((i + 1) * (count / threadCount)) - 1)
        );
      }
      runnableThreads[i].start();
    }

  }
}