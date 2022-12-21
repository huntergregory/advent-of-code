package main

import (
	"bufio"
	"fmt"
	"log"
	"os"
)

// parameters
const (
	inputFile = "inputs/input.txt"
)

func main() {
	input := parseInput()
	fmt.Println(input)
}

func parseInput() []int {
	file, err := os.Open(inputFile)
	if err != nil {
		log.Fatal(err)
	}
	defer file.Close()

	// var line string
	scanner := bufio.NewScanner(file)
	for scanner.Scan() {
		// scanner.Text()
	}

	if err := scanner.Err(); err != nil {
		log.Fatal(err)
	}

	return nil
}
