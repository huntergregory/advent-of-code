// In a real life scenario, might stream a message and avoid memory overhead.
// Uses two buffers: one for input, and one for processing.

package main

import (
	"bufio"
	"fmt"
	"io"
	"log"
	"os"
	"time"
)

const (
	markerSize       = 14
	ingestorCapacity = 128
	fileBufferSize   = 32
)

type ingestor struct {
	input       <-chan rune
	packetCount int
	marker      [markerSize]rune
	markerStart int
}

func newIngestor(ch <-chan rune) *ingestor {
	return &ingestor{
		input: ch,
	}
}

func (i *ingestor) ingest() {
	for {
		select {
		case packet := <-i.input:
			if i.packetCount-i.markerStart+1 == markerSize {
				// process message...
				break
			}

			i.packetCount++
			i.marker[i.packetCount%markerSize] = packet
			for j := i.packetCount - 1; j >= i.markerStart; j-- {
				if packet == i.marker[j%markerSize] {
					i.markerStart = j + 1
					break
				}
			}

			if i.packetCount-i.markerStart+1 == markerSize {
				fmt.Printf("found end of marker at packet %d\n", i.packetCount)
			}
		}
	}
}

// hard to compare to Python. Taking > 0.3 seconds to run an empty main() function.
func main() {
	f, err := os.Open("input/input.txt")
	if err != nil {
		log.Fatal(err)
	}
	defer f.Close()

	input := make(chan rune, ingestorCapacity)
	ingestor := newIngestor(input)
	go ingestor.ingest()

	reader := bufio.NewReader(f)
	buf := make([]byte, fileBufferSize)
	for {
		n, err := reader.Read(buf)
		if err != nil {
			if err != io.EOF {
				log.Fatal(err)
			}
			break
		}

		for i := 0; i < n; i++ {
			input <- rune(buf[i])
		}
	}

	// close(input)
	fmt.Println("finished reading file. sleeping while go routine finishes...")
	time.Sleep(1 * time.Second)
	fmt.Println("finished script")
}
