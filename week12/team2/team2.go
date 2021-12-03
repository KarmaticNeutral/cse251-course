/* ---------------------------------------
Course: CSE 251
Lesson Week: ?12
File: team.go
Author: Brother Comeau

Purpose: team activity - finding primes

Instructions:

- Process the array of numbers, find the prime numbers using goroutines

worker()

This goroutine will take in a list/array/channel of numbers.  It will place
prime numbers on another channel


readValue()

This goroutine will display the contents of the channel containing
the prime numbers

--------------------------------------- */
package main

import (
	"fmt"
	"math/rand"
	//"sync"
	"time"
)

func isPrime(n int) bool {
	// Primality test using 6k+-1 optimization.
	// From: https://en.wikipedia.org/wiki/Primality_test

	if n <= 3 {
		return n > 1
	}

	if n%2 == 0 || n%3 == 0 {
		return false
	}

	i := 5
	for (i * i) <= n {
		if n%i == 0 || n%(i+2) == 0 {
			return false
		}
		i += 6
	}
	return true
}

func worker(bulkNum chan int, primes chan int) {//, wg *sync.WaitGroup) {
	for num := range bulkNum {
    if isPrime(num) {
      primes <- num
    }
  }

  //wg.Done()
}

func readValues(primes chan int) {//, wg *sync.WaitGroup) {
  for p := range primes {
  	fmt.Println(p)
  }

  //wg.Done()
}

func main() {

	workers := 10
	numberValues := 100

  bulkNum := make(chan int)
  primes := make(chan int)

  //var wg sync.WaitGroup
  //wg.Add(workers + 1)

	// create workers
	for w := 1; w <= workers; w++ {
		go worker(bulkNum, primes)//, &wg) // Add any arguments
	}
  

	rand.Seed(time.Now().UnixNano())
	for i := 0; i < numberValues; i++ { 
    //fmt.Println(rand.Intn(1000))
		bulkNum <- rand.Int()
	}

	go readValues(primes)//, &wg) // Add any arguments

  //wg.Wait()

  time.Sleep(20 * time.Second)

	fmt.Println("All Done!")
}
