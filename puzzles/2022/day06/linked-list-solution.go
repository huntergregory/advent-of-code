// In a real life scenario, might stream a message and avoid memory overhead.
// Using a linked list works, but would probably be over-engineered.

package main

import (
	"bufio"
	"fmt"
	"io"
	"log"
	"os"
)

const (
	markerSize     = 14
	fileBufferSize = 32
)

type Node struct {
	data rune
	next *Node
}

// hard to compare to Python. Taking > 0.3 seconds to run an empty main() function.
func main2() {
	f, err := os.Open("input.txt")
	if err != nil {
		log.Fatal(err)
	}
	defer f.Close()

	reader := bufio.NewReader(f)
	buf := make([]byte, fileBufferSize)
	readCount := 0
	// linked list will have the newest (right-most) letter as the head
	// head.next will be the previous letter
	size := 0
	var head *Node
readLoop:
	for {
		n, err := reader.Read(buf)
		if err != nil {
			if err != io.EOF {
				log.Fatal(err)
			}
			break
		}

		for i := 0; i < n; i++ {
			newNode := &Node{
				data: rune(buf[i]),
			}

			if head == nil {
				// intialize for the very first letter
				head = newNode
				size++
			} else {
				// add newNode to the linked list
				newNode.next = head
				size++

				// cut off the linked list where a duplicate happens
				h := head
				priorH := newNode
				steps := 1
				for h != nil {
					if newNode.data == h.data {
						priorH.next = nil
						size = steps
						break
					}

					priorH = h
					h = h.next
					steps++
				}

				// update the tail
				head = newNode

				if size == markerSize {
					fmt.Printf("found marker at character %d\n", readCount*fileBufferSize+i+1)
					break readLoop
				}
			}
		}

		readCount++
	}

	fmt.Println("finished reading file")
}
