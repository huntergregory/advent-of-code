package main

import (
	"bufio"
	"fmt"
	"log"
	"math"
	"os"
	"strconv"
)

// parameters
const (
	inputFile = "inputs/input.txt"
	debug     = false
)

// part 2
const (
	// for part 1 solution, set to 1
	multiplier = 811589153
	// for part 1 solution, set to 1
	numMixes = 10
)

type node struct {
	data int
	prev *node
	next *node
}

func main() {
	head := parseInput()
	if debug {
		printCircularList(head)
	}
	mixList(head)
	coordinates(head)
}

func coordinates(head *node) {
	zero := head
	for zero.data != 0 {
		zero = zero.next
	}

	curr := zero
	sum := 0
	for i := 1; i <= 3000; i++ {
		curr = curr.next
		if i == 1000 || i == 2000 || i == 3000 {
			sum += curr.data
		}
	}
	fmt.Printf("coordinate sum is %d\n", sum*multiplier)
}

func mixList(head *node) {
	originalOrder := make([]*node, 0)
	originalOrder = append(originalOrder, head)
	curr := head.next
	for curr != head {
		originalOrder = append(originalOrder, curr)
		curr = curr.next
	}

	length := len(originalOrder)
	for i := 0; i < numMixes; i++ {
		for _, curr := range originalOrder {
			if debug {
				fmt.Printf("beginning shifts for %d...\n", curr.data)
			}

			if curr.data == 0 {
				continue
			}

			toRight := curr.data > 0
			numShifts := int(math.Abs(float64(curr.data)))
			// part 2 multiplication
			numShifts *= multiplier
			numShifts %= length - 1
			for shiftCount := 0; shiftCount < numShifts; shiftCount++ {
				right := curr.next
				left := curr.prev

				if toRight {
					// update curr's pointers
					curr.prev = right
					curr.next = right.next

					// update pointers for new curr.next
					curr.next.prev = curr

					// update pointers for old left and right
					left.next = right
					right.prev = left
					right.next = curr
				} else {
					// update curr's pointers
					curr.next = left
					curr.prev = left.prev

					// update pointers for new curr.prev
					curr.prev.next = curr

					// update pointers for old left and right
					right.prev = left
					left.prev = curr
					left.next = right
				}

				if debug {
					fmt.Printf("shift #%d\n", shiftCount)
					printCircularList(head)
				}
			}
		}
	}
}

func printCircularList(head *node) {
	vals := make([]string, 0)
	curr := head
	for len(vals) == 0 || curr != head {
		vals = append(vals, fmt.Sprintf("%d", curr.data))
		curr = curr.next
	}

	fmt.Printf("linked list: %+v\n", vals)
}

// parseInput returns the head of a circular linked list
func parseInput() *node {
	file, err := os.Open(inputFile)
	if err != nil {
		log.Fatal(err)
	}
	defer file.Close()

	// var line string
	var head *node
	var previous *node
	scanner := bufio.NewScanner(file)
	for scanner.Scan() {
		val, _ := strconv.Atoi(scanner.Text())
		curr := &node{
			data: val,
			prev: previous,
			next: nil,
		}

		if head == nil {
			head = curr
			previous = curr
		} else {
			previous.next = curr
			curr.prev = previous
			previous = curr
		}
	}
	previous.next = head
	head.prev = previous

	if err := scanner.Err(); err != nil {
		log.Fatal(err)
	}

	return head
}
